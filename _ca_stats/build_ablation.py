exec(open(__import__('pathlib').Path(__file__).resolve().parent.joinpath('ca_helpers.py')).read())
# ======================================================================= ablation.html
import math
def ticks_for(mx, step):
    top = math.ceil(mx / step / 4) * step * 4 if mx > 0 else step * 4
    return [top // 4 * i for i in range(5)]
AGE_TICKS = ticks_for(max(a['n'] for a in O['age_hist']), 10)
WT_TICKS = ticks_for(max(w['n'] for w in O['wt_hist']), 25)
age_groups = [[(a['n'], 'var(--p3)' if a['label'] not in ('18–29', '30+') else 'var(--p1)', f"{a['n']}件",
                (a['label'] + '歳' if a['label'][0].isdigit() and '–' not in a['label'] and '+' not in a['label'] else ('18–29歳' if a['label'] == '18–29' else '30歳以上')),
                '', f"{a['label']}歳：{a['n']}件", a['n'])] for a in O['age_hist']]
age_labels = [a['label'] if a['label'] not in ('18–29', '30+') else ('18–29' if a['label'] == '18–29' else '30+') for a in O['age_hist']]
wt_names = {'<10': '10kg未満', '70+': '70kg以上'}
wt_groups = [[(w['n'], 'var(--c-r)', f"{w['n']}件", wt_names.get(w['label'], w['label'] + 'kg'), '', f"{wt_names.get(w['label'], w['label'] + 'kg')}：{w['n']}件", w['n'])] for w in O['wt_hist']]
wt_labels = [w['label'] for w in O['wt_hist']]

per = O['by_period']
per_groups = [[(p['recur_pct'], f'var(--p{i + 1})', f"{p['recur_pct']}%", f"{p['period']}年", f"再発 {p['recur']}件 / 治療 {p['n']}件",
                f"{p['period']}年：再発率{p['recur_pct']}%（再発{p['recur']}件、治療{p['n']}件）", p['recur_pct'])] for i, p in enumerate(per)]

cat_rows = ''.join(f"                <tr><th scope=\"row\">{c['name']}</th><td>{f(c['n'])}</td><td>{f(c['patients'])}</td><td>{c['success_pct']}</td><td>{c['recur_pct']}</td></tr>\n" for c in O['by_cat'])
per_rows = ''.join(f"                <tr><th scope=\"row\">{p['period']}年</th><td>{f(p['n'])}</td><td>{f(p['patients'])}</td><td>{p['success_pct']}</td><td>{p['recur_pct']}</td></tr>\n" for p in per)
E = O['energy']
cats = {c['name']: c for c in O['by_cat']}
adult = O['n'] - O['under18']

abl_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="大阪市立総合医療センター 小児不整脈科で2006年から2026年までに行ったカテーテルアブレーション全{f(O['n'])}件のデータ。年齢・体重の分布、成功率・再発率、不整脈別の成績と、WPW・AVNRT・PVC/NSVTの詳しい成績へのリンク。">
  <title>アブレーションの仕事 | つぐとしのweb site</title>
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
{nav('ablation.html')}
        </nav>
      </div>
    </header>

    <main>
      <div class="page-hero ca-hero ca-hero--photo">
        <figure class="ca-hero-photo"><span class="shot-img"><img src="assets/media/ablation-room.webp?v=2" width="1159" height="768" alt="カテーテル室でアブレーション治療をしている様子"></span><figcaption hidden>カテーテル室でのアブレーション治療</figcaption></figure>
        <div class="ca-hero-text">
        <p class="eyebrow">Catheter ablation · 2006–2026</p>
        <h1><span class="nw">アブレーションの仕事</span><span class="h1-sub">全症例のデータ（2006–2026年）</span></h1>
        <p class="sec-lede">2006年に大阪市立総合医療センター 小児不整脈科に赴任してから2026年9月までに、当科で行った<b>カテーテルアブレーション{f(O['n'])}件（患者さん{f(O['patients'])}人）</b>のデータです。治療したときの年齢と体重、成功率と再発率、不整脈ごとの成績をまとめました。WPW・AVNRT・PVC/NSVTは、それぞれのページで詳しく紹介しています。</p>
        <nav class="jump" aria-label="このページの目次">
          <a href="#summary">概要</a><a href="#outcome">成功率と再発率</a><a href="#age">年齢</a><a href="#weight">体重</a><a href="#period">期間ごとの成績</a><a href="#kinds">不整脈ごとの成績</a><a href="#detail">詳しい成績</a><a class="jump-go" href="wpw_results.html">WPW</a><a class="jump-go" href="avnrt_results.html">AVNRT</a><a class="jump-go" href="pvc_results.html">PVC/NSVT</a>
        </nav>
        </div>
      </div>

      <div class="doc">
        <section class="doc-card glass" id="summary" data-reveal>
          <h2>概要</h2>
          <div class="ca-kpis ca-kpis--4">
{kpi('治療件数', f(O['n']), '件', f'<span class="nw">2006年6月–2026年9月、</span><span class="nw">患者さん{f(O["patients"])}人</span>')}{kpi('成功率', O['success_pct'], '%', f'<span class="nw">成功{f(O["success"])}件</span> <span class="nw">÷ {f(O["n"])}件</span>', 'ca-kpi--ok')}{kpi('再発率', O['recur_pct'], '%', f'<span class="nw">再発{f(O["recur"])}件</span> <span class="nw">÷ {f(O["n"])}件</span>')}{kpi('年齢（中央値）', f"{O['age_median']:g}", '歳', f'<span class="nw">0歳から</span><span class="nw">{O["age_max"]:g}歳まで</span>')}          </div>

          <p class="ca-kpi-head">小さな子どもや、心臓の手術を受けた患者さんも</p>
          <div class="ca-kpis ca-kpis--4">
{kpi('1歳未満', O['infants'], '件', '赤ちゃんの治療')}{kpi('体重15kg未満', O['under15kg'], '件', '体の小さな子どもの治療')}{kpi('先天性心疾患', O['chd'], '件', '<span class="nw">心臓の病気や手術の</span><span class="nw">あとの不整脈</span>')}{kpi('18歳以上', adult, '件', '<span class="nw">子どものころからの</span><span class="nw">患者さんなど</span>')}          </div>
          <p class="doc-note">2016年からは、凍らせて治療する<b>冷凍アブレーション（クライオ）</b>も使っています（冷凍のみ{E['Cryo']['n']}件、高周波と両方{E['RF+Cryo']['n']}件）。</p>
        </section>

        <section class="doc-card glass" id="outcome" data-reveal>
          <h2>成功率と再発率</h2>
          <p>「成功」は、治療の終わりに頻拍が起こらなくなった、または症状や不整脈が良くなったものです。「再発」は、治療のあとに同じ不整脈がまた起きたものです。</p>
          <div class="pies pies--2">
{pie2('成功率', f'全{f(O["n"])}件のうち', O['success_pct'], '--c-ok', '成功', O['success'], 'それ以外', O['n'] - O['success'], '')}{pie2('再発率', f'全{f(O["n"])}件のうち', O['recur_pct'], '--c-re', '再発', O['recur'], '再発なし', O['n'] - O['recur'], '')}          </div>
        </section>

        <section class="doc-card glass" id="age" data-reveal>
          <h2>治療したときの年齢</h2>
          <p>いちばん多いのは12〜14歳（中学生）です。0歳の赤ちゃんから、子どものころから診ている大人の患者さんまで治療しています。</p>
{bars_chart('治療したときの年齢ごとの治療件数の棒グラフ', '治療件数（件）', AGE_TICKS, None, age_groups, age_labels, 'ca-chart--hist ca-chart--dense', '年齢（歳）', '棒にマウスを合わせる（スマホではタップする）と件数が表示されます。18歳以上は、まとめて2本にしています。')}        </section>

        <section class="doc-card glass" id="weight" data-reveal>
          <h2>治療したときの体重</h2>
          <p>体重15kg未満（おおよそ3歳くらいまで）の小さな子どもの治療は{O['under15kg']}件です。体が小さいほど、カテーテルを扱う難しさが増します。</p>
{bars_chart('治療したときの体重ごとの治療件数の棒グラフ', '治療件数（件）', WT_TICKS, None, wt_groups, wt_labels, 'ca-chart--hist', '体重（kg）', '棒にマウスを合わせる（スマホではタップする）と件数が表示されます。')}        </section>

        <section class="doc-card glass" id="period" data-reveal>
          <h2>期間ごとの成績</h2>
          <p>治療した時期を3つに分けると、再発率は少しずつ下がっています。</p>
{bars_chart('期間ごとの再発率の棒グラフ', '再発率（%）', [0, 5, 10, 15, 20], None, per_groups, [p['period'] + '年' for p in per])}          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">期間</th><th scope="col" class="num">治療件数</th><th scope="col" class="num">患者数</th><th scope="col" class="num">成功率（%）</th><th scope="col" class="num">再発率（%）</th></tr></thead>
              <tbody>
{per_rows}              </tbody>
              <tfoot><tr><th scope="row">全期間</th><td>{f(O['n'])}</td><td>{f(O['patients'])}</td><td>{O['success_pct']}</td><td>{O['recur_pct']}</td></tr></tfoot>
            </table>
          </div>
        </section>

        <section class="doc-card glass" id="kinds" data-reveal>
          <h2>不整脈ごとの成績</h2>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">不整脈</th><th scope="col" class="num">治療件数</th><th scope="col" class="num">患者数</th><th scope="col" class="num">成功率（%）</th><th scope="col" class="num">再発率（%）</th></tr></thead>
              <tbody>
{cat_rows}              </tbody>
            </table>
          </div>
          <p class="ca-note-small">1回の治療で2種類以上の不整脈を治療したときは、それぞれに数えています（そのため合計は全体の件数より多くなります）。件数の少ない不整脈は、率が大きく動きます。</p>
        </section>

        <section class="doc-card glass" id="detail" data-reveal>
          <h2>詳しい成績</h2>
          <p>件数の多い3つの不整脈は、それぞれのページで詳しく紹介しています。</p>
          <div class="ca-subs">
            <a class="ca-sub" href="wpw_results.html"><b>WPW</b><span>副伝導路の位置と時期ごとの再発率、高周波と冷凍、無症候性WPW。{f(W['n'])}件、成功率{W['success_pct']}%</span><em>WPWの成績</em></a>
            <a class="ca-sub" href="avnrt_results.html"><b>AVNRT</b><span>房室結節リエントリー性頻拍。通常型（common）とそれ以外、高周波と冷凍の比較。{f(R['avnrt']['n'])}件</span><em>AVNRTの成績</em></a>
            <a class="ca-sub" href="pvc_results.html"><b>PVC/NSVT</b><span>心室期外収縮・非持続性心室頻拍。右室流出路・右室流入路・その他の部位ごとの成績。{f(R['pvc']['n'])}件</span><em>PVC/NSVTの成績</em></a>
          </div>
          <p class="doc-note">集計方法：当科のアブレーション治療データベースから、2006年1月1日〜2026年9月26日に不整脈に対して通電（高周波または冷凍）を行った記録{f(O['n'])}件（患者さん{f(O['patients'])}人）を集計しました。同じ患者さんの2回目以降の治療も1件として数えています。再発は、データベースに再発と記録されたものを数えた値です（追跡期間の長さは揃えていません）。</p>
        </section>

        <section class="doc-card glass" id="related" data-reveal>
          <h2>関連ページ</h2>
          <ul class="doc-links">
            <li><a href="index_kato_paper.html"><span>1000例の治療成績（Heart Rhythm 2020）<small>2006〜2018年のアブレーション1021件の成績をまとめた論文の紹介</small></span></a></li>
            <li><a href="page_rfca/rfca_manual.html"><span>カテーテルアブレーション・電気生理検査の説明資料<small>検査と治療の流れ（PDF）</small></span></a></li>
          </ul>
        </section>
      </div>
    </main>

    <footer class="page-foot">
      <div class="links"><a href="index.html">トップページ</a><a href="wpw_results.html">WPW</a><a href="avnrt_results.html">AVNRT</a><a href="pvc_results.html">PVC/NSVT</a></div>
      <p>つぐとしのweb site · 1997.1.1 開設</p>
      <img src="for_top_page/gif/PoweredByMac_tang.gif" width="88" height="31" alt="Powered by Mac">
    </footer>
  </div>

  <dialog class="nx-lightbox" id="nx-lightbox" aria-label="写真の拡大表示">
    <button type="button" class="lb-close" data-lb-close aria-label="閉じる">×</button>
    <figure><img alt=""><figcaption></figcaption></figure>
  </dialog>

  <script src="assets/ca.js?v={V_CA}" defer></script>
  <script src="assets/tsugu.js?v=20260926f" defer></script>
</body>
</html>
'''
(ROOT / 'ablation.html').write_text(abl_html, encoding='utf-8')

print('ok')
