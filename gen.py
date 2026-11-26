import os, html, json, shutil, sys
from posts import POSTS
SITE = "Kitten Paw Tutorials"
TAGLINE = "ゲーム・ガジェットのエラーと使い方を、わかりやすく解説"
BASE = os.environ.get("BASE", "https://kilillan.github.io/kittenpaw-blog")
PREFIX = os.environ.get("PREFIX", "/kittenpaw-blog")
YT = "https://www.youtube.com/channel/UCmqBViCbHVO3VVQsvNC_8jw"
OUT = "site"
CATS = ["GTA6", "PS5", "Ray-Ban Meta", "Windows"]
CSLUG = {"GTA6": "gta6", "PS5": "ps5", "Ray-Ban Meta": "rayban-meta", "Windows": "windows"}
DISCLOSE = "※本記事には広告（アフィリエイトリンク）が含まれます"
AMZNOTE = "Amazonのアソシエイトとして、Kitten Paw Tutorialsは適格販売により収入を得ています。"
e = html.escape

CSS = """*{box-sizing:border-box}body{margin:0;font-family:"Hiragino Sans","Noto Sans JP","Yu Gothic",sans-serif;background:#f4f0e9;color:#181716;line-height:1.85}
a{color:#9a6b2f}header{background:#181716;color:#fff}header .in,main,footer .in{max-width:860px;margin:0 auto;padding:0 20px}
header .in{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;padding:18px 20px}
header a.logo{color:#fff;text-decoration:none;font-weight:800;font-size:22px;letter-spacing:.02em}header a.logo span{color:#b88a48}
nav a{color:#ddd;text-decoration:none;margin-left:14px;font-size:14px}nav a:hover{color:#b88a48}
.tag{font-size:13px;color:#bbb;margin:0}main{padding-top:28px;padding-bottom:40px}
.card{display:block;background:#fff;border:1px solid #d6cec2;border-radius:16px;padding:20px 22px;margin:0 0 16px;text-decoration:none;color:#181716;transition:transform .15s}
.card:hover{transform:translateY(-2px);border-color:#b88a48}.card h2{font-size:19px;margin:6px 0 6px;line-height:1.5}.card p{margin:0;color:#6e665c;font-size:14px}
.cat{display:inline-block;font-size:12px;font-weight:700;background:#181716;color:#fff;border-radius:20px;padding:2px 12px}.date{font-size:12px;color:#8a8275;margin-left:8px}
article{background:#fff;border:1px solid #d6cec2;border-radius:18px;padding:28px 30px}article h1{font-size:26px;line-height:1.5;margin:10px 0 8px}
article h2{font-size:20px;border-left:6px solid #b88a48;padding-left:12px;margin:34px 0 10px}.disc{font-size:13px;color:#8a8275;margin:0 0 14px}
.summary{background:#faf6ee;border:1px solid #e6dccb;border-radius:14px;padding:16px 18px;margin:16px 0}.summary b{color:#9a6b2f}
.items{display:grid;gap:12px;margin:18px 0}.item{display:flex;justify-content:space-between;align-items:center;gap:12px;border:1px solid #d6cec2;border-radius:14px;padding:14px 16px;background:#fffdf9}
.item .n{font-weight:700}.item .s{font-size:13px;color:#8a8275}.btn{flex-shrink:0;background:#ff9900;color:#181716;font-weight:800;text-decoration:none;border-radius:24px;padding:9px 18px;font-size:14px}
.yt{display:inline-block;margin-top:24px;background:#e2403a;color:#fff;text-decoration:none;font-weight:800;border-radius:24px;padding:10px 20px}
footer{background:#181716;color:#aaa;font-size:13px;padding:24px 0;margin-top:30px}footer a{color:#ddd}
ol,ul{padding-left:1.4em}li{margin:4px 0}@media(max-width:600px){article{padding:20px 18px}article h1{font-size:22px}.item{flex-direction:column;align-items:flex-start}}"""

def page(title, desc, body, path, canonical_type="website", extra_head=""):
    url = BASE + path
    nav = "".join(f'<a href="{PREFIX}/category/{CSLUG[c]}/">{e(c)}</a>' for c in CATS)
    return f"""<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="{canonical_type}"><meta property="og:url" content="{url}">
<link rel="stylesheet" href="{PREFIX}/style.css">{extra_head}</head><body>
<header><div class="in"><div><a class="logo" href="{PREFIX}/">Kitten Paw <span>Tutorials</span></a><p class="tag">{e(TAGLINE)}</p></div><nav>{nav}</nav></div></header>
<main>{body}</main>
<footer><div class="in"><p>{e(AMZNOTE)}</p><p><a href="{PREFIX}/about/">このサイトについて</a> ・ <a href="{PREFIX}/privacy/">プライバシーポリシー</a> ・ <a href="{YT}" rel="noopener">YouTubeチャンネル</a></p><p>© 2026 {e(SITE)}</p></div></footer></body></html>"""

