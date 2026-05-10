"""fetch_product_images.py — A層メーカー公式HPから製品画像を取得して prototype/assets/maker-products/ に保存。

5/9 step-7 で group_1 (curl 方式) は 9 社成功、group_2/3 (WebFetch) は 21 社全件 denied。
本スクリプトは group_1 の curl 方式を汎用化し、残りの社へ再適用する。

方針:
  - requests + BeautifulSoup4 で公式HPを取得
  - og:image / <link rel="image_src"> / 製品ページ <img src= or data-src=> を候補に
  - HEAD 検証 (Content-Type=image/*, Content-Length>=5KB)
  - 各社最大 4 枚、prototype/assets/maker-products/{NNN}/{1..4}.{ext} に保存
  - 失敗社は data/maker_products.json に空配列 + skip_reason で記録
  - 既存 fetched_ok=true 社は不可侵 (--all 時もスキップ、--force で上書き)

Usage:
  python scripts/fetch_product_images.py             # 既存 NG + 未取得社をリトライ
  python scripts/fetch_product_images.py --only "082 100"
  python scripts/fetch_product_images.py --force --only "082"  # 既存 OK でも上書き
  python scripts/fetch_product_images.py --dry        # 取得計画のみ表示
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MAKERS_CSV = ROOT / "data" / "makers.csv"
PRODUCTS_PATH = ROOT / "data" / "maker_products.json"
BRAND_PATH = ROOT / "data" / "maker_brand.json"
OUT_DIR = ROOT / "prototype" / "assets" / "maker-products"
OUT_DIR.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
}
TIMEOUT = (4, 6)  # (connect, read) 短めにしてハング回避
HEAD_TIMEOUT = (3, 4)
DL_TIMEOUT = (4, 8)

# 製品っぽいページに繋がる「アンカーテキスト or path 断片」
PRODUCT_LINK_HINTS = [
    "products", "product", "catalog", "lineup", "items",
    "製品", "商品", "ラインナップ", "カタログ", "シリーズ",
]
# アイコン/装飾と判定する URL パターン (除外)
ICON_PATTERNS = re.compile(
    r"(logo|icon|favicon|btn|banner|bg[-_]|header|footer|spacer|blank|noimage|placeholder|sprite|"
    r"fallback|/top[_/-]|/top\.|_top[_.]|index[_.]|hero|keyvisual|mainvisual|/mv[_/.]|/kv[_/.]|"
    r"slide|slider|carousel|background|cover[_/.])",
    re.IGNORECASE,
)
# 製品ページ的 URL の優遇 (含まれていれば +score)
PRODUCT_URL_PATTERNS = re.compile(
    r"(products?/|items?/|catalog|goods/|lineup/|/p/|series|model)",
    re.IGNORECASE,
)
MIN_BYTES = 30 * 1024  # 30KB (実製品画像は通常 50KB+、バナーは大抵 <30KB か >2MB)
MAX_BYTES = 3 * 1024 * 1024  # 3MB (横長バナー除外)


def load_brand() -> dict:
    with open(BRAND_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def load_products() -> dict:
    if not PRODUCTS_PATH.exists():
        return {"_doc": ""}
    with open(PRODUCTS_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_maker_names() -> dict[str, str]:
    """makers.csv → {zero-padded No: name} を返す。"""
    import csv
    with open(MAKERS_CSV, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return {f"{int(r['no']):03d}": r["name"] for r in rows}


def absolute(base: str, src: str) -> str:
    """相対 URL を絶対化。// 始まりは https: 補完。"""
    if not src:
        return ""
    if src.startswith("//"):
        return "https:" + src
    return urljoin(base, src)


def is_likely_product_image(url: str) -> bool:
    if not url:
        return False
    if not re.search(r"\.(jpe?g|png|webp)(\?|$)", url, re.IGNORECASE):
        return False
    if ICON_PATTERNS.search(url):
        return False
    return True


def fetch_html(url: str) -> str | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code != 200:
            return None
        # 文字化け対策: r.encoding を charset から推定し直す
        if not r.encoding or r.encoding.lower() == "iso-8859-1":
            r.encoding = r.apparent_encoding
        return r.text
    except requests.RequestException:
        return None


