#!/usr/bin/env python3
"""病院の公式サイト（小児不整脈部門「アブレーション治療の成績」）へ渡すデータセットを作る。
個人サイトの4ページ（ablation / wpw_results / pvc_results / avnrt_results）の本文を取り出し、
白背景・Noto Sans JP・病院の青に合わせたテンプレートに入れ直す。外部依存はフォントだけ。"""
import re, shutil, zipfile
from pathlib import Path

SITE = Path('/Users/tsugu/tsuguszk.github.io')
OUT = Path('/Users/tsugu/Library/CloudStorage/GoogleDrive-tsugutoshi@gmail.com/マイドライブ/dropbox_Google/AI_workspace/260626website改編/病院サイト用_アブレーション治療の成績')
UPDATED = '2026年9月26日'
PAGES = [  # (個人サイトのファイル, 病院用のファイル, タブ名, ページ名)
    ('ablation.html', 'index.html', '全体', 'アブレーション治療の成績'),
    ('wpw_results.html', 'wpw.html', 'WPW', 'WPWのアブレーション治療の成績'),
    ('avnrt_results.html', 'avnrt.html', 'AVNRT', 'AVNRTのアブレーション治療の成績'),
    ('pvc_results.html', 'pvc.html', 'PVC/NSVT', 'PVC/NSVTのアブレーション治療の成績'),
]
LINKMAP = {src: dst for src, dst, _, _ in PAGES}
KATO = 'https://pubmed.ncbi.nlm.nih.gov/31415819/'

if OUT.exists():
    shutil.rmtree(OUT)
(OUT / 'images').mkdir(parents=True)
(OUT / 'fragments').mkdir()

# ---------- 写真（webp と jpg の両方）
shutil.copy(SITE / 'assets/media/ablation-room.webp', OUT / 'images/ablation-room.webp')
try:
    from PIL import Image
    Image.open(SITE / 'assets/media/ablation-room.webp').convert('RGB').save(OUT / 'images/ablation-room.jpg', quality=88)
except ImportError:
    pass

# ---------- CSS：ca.css の .nx を .ocgh-abl に置き換え、白背景の基本部品を足す
ca = (SITE / 'assets/ca.css').read_text(encoding='utf-8')
ca = ca.replace('.nx-js .nx [data-reveal]:not(.is-in) ', '.ocgh-abl .reveal-off ')  # 表示アニメーションは使わない
ca = re.sub(r'\.nx(?=[ .:{,])', '.ocgh-abl', ca)
ca = ca.replace('--p1: #e3a07c; --p2: #d27a45; --p3: #c4581c;', '--p1: #a9d2f5; --p2: #58a9ee; --p3: #0b78d8;')
ca = ca.replace('--c-l: #c4581c; --c-s: #e0a526; --c-r: #2a8c7c;', '--c-l: #0b78d8; --c-s: #f0a92b; --c-r: #2aa58c;')
ca = ca.replace('--c-ok: #2a8c7c; --c-re: #c4581c; --c-rest: #e4ded5;', '--c-ok: #2aa58c; --c-re: #e2762e; --c-rest: #e6ebf0;')
ca = ca.replace('--c-rf: #c4581c; --c-cryo: #3d8fd1;', '--c-rf: #e2762e; --c-cryo: #3fa9f5;')
ca = ca.replace('--c-g1: #c4581c; --c-g2: #2a8c7c;', '--c-g1: #0b78d8; --c-g2: #2aa58c;')
ca = ca.replace('.ocgh-abl .ca-kpi--all { background: #fff4ec; box-shadow: inset 0 0 0 2px rgba(196, 88, 28, .35); }',
                '.ocgh-abl .ca-kpi--all { background: #eef6fe; box-shadow: inset 0 0 0 2px rgba(11, 120, 216, .35); }')
