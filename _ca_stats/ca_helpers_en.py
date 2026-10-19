# 英語版の成績ページ（ablation_en・wpw_results_en・avnrt_results_en・pvc_results_en）の共通部品。ca_helpers.py のあとに exec で読み込む
LOC_EN = {'左側': 'Left', '中隔': 'Septal', '右側': 'Right'}
TYPE_EN = {'顕性': 'Manifest', '間欠性': 'Intermittent', '潜在性': 'Concealed'}
TOPCLS = ' class="nav-top"'
EN_STYLE = '''  <style>
    /* 英語版：スマホではメニューの「Top」を隠し（ロゴでトップへ戻れる）、入りきらないときは横にスクロールさせる */
    @media (max-width: 599px) {
      .nx .localnav nav { min-width: 0; overflow-x: auto; scrollbar-width: none; }
      .nx .localnav nav a { padding: 5px 7px; }
      .nx .localnav nav a.nav-top { display: none; }
      /* 英語の長い凡例（Radiofrequency など）で円グラフのカードがはみ出さないように */
      .nx .pie-card { grid-template-columns: 120px minmax(0, 1fr); }
      .nx .pie-legend li { overflow-wrap: anywhere; }
    }
  </style>
'''


def head_en(title, desc, ja):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="{desc}">
  <title>{title} | Tsugutoshi Suzuki, MD, PhD</title>
  <link rel="alternate" hreflang="ja" href="https://www.tsugutoshi.com/{ja}">
  <link rel="shortcut icon" href="assets/icons/profile.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/icons/profile-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/icons/profile-180.png">
  <meta name="theme-color" content="#8bf5c5">
  <link rel="stylesheet" href="assets/tsugu.css?v={V_T}">
  <script>document.documentElement.classList.add('nx-js');</script>
  <link rel="stylesheet" href="assets/ca.css?v={V_CA}">
{EN_STYLE}  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-R0BG9XQGE4"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-R0BG9XQGE4');
  </script>
</head>
'''


def nav_en(cur, ja):
    items = [('index_en.html', 'Top'), ('ablation_en.html', '<span class="long">Catheter Ablation</span><span class="short">All</span>'), ('wpw_results_en.html', 'WPW'),
             ('avnrt_results_en.html', 'AVNRT'), ('pvc_results_en.html', '<span class="long">PVC/NSVT</span><span class="short">PVC</span>')]
    out = '\n'.join(f'          <a href="{h}"{CUR if h == cur else ""}{TOPCLS if h == "index_en.html" else ""}>{t}</a>' for h, t in items)
    return f'''    <header class="localnav">
      <div class="in">
        <a class="logo" href="index_en.html" aria-label="To the top page"><img src="for_top_page/gif/title.gif" width="273" height="84" alt="Tsugutoshi's HomePage"></a>
        <nav aria-label="Site">
{out}
          <a href="{ja}" hreflang="ja" lang="ja">日本語</a>
        </nav>
      </div>
    </header>
'''


def foot_en(links):
    l = ''.join(f'<a href="{h}">{t}</a>' for h, t in links)
    return f'''    <footer class="page-foot">
      <div class="links">{l}</div>
      <p>Tsugutoshi Suzuki's website · since 1997</p>
      <img src="for_top_page/gif/PoweredByMac_tang.gif" width="88" height="31" alt="Powered by Mac">
    </footer>
  </div>

  <script src="assets/ca.js?v={V_CJ}" defer></script>
  <script src="assets/tsugu.js?v={V_TJ}" defer></script>
</body>
</html>
'''


def pie2_en(title, small, pct_, color, label_on, n_on, label_off, n_off):
    a = f'{pct_:.2f}'
    return f'''            <figure class="pie-card">
              <figcaption><b>{title}</b><small>{small}</small></figcaption>
              <div class="pie" style="background:conic-gradient(var({color}) 0% {a}%, var(--c-rest) {a}% 100%)" role="img" aria-label="{title}: {label_on} {f(n_on)} ({pct_:.1f}%), {label_off} {f(n_off)}"><span class="pie-hole"><b>{pct_:.1f}</b>%</span></div>
              <ul class="pie-legend"><li><span class="pie-sw" style="background:var({color})" aria-hidden="true"></span>{label_on}<b>{f(n_on)}</b></li><li><span class="pie-sw" style="background:var(--c-rest)" aria-hidden="true"></span>{label_off}<b>{f(n_off)}</b></li></ul>
            </figure>
'''


def pie_multi_en(title, small, parts, hole_num, hole_unit, aria_head):
    tot = sum(n for _, n, _ in parts)
    stops, acc, leg, aria = [], 0.0, [], []
    for name, n, color in parts:
        p = n / tot * 100
        stops.append(f'var({color}) {acc:.2f}% {acc + p:.2f}%'); acc += p
        leg.append(f'<li><span class="pie-sw" style="background:var({color})" aria-hidden="true"></span>{name}<b>{p:.0f}%</b><small>{f(n)}</small></li>')
        aria.append(f'{name} {f(n)} ({p:.0f}%)')
    return f'''            <figure class="pie-card">
              <figcaption><b>{title}</b><small>{small}</small></figcaption>
              <div class="pie" style="background:conic-gradient({', '.join(stops)})" role="img" aria-label="{aria_head}: {', '.join(aria)}"><span class="pie-hole"><b>{hole_num}</b>{hole_unit}</span></div>
              <ul class="pie-legend">{''.join(leg)}</ul>
            </figure>
'''


def stacks_en(rows):
    out = ''
    for label, parts in rows:
        tot = sum(n for _, n, _ in parts)
        segs = ''.join(f'<i style="--w:{n / tot * 100:.2f}%;--c:var({c})" title="{nm} {n}">{n if n / tot > .07 else ""}</i>' for nm, n, c in parts if n)
        aria = ', '.join(f'{nm} {n}' for nm, n, _ in parts)
        out += f'            <li class="ca-stack"><span>{label}</span><div class="ca-stack-bar" role="img" aria-label="{label}: {aria}">{segs}</div></li>\n'
    return f'          <ul class="ca-stacks">\n{out}          </ul>\n'


def legend_en(items):
    return '\n            <ul class="ca-legend" aria-label="Legend">' + ''.join(
        f'<li><span class="ca-sw" style="--c:var({c})" aria-hidden="true"></span>{n}</li>' for n, c in items) + '</ul>'


ENERGY_LEG = '<ul class="ca-legend" aria-label="Legend"><li><span class="ca-sw" style="--c:var(--c-rf)" aria-hidden="true"></span>Radiofrequency</li><li><span class="ca-sw" style="--c:var(--c-cryo)" aria-hidden="true"></span>Cryo</li><li><span class="ca-sw" style="--c:var(--c-both)" aria-hidden="true"></span>Both</li></ul>'
METHODS_DATES = 'between January 1, 2006 and September 26, 2026'