def extract_candidates(html: str, base_url: str) -> list[tuple[str, str]]:
    """HTML から (image_url, alt_or_name) 候補を返す。優先順位ソート済。"""
    soup = BeautifulSoup(html, "html.parser")
    out: list[tuple[str, str, int]] = []  # (url, name, priority_score)

    is_product_page = bool(PRODUCT_URL_PATTERNS.search(base_url))

    # 1) og:image (製品ページ由来の場合のみ優先。トップページ由来はコーポレートヒーロー扱いで低)
    for meta in soup.find_all("meta", attrs={"property": ["og:image", "og:image:url"]}):
        url = absolute(base_url, meta.get("content", ""))
        if is_likely_product_image(url):
            score = 100 if is_product_page else 30
            out.append((url, meta.get("alt") or "Hero", score))

    # 2) <link rel="image_src">
    for link in soup.find_all("link", rel=lambda v: v and "image_src" in (v if isinstance(v, list) else [v])):
        url = absolute(base_url, link.get("href", ""))
        if is_likely_product_image(url):
            out.append((url, "image_src", 90 if is_product_page else 25))

    # 3) <img> 全部 (src / data-src / data-original)
    for img in soup.find_all("img"):
        for attr in ("src", "data-src", "data-original", "data-lazy-src"):
            raw = img.get(attr, "")
            if raw:
                break
        else:
            continue
        url = absolute(base_url, raw)
        if not is_likely_product_image(url):
            continue
        alt = (img.get("alt") or img.get("title") or "").strip()
        # サイズヒント (widthが大きいほど高優先)
        try:
            w = int(img.get("width") or 0)
        except ValueError:
            w = 0
        score = 50
        if w >= 400:
            score = 80
        elif w >= 200:
            score = 60
        # 製品ページ的 URL ボーナス (画像URL自体に products/items/catalog 等)
        if PRODUCT_URL_PATTERNS.search(url):
            score += 25
        # 製品ページ由来の画像 (source page が product 系) は加点
        if is_product_page:
            score += 15
        # _s/_thumb など縮小版は減点
        if re.search(r"(_s|_thumb|_small|_mini)\b", url, re.IGNORECASE):
            score -= 20
        # 型番 (アルファ+数字混在 4文字以上) を含むファイル名はボーナス
        filename = url.rsplit("/", 1)[-1].split("?")[0]
        if re.search(r"[A-Z][A-Z0-9_-]{2,}\d|[A-Z]+[\-_]?\d{2,}", filename):
            score += 30
        out.append((url, alt or "Product", score))

    # 重複除外 (URLベース)、スコア降順
    seen = {}
    for url, name, score in out:
        if url not in seen or seen[url][1] < score:
            seen[url] = (name, score)
    sorted_items = sorted(seen.items(), key=lambda kv: -kv[1][1])
    return [(url, name) for url, (name, _) in sorted_items]


def discover_product_pages(html: str, base_url: str, limit: int = 5) -> list[str]:
    """製品一覧/ラインナップへのリンク URL を返す (最大 limit 個)。"""
    soup = BeautifulSoup(html, "html.parser")
    candidates: list[tuple[str, int]] = []
    for a in soup.find_all("a", href=True):
        href = absolute(base_url, a["href"])
        if not href.startswith(("http://", "https://")):
            continue
        # 同一ホストのみ (外部リンク除外)
        if urlparse(href).netloc != urlparse(base_url).netloc:
            continue
        path_lc = (urlparse(href).path + " " + (a.get_text() or "")).lower()
        score = sum(1 for h in PRODUCT_LINK_HINTS if h.lower() in path_lc)
        if score >= 1:
            candidates.append((href, score))
    seen = {}
    for url, score in candidates:
        if url not in seen or seen[url] < score:
            seen[url] = score
    return [u for u, _ in sorted(seen.items(), key=lambda kv: -kv[1])][:limit]


def head_check(url: str) -> tuple[bool, str, int]:
    """(ok, content_type, content_length) を返す。"""
    try:
        r = requests.head(url, headers=HEADERS, timeout=HEAD_TIMEOUT, allow_redirects=True)
        if r.status_code != 200:
            return False, "", 0
        ct = r.headers.get("content-type", "").split(";")[0].strip().lower()
        cl = int(r.headers.get("content-length", "0") or 0)
        if not ct.startswith("image/"):
            return False, ct, cl
        return True, ct, cl
    except (requests.RequestException, ValueError):
        return False, "", 0