ca = re.sub(r'/\* このページ群はナビが5項目.*?\n}\n', '', ca, flags=re.S)
base = '''/* 大阪市立総合医療センター 小児不整脈部門「アブレーション治療の成績」
   すべての指定は .ocgh-abl の中だけに効きます（病院サイトの他の部分に影響しません）。
   文字は病院サイトと同じ Noto Sans JP。サイト側で読み込み済みなら、HTML の Google Fonts の行は消してかまいません。 */
.ocgh-abl {
  --ink: #1a1a1a; --ink-2: #333; --muted: #666; --line: #dde3ea; --accent: #0b78d8; --link: #2c6ea7; --gutter: 16px;
  color: var(--ink); background: #fff; font-family: "Noto Sans JP", "Hiragino Sans", "Hiragino Kaku Gothic ProN", Meiryo, sans-serif;
  font-size: 16px; line-height: 1.8; -webkit-text-size-adjust: 100%;
}
.ocgh-abl *, .ocgh-abl *::before, .ocgh-abl *::after { box-sizing: border-box; }
.ocgh-abl img { max-width: 100%; height: auto; }
.ocgh-abl a { color: var(--link); }
.ocgh-abl a:hover { text-decoration: none; }
.ocgh-abl h1, .ocgh-abl h2, .ocgh-abl h3 { margin: 0; line-height: 1.4; color: var(--ink); }
.ocgh-abl p { margin: 0 0 1em; }

/* 4ページの切り替えタブ */
.ocgh-abl .abl-tabs { display: flex; flex-wrap: wrap; gap: 6px; max-width: 960px; margin: 0 auto; padding: 16px var(--gutter) 0; }
.ocgh-abl .abl-tabs a { padding: 6px 16px; border: 1px solid var(--line); border-radius: 999px; color: var(--ink); font-size: .9rem; font-weight: 700; text-decoration: none; }
.ocgh-abl .abl-tabs a:hover { border-color: var(--accent); color: var(--accent); }
.ocgh-abl .abl-tabs a[aria-current="page"] { border-color: transparent; background: linear-gradient(90deg, #0b78d8, #58a9ee); color: #fff; }

/* 冒頭 */
.ocgh-abl .page-hero { max-width: 960px; margin: 0 auto; padding: 24px var(--gutter) 28px; }
.ocgh-abl .eyebrow { margin: 0 0 6px; color: var(--accent); font-size: .8rem; font-weight: 700; letter-spacing: .08em; }
.ocgh-abl .eyebrow a { color: var(--accent); }
.ocgh-abl .page-hero h1 { font-size: clamp(1.6rem, 1.2rem + 1.8vw, 2.3rem); font-weight: 700; }
.ocgh-abl .sec-lede { margin: 14px 0 0; color: var(--ink-2); }
.ocgh-abl .jump { display: flex; flex-wrap: wrap; gap: 6px 8px; margin-top: 16px; }
.ocgh-abl .jump a { padding: 3px 12px; border-radius: 999px; background: #eef6fe; color: var(--link); font-size: .86rem; text-decoration: none; }
.ocgh-abl .jump a:hover { background: #dcecfc; }

/* 本文のカード */
.ocgh-abl .doc { display: grid; gap: 28px; max-width: 960px; margin: 0 auto; padding: 0 var(--gutter) 40px; }
.ocgh-abl .doc-card { padding: 0; }
.ocgh-abl .doc-card > h2 { margin-bottom: 14px; padding: 8px 16px; background: linear-gradient(90deg, #0b78d8, #58a9ee); color: #fff; font-size: 1.15rem; font-weight: 700; }
.ocgh-abl .doc-card h3 { margin: 22px 0 8px; padding-left: 10px; border-left: 4px solid var(--accent); font-size: 1.02rem; font-weight: 700; }
.ocgh-abl .doc-card > p, .ocgh-abl .doc-card li { color: var(--ink-2); }
.ocgh-abl .doc-note { margin: 16px 0 0; padding: 12px 16px; border-left: 4px solid var(--accent); background: #f4f8fc; color: var(--ink-2); font-size: .95rem; }
.ocgh-abl .doc-links { display: grid; gap: 8px; margin: 12px 0 0; padding: 0; list-style: none; }
.ocgh-abl .doc-links a { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border: 1px solid var(--line); border-radius: 10px; color: var(--ink); font-weight: 700; text-decoration: none; }
.ocgh-abl .doc-links a::after { content: "›"; margin-left: auto; color: var(--accent); font-size: 1.3rem; line-height: 1; }
.ocgh-abl .doc-links a:hover { border-color: var(--accent); }
.ocgh-abl .doc-links small { display: block; color: var(--muted); font-size: .82rem; font-weight: 400; }
.ocgh-abl .doc-table { width: 100%; margin: 12px 0 0; border-collapse: collapse; font-size: .93rem; }
.ocgh-abl .doc-table th, .ocgh-abl .doc-table td { padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
.ocgh-abl .doc-table thead th { background: #f4f8fc; }
.ocgh-abl .doc-table th { color: var(--ink); font-weight: 700; white-space: nowrap; }
.ocgh-abl .doc-table td { color: var(--ink-2); }
.ocgh-abl .doc-scroll { overflow-x: auto; }
.ocgh-abl .abl-foot { max-width: 960px; margin: 0 auto; padding: 16px var(--gutter) 32px; border-top: 1px solid var(--line); color: var(--muted); font-size: .85rem; }
.ocgh-abl [hidden] { display: none !important; }

'''
css = base + ca + '''
/* スマホでは見出しを1行に収める */
@media (max-width: 480px) { .ocgh-abl .page-hero.ca-hero h1 { font-size: 1.45rem; } .ocgh-abl .page-hero.ca-hero h1 .h1-sub { font-size: .72em; } }
'''
(OUT / 'ablation-results.css').write_text(css, encoding='utf-8')