def md(src):
    out = []; lst = None
    def close():
        nonlocal lst
        if lst: out.append(f"</{lst}>"); lst = None
    for line in src.strip().split("\n"):
        line = line.rstrip()
        if line.startswith("## "): close(); out.append(f"<h2>{e(line[3:])}</h2>")
        elif line.startswith("- "):
            if lst != "ul": close(); out.append("<ul>"); lst = "ul"
            out.append(f"<li>{e(line[2:])}</li>")
        elif len(line) > 2 and line[0].isdigit() and line[1:3] == ". ":
            if lst != "ol": close(); out.append("<ol>"); lst = "ol"
            out.append(f"<li>{e(line[3:])}</li>")
        elif line: close(); out.append(f"<p>{e(line)}</p>")
    close(); return "\n".join(out)

def items_html(items):
    rows = "".join(f'<div class="item"><div><div class="n">{e(n)}</div><div class="s">{e(note)}</div></div><a class="btn" href="{e(u)}" rel="nofollow sponsored noopener" target="_blank">Amazonで見る</a></div>' for n, u, note in items)
    return f'<h2>おすすめアイテム</h2><div class="items">{rows}</div>'

def card(p):
    return f'<a class="card" href="{PREFIX}/posts/{p["slug"]}/"><span class="cat">{e(p["cat"])}</span><span class="date">{p["date"]}</span><h2>{e(p["title"])}</h2><p>{e(p["desc"])}</p></a>'

def write(path, content):
    fp = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith((".xml", ".txt", ".css")) else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, "w").write(content)

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
posts = sorted(POSTS, key=lambda p: p["date"], reverse=True)
write("/style.css", CSS); open(os.path.join(OUT, ".nojekyll"), "w").write("")
import shutil, glob
for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "*")): shutil.copy(f, OUT)
for p in posts:
    path = f"/posts/{p['slug']}/"
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "datePublished": p["date"], "dateModified": p["date"], "description": p["desc"], "author": {"@type": "Organization", "name": SITE}}, ensure_ascii=False)
    body = f"""<article><span class="cat">{e(p["cat"])}</span><span class="date">{p["date"]}</span><h1>{e(p["title"])}</h1>
<p class="disc">{e(DISCLOSE)}</p><div class="summary"><b>結論：</b>{e(p["summary"])}</div>
{items_html(p["items"][:1])}
{md(p["body"])}
{items_html(p["items"])}
<p>直らない場合や、どの方法で直ったかは、YouTubeのコメント欄で教えてください。</p>
<a class="yt" href="{YT}" rel="noopener" target="_blank">▶ 動画で見る（YouTube）</a></article>"""
    write(path, page(f'{p["title"]} | {SITE}', p["desc"], body, path, "article", f'<script type="application/ld+json">{ld}</script>'))
write("/", page(f"{SITE} | {TAGLINE}", TAGLINE + "。GTA6、PS5、Ray-Ban Meta、Windowsのトラブル解決ガイド。", f'<p class="disc">{e(DISCLOSE)}</p>' + "".join(card(p) for p in posts), "/"))
for c in CATS:
    ps = [p for p in posts if p["cat"] == c]
    write(f"/category/{CSLUG[c]}/", page(f"{c}の記事一覧 | {SITE}", f"{c}のエラーや使い方の解説記事一覧。", f"<h1>{e(c)}</h1>" + "".join(card(p) for p in ps), f"/category/{CSLUG[c]}/"))
about = f"""<article><h1>このサイトについて</h1><p>Kitten Paw Tutorialsは、ゲーム機・PC・ガジェットのエラーや使い方を、わかりやすく解説するサイトです。YouTubeチャンネル「Kitten Paw Tutorials」と連動して、動画の内容を記事でも確認できるようにしています。</p>
<p>記事の内容は、各メーカーの公式サポート情報などをもとに作成していますが、最新の状況と異なる場合があります。お使いの機器の公式サポートもあわせてご確認ください。</p><p>{e(AMZNOTE)}</p></article>"""
write("/about/", page(f"このサイトについて | {SITE}", "Kitten Paw Tutorialsについて", about, "/about/"))
privacy = f"""<article><h1>プライバシーポリシー</h1><h2>広告について</h2><p>当サイトは、Amazonアソシエイト・プログラムなどのアフィリエイトプログラムに参加しています。また、今後Google AdSenseなどの第三者配信の広告サービスを利用する場合があります。広告配信事業者は、ユーザーの興味に応じた広告を表示するためにCookieを使用することがあります。</p>
<p>{e(AMZNOTE)}</p><h2>アクセス解析について</h2><p>当サイトでは、サイトの改善のためにアクセス解析ツールを利用する場合があります。これらのツールはCookieを使用してデータを収集しますが、個人を特定する情報は含まれません。</p>
<h2>免責事項</h2><p>当サイトの情報はできるかぎり正確に提供するよう努めていますが、内容の正確性や安全性を保証するものではありません。当サイトの情報を利用したことによる損害について、一切の責任を負いかねます。</p>
<h2>お問い合わせ</h2><p>お問い合わせは、<a href="{YT}">YouTubeチャンネル</a>のコメント欄からお願いします。</p><p>制定日：2026年11月26日</p></article>"""
write("/privacy/", page(f"プライバシーポリシー | {SITE}", "Kitten Paw Tutorialsのプライバシーポリシー", privacy, "/privacy/"))
urls = ["/", "/about/", "/privacy/"] + [f"/category/{CSLUG[c]}/" for c in CATS] + [f"/posts/{p['slug']}/" for p in posts]
write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc></url>" for u in urls) + "</urlset>")
write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
print("pages", len(urls))