def download_image(url: str, dest: Path) -> int:
    try:
        r = requests.get(url, headers=HEADERS, timeout=DL_TIMEOUT, stream=True)
        if r.status_code != 200:
            return 0
        dest.parent.mkdir(parents=True, exist_ok=True)
        size = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                size += len(chunk)
                if size > MAX_BYTES:  # 巨大画像は途中で打ち切り
                    break
        return size
    except requests.RequestException:
        return 0


def ext_for(content_type: str, url: str) -> str:
    ct = content_type.lower()
    if "jpeg" in ct or "jpg" in ct:
        return "jpg"
    if "png" in ct:
        return "png"
    if "webp" in ct:
        return "webp"
    if "gif" in ct:
        return "gif"
    # fallback: URL 末尾
    m = re.search(r"\.(jpe?g|png|webp|gif)(?:\?|$)", url, re.IGNORECASE)
    if m:
        return m.group(1).lower().replace("jpeg", "jpg")
    return "jpg"


def fetch_for_maker(no: str, name: str, source, max_images: int = 4, dry: bool = False) -> dict:
    """単一メーカーの製品画像を取得。fetched_ok=true ならローカル保存済。

    source は str (単一URL) または list[str] (複数製品ページ) 両対応。
    list の場合は各URLが「製品ページ直」前提で discover をスキップ、各URLから最大2枚ずつ。
    """
    # source を list に正規化
    if isinstance(source, list):
        source_urls = [s for s in source if s]
        is_multi = True
    else:
        source_urls = [source] if source else []
        is_multi = False

    label = f"{len(source_urls)} URLs" if is_multi else (source_urls[0] if source_urls else "<no source>")
    print(f"\n=== {no} {name} ({label}) ===")
    if not source_urls:
        return {"name": name, "products": [], "fetched_ok": False, "skip_reason": "no source URL"}

    # 複数URL指定時は各URLから2枚ずつを目安に最大6枚
    if is_multi:
        max_images = min(6, max(max_images, len(source_urls) * 2))

    pages_to_scan: list[tuple[str, str]] = []
    for i, src_url in enumerate(source_urls, 1):
        if is_multi:
            print(f"  [URL {i}/{len(source_urls)}] {src_url}")
        html = fetch_html(src_url)
        if not html:
            if is_multi:
                print(f"    fetch failed")
            continue
        pages_to_scan.append((src_url, html))
        # 単一source の場合のみ discover で補完
        if not is_multi:
            for sub in discover_product_pages(html, src_url, limit=4):
                time.sleep(1.2)
                sub_html = fetch_html(sub)
                if sub_html:
                    pages_to_scan.append((sub, sub_html))

    if not pages_to_scan:
        joined = source_urls[0] if not is_multi else f"{len(source_urls)} URLs"
        return {"name": name, "products": [], "fetched_ok": False, "skip_reason": f"fetch failed: {joined}"}

    print(f"  scanned pages: {len(pages_to_scan)}")
    candidates: list[tuple[str, str, str]] = []  # (url, name, source_page)
    for src, body in pages_to_scan:
        for url, alt in extract_candidates(body, src):
            candidates.append((url, alt, src))

    # 重複除外 + スコア再計算 (PRODUCT_URL_PATTERNS / 型番パターン / 装飾URL除外を厳密に)
    def rescore(url: str, src: str) -> int:
        s = 50
        if PRODUCT_URL_PATTERNS.search(url):
            s += 30
        if PRODUCT_URL_PATTERNS.search(src):
            s += 15
        filename = url.rsplit("/", 1)[-1].split("?")[0]
        if re.search(r"[A-Z][A-Z0-9_-]{2,}\d|[A-Z]+[\-_]?\d{2,}", filename):
            s += 30
        if re.search(r"(_s|_thumb|_small|_mini)\b", url, re.IGNORECASE):
            s -= 25
        if re.search(r"(top|index|hero|main|key|mv|kv|slide|banner|cover|fallback)", url, re.IGNORECASE):
            s -= 30
        return s

    seen_urls = set()
    uniq = []
    for url, alt, src in candidates:
        if url in seen_urls:
            continue
        seen_urls.add(url)
        uniq.append((rescore(url, src), url, alt, src))
    uniq.sort(key=lambda x: -x[0])
    # 上位 30 件だけを HEAD 検証 (そこで 4 枚揃わなければあきらめ)
    uniq = [(u, a, s) for _, u, a, s in uniq[:30]]
    print(f"  candidate images: {len(uniq)} (top 30 filtered)")

    if dry:
        for url, alt, src in uniq[:8]:
            print(f"    {url}  ({alt[:30]})")
        return {"name": name, "products": [], "fetched_ok": False, "skip_reason": "dry run"}

    # 既存出力を一度クリア (再生成時の重複防止)
    out_dir = OUT_DIR / no
    if out_dir.exists():
        for old in out_dir.glob("*"):
            old.unlink()

    # 複数URL時は各 source_page から最大2枚で偏り防止
    per_source_max = 2 if is_multi else max_images
    src_counts: dict[str, int] = {}

    selected: list[dict] = []
    for url, alt, src in uniq:
        if len(selected) >= max_images:
            break
        if src_counts.get(src, 0) >= per_source_max:
            continue
        ok, ct, cl = head_check(url)
        if not ok:
            continue
        if cl and cl < MIN_BYTES:
            continue
        if cl and cl > MAX_BYTES:
            continue
        idx = len(selected) + 1
        ext = ext_for(ct, url)
        dest = out_dir / f"{idx}.{ext}"
        size = download_image(url, dest)
        if size < MIN_BYTES or size > MAX_BYTES:
            if dest.exists():
                dest.unlink()
            continue
        # アスペクト比チェック: 横長すぎ (>2.4:1) はバナー扱いで除外
        try:
            from PIL import Image
            with Image.open(dest) as im:
                w, h = im.size
                if h > 0 and (w / h) > 2.4:
                    dest.unlink()
                    continue
                if w < 300 or h < 200:
                    dest.unlink()
                    continue
        except Exception:
            pass  # PIL 読込失敗時は素通し (壊れた画像は後で気づく)
        local_url = f"../../assets/maker-products/{no}/{idx}.{ext}"
        selected.append({
            "name": alt[:80] if alt else f"{name} 製品 {idx}",
            "category": "",
            "image_url": local_url,
            "source_page": src,
            "remote_url": url,
            "bytes": size,
        })
        src_counts[src] = src_counts.get(src, 0) + 1
        print(f"  + {idx}.{ext} ({size:,} bytes, {ct})  ← {url[:80]}")
        time.sleep(0.5)

    if not selected:
        return {"name": name, "products": [], "fetched_ok": False, "skip_reason": "no valid images found"}

    return {"name": name, "products": selected, "fetched_ok": True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="特定の maker_no (例 082) だけ。space 区切りで複数可")
    ap.add_argument("--force", action="store_true", help="既存 fetched_ok=true でも上書き")
    ap.add_argument("--dry", action="store_true", help="取得せず候補だけ表示")
    args = ap.parse_args()

    brand = load_brand()
    products = load_products()
    names = load_maker_names()

    if args.only:
        targets = [s.strip().zfill(3) for s in args.only.split() if s.strip()]
    else:
        # ターゲット: brand あり、かつ (products 未登録 or fetched_ok=false)
        targets = []
        for k in sorted(brand.keys()):
            rec = products.get(k)
            if not rec or not rec.get("fetched_ok"):
                targets.append(k)

    print(f"対象 ({len(targets)}社): {' '.join(targets)}")

    ok_count, fail_count = 0, 0
    failures: list[tuple[str, str]] = []
    for no in targets:
        # --force でなければ既存 fetched_ok=true をスキップ
        if not args.force and products.get(no, {}).get("fetched_ok"):
            print(f"\n=== {no} (既存 OK、skip) ===")
            continue
        name = names.get(no, brand.get(no, {}).get("name", "unknown"))
        source = brand.get(no, {}).get("source", "")
        result = fetch_for_maker(no, name, source, dry=args.dry)
        if not args.dry:
            products[no] = result
        if result.get("fetched_ok"):
            ok_count += 1
        else:
            fail_count += 1
            failures.append((no, result.get("skip_reason", "")))
        time.sleep(1.0)

    if not args.dry:
        with open(PRODUCTS_PATH, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"\nWrote: {PRODUCTS_PATH.relative_to(ROOT)}")

    print(f"\n=== サマリ ===")
    print(f"  成功: {ok_count}")
    print(f"  失敗: {fail_count}")
    if failures:
        print(f"  失敗内訳:")
        for no, reason in failures:
            print(f"    {no}: {reason}")


if __name__ == "__main__":
    sys.exit(main() or 0)