js = (SITE / 'assets/ca.js').read_text(encoding='utf-8').replace("'.nx .ca-plot'", "'.ocgh-abl .ca-plot'")
(OUT / 'ablation-results.js').write_text(js, encoding='utf-8')


# ---------- 本文を取り出して病院向けに直す
def convert(html, src):
    main = re.search(r'<main>(.*)</main>', html, re.S).group(1)
    main = re.sub(r' data-reveal(="\d")?', '', main)
    # 冒頭の写真（拡大ボタンをやめて、ただの写真に）
    main = re.sub(r'<figure class="ca-hero-photo">.*?</figure>',
                  '<figure class="ca-hero-photo"><picture><source srcset="images/ablation-room.webp" type="image/webp"><img src="images/ablation-room.jpg" width="1159" height="768" alt="カテーテル室でアブレーション治療をしている様子（モニターの患者情報はぼかしています）"></picture></figure>', main, flags=re.S)
    # 個人サイト向けの書き方を病院向けに
    rep = [
        ('2006年に大阪市立総合医療センター 小児不整脈科に赴任してから2026年9月までに、当科で行った', '当科（小児不整脈部門）で2006年から2026年9月までに行った'),
        ('2006年に大阪市立総合医療センター 小児不整脈科に赴任してから、2026年までの20年間に当科で行った', '当科（小児不整脈部門）で2006年から2026年までの20年間に行った'),
        ('<span class="nw">アブレーションの仕事</span><span class="h1-sub">全症例のデータ（2006–2026年）</span>', '<span class="nw">アブレーション治療の成績</span><span class="h1-sub">全症例のデータ（2006–2026年）</span>'),
        ('<a href="ablation.html">アブレーションの仕事</a> ›', '<a href="index.html">アブレーション治療の成績</a> ›'),
        ('<a href="ablation.html">アブレーション全体のデータ</a>もご覧ください。', '<a href="index.html">アブレーション治療全体の成績</a>もご覧ください。'),
        ('潜在性は、右側が少ない、というデータです。あまり知られていないデータだと思います。', '潜在性では、右側の副伝導路が少ないという結果でした。'),
        ('（<a href="index_kato_paper.html">論文のページへ</a>）', f'（<a href="{KATO}">Heart Rhythm 2020;17:49–55（PubMed）</a>）'),
    ]
    for a, b in rep:
        main = main.replace(a, b)
    # 関連ページ：個人サイトの論文紹介・説明資料は論文へのリンクに置き換え
    main = re.sub(r'<li><a href="index_kato_paper.html">.*?</a></li>',
                  f'<li><a href="{KATO}"><span>1000例の治療成績の論文（Heart Rhythm 2020）<small>当院で2006〜2018年に行った小児のアブレーション治療1021件の成績（PubMed）</small></span></a></li>', main, flags=re.S)
    main = re.sub(r'\s*<li><a href="page_rfca/rfca_manual.html">.*?</a></li>', '', main, flags=re.S)
    main = main.replace('<span>アブレーションの仕事（全症例のデータ）<small>', '<span>アブレーション治療の成績（全症例のデータ）<small>')
    main = main.replace('<span>アブレーションの仕事<small>', '<span>アブレーション治療の成績<small>')
    for s, d in LINKMAP.items():
        main = main.replace(f'href="{s}', f'href="{d}')
    left = re.findall(r'href="(?!https?:|#|index\.html|wpw\.html|pvc\.html|avnrt\.html)([^"]+)"', main)
    assert not left, (src, left)
    assert 'assets/' not in main, src
    return main


