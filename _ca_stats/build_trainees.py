exec(open(__import__('pathlib').Path(__file__).resolve().parent.joinpath('ca_helpers.py')).read())
# ======================================================================= trainees.html（これまでに小児不整脈で研修された先生方）
# 卒後年数などの個人の経歴は載せない（採用年度・名前・研修前の所属だけ）
TRAINEES = [
    (2009, '岸本慎太郎', '久留米大学'),
    (2009, '尾崎智康', '大阪医科大学'),
    (2010, '青木寿明', '大阪大学'),
    (2012, '吉田修一朗', '名古屋大学'),
    (2015, '渡辺重朗', '横浜市立大学'),
    (2016, '加藤有子', '県立尼崎病院'),
    (2019, '佐藤啓', '金沢大学'),
    (2019, '福留啓祐', '香川県国立こども病院'),
    (2020, '寺師英子', '九州大学'),
    (2022, '中川亮', '金沢大学'),
    (2022, '佐藤一寿', '千葉県立こども病院'),
    (2024, '高見澤幸一', '東京大学'),
    (2025, '小野朱美', '徳島大学'),
    (2026, '松本一希', '名古屋大学'),
]
rows = ''.join(f'                <tr><td>{y}</td><th scope="row">{n}</th><td>{s}</td></tr>\n' for y, n, s in TRAINEES)

html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="大阪市立総合医療センター 小児不整脈科で、2009年の科の設立から2026年までに研修された{len(TRAINEES)}名の先生方。">
  <title>これまでに小児不整脈で研修された先生方 | つぐとしのweb site</title>
  <link rel="shortcut icon" href="assets/icons/profile.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/icons/profile-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/icons/profile-180.png">
  <meta name="theme-color" content="#8bf5c5">
  <link rel="stylesheet" href="assets/tsugu.css?v={V_T}">
  <script>document.documentElement.classList.add('nx-js');</script>
  <link rel="stylesheet" href="assets/ca.css?v={V_CA}">
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-R0BG9XQGE4"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-R0BG9XQGE4');
  </script>
</head>

<body class="nx-body">
  <div class="nx">

    <header class="localnav">
      <div class="in">
        <a class="logo" href="index.html" aria-label="トップページへ"><img src="for_top_page/gif/title.gif" width="273" height="84" alt="つぐとしのweb site"></a>
        <nav aria-label="サイト内">
          <a href="index.html">トップ</a>
{nav('')}
        </nav>
      </div>
    </header>

    <main>
      <div class="page-hero">
        <p class="eyebrow">Trainees · 2009–2026</p>
        <h1 class="h1-mid"><span style="display:inline-block">これまでに小児不整脈で</span><span style="display:inline-block">研修された先生方</span></h1>
        <p class="sec-lede">2009年の小児不整脈科設立から、2026年までに{len(TRAINEES)}名の先生方が研修にこられました。<br>研修後は全国で活躍されています。</p>
      </div>

      <div class="doc">
        <section class="doc-card glass" id="trainees" data-reveal>
          <h2>研修された先生方（{len(TRAINEES)}名）</h2>
          <div class="doc-scroll">
            <table class="doc-table trainee-table">
              <thead><tr><th scope="col">採用年度</th><th scope="col">お名前</th><th scope="col">研修前の所属</th></tr></thead>
              <tbody>
{rows}              </tbody>
            </table>
          </div>
        </section>

        <section class="doc-card glass" id="related" data-reveal>
          <h2>関連ページ</h2>
          <ul class="doc-links">
            <li><a href="ablation.html"><span>アブレーションの仕事<small>2006年からのアブレーション全症例のデータ</small></span></a></li>
          </ul>
        </section>
      </div>
    </main>

    <footer class="page-foot">
      <div class="links"><a href="index.html">トップページ</a><a href="ablation.html">アブレーションの仕事</a></div>
      <p>つぐとしのweb site · 1997.1.1 開設</p>
      <img src="for_top_page/gif/PoweredByMac_tang.gif" width="88" height="31" alt="Powered by Mac">
    </footer>
  </div>

  <script src="assets/tsugu.js?v={V_TJ}" defer></script>
</body>
</html>
'''
(ROOT / 'trainees.html').write_text(html, encoding='utf-8')
print('ok')