for src, dst, tab, title in PAGES:
    html = (SITE / src).read_text(encoding='utf-8')
    body = convert(html, src)
    tabs = '\n'.join(f'    <a href="{d}"{" aria-current=\"page\"" if d == dst else ""}>{t}</a>' for _, d, t, _ in PAGES)
    frag = f'''<div class="ocgh-abl">
  <nav class="abl-tabs" aria-label="アブレーション治療の成績のページ">
{tabs}
  </nav>
  <main>{body}</main>
  <p class="abl-foot">大阪市立総合医療センター 小児循環器・不整脈内科（小児不整脈部門）　データ更新日：{UPDATED}</p>
</div>
'''
    desc = re.search(r'<meta name="description" content="([^"]*)"', html).group(1).replace('アブレーションの仕事', 'アブレーション治療の成績')
    page = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{desc}">
  <title>{title} | 小児循環器・不整脈内科 | 大阪市立総合医療センター</title>
  <!-- 病院サイトで Noto Sans JP を読み込み済みなら、次の3行は不要です -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap">
  <link rel="stylesheet" href="ablation-results.css">
</head>
<body style="margin:0;background:#fff">
{frag}  <script src="ablation-results.js" defer></script>
</body>
</html>
'''
    (OUT / dst).write_text(page, encoding='utf-8')
    (OUT / 'fragments' / dst.replace('.html', '_本文.html')).write_text(frag, encoding='utf-8')

# ---------- 管理者向けの説明
readme = f'''# 小児不整脈部門「アブレーション治療の成績」ページ一式

大阪市立総合医療センター 小児循環器・不整脈内科（小児不整脈部門）
作成：鈴木嗣敏　データ更新日：{UPDATED}

## 内容

| ファイル | 内容 |
|---|---|
| index.html | アブレーション治療の成績（全体）：件数・成功率・再発率、年齢・体重の分布、不整脈ごとの成績 |
| wpw.html | WPW：副伝導路の位置・時期ごとの成績、高周波と冷凍、無症候性WPW |
| avnrt.html | AVNRT：通常型と非通常型、高周波と冷凍の比較 |
| pvc.html | PVC/NSVT：部位ごとの成績 |
| ablation-results.css | 見た目（4ページ共通）。すべて `.ocgh-abl` の中だけに効きます |
| ablation-results.js | 棒グラフにマウスを合わせたときの数値表示（なくてもページは表示されます） |
| images/ | 写真（webp と jpg） |
| fragments/ | 各ページの本文だけ（`<div class="ocgh-abl">…</div>`）。CMS に貼り付ける場合用 |

## 掲載のしかた（どちらか）

1. **このフォルダをそのまま置く**：4つの HTML・CSS・JS・images を同じフォルダに置けば、そのまま表示されます。ページ間のリンクは相対パスです。
2. **既存ページ（WordPress など）に埋め込む**：`fragments/*_本文.html` を本文に貼り付け、`ablation-results.css` と `ablation-results.js` を読み込んでください。画像のパス（`images/…`）とページ間のリンク（`index.html` など）は、置き場所に合わせて書き換えてください。

- グラフは HTML と CSS だけで描いています（画像やライブラリは不要）。
- スマートフォンの幅（375px）から PC まで確認しています。
- 外部から読み込むのは Google Fonts（Noto Sans JP）だけです。病院サイトで読み込み済みなら、HTML の該当3行は削除してかまいません。
- アクセス解析のタグは入れていません。

## データについて

- 当科のアブレーション治療データベースから、2006年1月1日〜{UPDATED}の治療記録を集計した数値です。
- ページに載っているのは集計値だけで、患者さんを特定できる情報は含みません。写真のモニターの患者情報はぼかしています。
- 毎年1回、数値を更新する予定です。更新時は、このフォルダ一式を差し替えます。

## 問い合わせ

小児循環器・不整脈内科（小児不整脈部門）　鈴木嗣敏
'''
(OUT / 'README_サイト管理者の方へ.md').write_text(readme, encoding='utf-8')

# ---------- zip
zp = OUT.parent / f'{OUT.name}.zip'
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.rglob('*')):
        if f.is_file() and f.name != '.DS_Store':
            z.write(f, Path(OUT.name) / f.relative_to(OUT))
print('ok', OUT, zp)
