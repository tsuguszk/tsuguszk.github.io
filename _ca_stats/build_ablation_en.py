_here = __import__('pathlib').Path(__file__).resolve().parent
exec(open(_here / 'ca_helpers.py').read()); exec(open(_here / 'ca_helpers_en.py').read())
# ======================================================================= ablation_en.html（アブレーションの仕事の英語版。数字は日本語版と同じ results_v2.json から）
import math
def ticks_for(mx, step):
    top = math.ceil(mx / step / 4) * step * 4 if mx > 0 else step * 4
    return [top // 4 * i for i in range(5)]
AGE_TICKS = ticks_for(max(a['n'] for a in O['age_hist']), 10)
WT_TICKS = ticks_for(max(w['n'] for w in O['wt_hist']), 25)
def age_name(l):
    return {'18–29': '18–29 years', '30+': '30 years and older'}.get(l, f'{l} years')
age_groups = [[(a['n'], 'var(--p3)' if a['label'] not in ('18–29', '30+') else 'var(--p1)', f"{a['n']}", age_name(a['label']), '', f"{age_name(a['label'])}: {a['n']} procedures", a['n'])] for a in O['age_hist']]
age_labels = [a['label'] for a in O['age_hist']]
wt_names = {'<10': 'under 10 kg', '70+': '70 kg and over'}
wt_groups = [[(w['n'], 'var(--c-r)', f"{w['n']}", wt_names.get(w['label'], w['label'] + ' kg'), '', f"{wt_names.get(w['label'], w['label'] + ' kg')}: {w['n']} procedures", w['n'])] for w in O['wt_hist']]
wt_labels = [w['label'] for w in O['wt_hist']]
per = O['by_period']
per_groups = [[(p['recur_pct'], f'var(--p{i + 1})', f"{p['recur_pct']}%", p['period'], f"{p['recur']} recurrences / {p['n']} procedures",
                f"{p['period']}: recurrence rate {p['recur_pct']}% ({p['recur']} of {p['n']} procedures)", p['recur_pct'])] for i, p in enumerate(per)]
# 不整脈の名前（日本語版の名前 → 英語）。集計に新しい名前が増えたら、ここに足す
CAT_EN = {
    'WPW': 'WPW syndrome', 'AVNRT': 'AVNRT', 'PVC/NSVT': 'PVC/NSVT',
    '心室頻拍（sVT）': 'Ventricular tachycardia (sustained VT)',
    '心房内リエントリー性頻拍・心房粗動（IART/AFL）': 'Intra-atrial reentrant tachycardia / atrial flutter (IART/AFL)',
    '異所性心房頻拍（EAT/focal AT）': 'Ectopic atrial tachycardia (EAT/focal AT)',
    'twin AV node': 'Twin AV node tachycardia',
    '心房細動・多源性心房頻拍（AF/MAT）': 'Atrial fibrillation / multifocal atrial tachycardia (AF/MAT)',
    '接合部頻拍（JET）': 'Junctional ectopic tachycardia (JET)',
    'PJRT': 'PJRT', 'Mahaim': 'Mahaim fiber',
}
cat_rows = ''.join(f"                <tr><th scope=\"row\">{CAT_EN[c['name']]}</th><td>{f(c['n'])}</td><td>{f(c['patients'])}</td><td>{c['success_pct']}</td><td>{c['recur_pct']}</td></tr>\n" for c in O['by_cat'])
per_rows = ''.join(f"                <tr><th scope=\"row\">{p['period']}</th><td>{f(p['n'])}</td><td>{f(p['patients'])}</td><td>{p['success_pct']}</td><td>{p['recur_pct']}</td></tr>\n" for p in per)
E = O['energy']
adult = O['n'] - O['under18']
MON = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
def ym(s):
    y, m = s.split('-')[:2]
    return f'{MON[int(m)]} {y}'
FIRST, LAST = ym(O['first']), ym(O['last'])

def pie2_en(title, small, pct_, color, label_on, n_on, label_off, n_off):
    a = f'{pct_:.2f}'
    return f'''            <figure class="pie-card">
              <figcaption><b>{title}</b><small>{small}</small></figcaption>
              <div class="pie" style="background:conic-gradient(var({color}) 0% {a}%, var(--c-rest) {a}% 100%)" role="img" aria-label="{title}: {label_on} {f(n_on)} ({pct_:.1f}%), {label_off} {f(n_off)}"><span class="pie-hole"><b>{pct_:.1f}</b>%</span></div>
              <ul class="pie-legend"><li><span class="pie-sw" style="background:var({color})" aria-hidden="true"></span>{label_on}<b>{f(n_on)}</b></li><li><span class="pie-sw" style="background:var(--c-rest)" aria-hidden="true"></span>{label_off}<b>{f(n_off)}</b></li></ul>
            </figure>
'''


html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="Data from all {f(O['n'])} catheter ablation procedures performed in the Department of Pediatric Electrophysiology, Osaka City General Hospital, from 2006 to 2026: age and weight distribution, success and recurrence rates, and outcomes by arrhythmia.">
  <title>Catheter Ablation | Tsugutoshi Suzuki, MD, PhD</title>
  <link rel="alternate" hreflang="ja" href="https://www.tsugutoshi.com/ablation.html">
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

<body class="nx-body">
  <div class="nx">

{nav_en('ablation_en.html', 'ablation.html')}
    <main>
      <div class="page-hero ca-hero ca-hero--photo">
        <figure class="ca-hero-photo"><span class="shot-img"><img src="assets/media/ablation-room.webp?v=4" width="1540" height="1021" alt="Catheter ablation in the catheterization laboratory"></span></figure>
        <div class="ca-hero-text">
        <p class="eyebrow">Catheter ablation · 2006–2026</p>
        <h1><span class="nw">Catheter Ablation</span><span class="h1-sub">All procedures, 2006–2026</span></h1>
        <p class="sec-lede">Data from all <b>{f(O['n'])} catheter ablation procedures ({f(O['patients'])} patients)</b> performed in our department from my arrival at Osaka City General Hospital in 2006 to {LAST}: age and body weight at treatment, success and recurrence rates, and outcomes by arrhythmia.</p>
        <nav class="jump" aria-label="On this page">
          <a href="#summary">Summary</a><a href="#outcome">Success and recurrence</a><a href="#age">Age</a><a href="#weight">Weight</a><a href="#period">By period</a><a href="#kinds">By arrhythmia</a><a href="#detail">Detailed results</a><a class="jump-go" href="wpw_results_en.html">WPW</a><a class="jump-go" href="avnrt_results_en.html">AVNRT</a><a class="jump-go" href="pvc_results_en.html">PVC/NSVT</a>
        </nav>
        </div>
      </div>

      <div class="doc">
        <section class="doc-card glass" id="summary" data-reveal>
          <h2>Summary</h2>
          <div class="ca-kpis ca-kpis--4">
{kpi('Procedures', f(O['n']), '', f'<span class="nw">{FIRST}–{LAST},</span> <span class="nw">{f(O["patients"])} patients</span>')}{kpi('Success rate', O['success_pct'], '%', f'<span class="nw">{f(O["success"])} successful</span> <span class="nw">of {f(O["n"])}</span>', 'ca-kpi--ok')}{kpi('Recurrence rate', O['recur_pct'], '%', f'<span class="nw">{f(O["recur"])} recurrences</span> <span class="nw">of {f(O["n"])}</span>')}{kpi('Median age', f"{O['age_median']:g}", ' years', f'<span class="nw">from 0</span> <span class="nw">to {O["age_max"]:g} years</span>')}          </div>

          <p class="ca-kpi-head">Including small children and patients after heart surgery</p>
          <div class="ca-kpis ca-kpis--4">
{kpi('Under 1 year', O['infants'], '', 'Procedures in infants')}{kpi('Under 15 kg', O['under15kg'], '', 'Procedures in small children')}{kpi('Congenital heart disease', O['chd'], '', '<span class="nw">Arrhythmias with heart disease</span> <span class="nw">or after surgery</span>')}{kpi('18 years and older', adult, '', '<span class="nw">Mostly patients we have</span> <span class="nw">followed since childhood</span>')}          </div>
          <p class="doc-note">Since 2016 we have also used <b>cryoablation</b>, which treats by freezing (cryoablation alone in {E['Cryo']['n']} procedures, combined with radiofrequency in {E['RF+Cryo']['n']}).</p>
        </section>

        <section class="doc-card glass" id="outcome" data-reveal>
          <h2>Success and recurrence</h2>
          <p>"Success" means that tachycardia could no longer be induced at the end of the procedure, or that symptoms or the arrhythmia improved. "Recurrence" means that the same arrhythmia returned after the procedure.</p>
          <div class="pies pies--2">
{pie2_en('Success rate', f'of all {f(O["n"])} procedures', O['success_pct'], '--c-ok', 'Success', O['success'], 'Other', O['n'] - O['success'])}{pie2_en('Recurrence rate', f'of all {f(O["n"])} procedures', O['recur_pct'], '--c-re', 'Recurrence', O['recur'], 'No recurrence', O['n'] - O['recur'])}          </div>
        </section>

        <section class="doc-card glass" id="age" data-reveal>
          <h2>Age at treatment</h2>
          <p>The most common ages are 12 to 14 (junior high school). We treat patients from infants to adults we have followed since childhood.</p>
{bars_chart('Bar chart of the number of procedures by age at treatment', 'Procedures', AGE_TICKS, None, age_groups, age_labels, 'ca-chart--hist ca-chart--dense', 'Age (years)', 'Hover over a bar (tap on a phone) to see the number. Ages 18 and over are grouped into two bars.')}        </section>

        <section class="doc-card glass" id="weight" data-reveal>
          <h2>Body weight at treatment</h2>
          <p>{O['under15kg']} procedures were in small children weighing under 15 kg (roughly up to 3 years of age). The smaller the body, the harder it is to handle the catheters.</p>
{bars_chart('Bar chart of the number of procedures by body weight at treatment', 'Procedures', WT_TICKS, None, wt_groups, wt_labels, 'ca-chart--hist', 'Body weight (kg)', 'Hover over a bar (tap on a phone) to see the number.')}        </section>

        <section class="doc-card glass" id="period" data-reveal>
          <h2>Results by period</h2>
          <p>Dividing the procedures into three periods, the recurrence rate has gradually decreased.</p>
{bars_chart('Bar chart of the recurrence rate by period', 'Recurrence rate (%)', [0, 5, 10, 15, 20], None, per_groups, [p['period'] for p in per])}          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">Period</th><th scope="col" class="num">Procedures</th><th scope="col" class="num">Patients</th><th scope="col" class="num">Success (%)</th><th scope="col" class="num">Recurrence (%)</th></tr></thead>
              <tbody>
{per_rows}              </tbody>
              <tfoot><tr><th scope="row">All periods</th><td>{f(O['n'])}</td><td>{f(O['patients'])}</td><td>{O['success_pct']}</td><td>{O['recur_pct']}</td></tr></tfoot>
            </table>
          </div>
        </section>

        <section class="doc-card glass" id="kinds" data-reveal>
          <h2>Results by arrhythmia</h2>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">Arrhythmia</th><th scope="col" class="num">Procedures</th><th scope="col" class="num">Patients</th><th scope="col" class="num">Success (%)</th><th scope="col" class="num">Recurrence (%)</th></tr></thead>
              <tbody>
{cat_rows}              </tbody>
            </table>
          </div>
          <p class="ca-note-small">When two or more arrhythmias were treated in one procedure, each was counted (so the total is larger than the number of procedures). Rates for arrhythmias with few procedures can vary widely.</p>
        </section>

        <section class="doc-card glass" id="detail" data-reveal>
          <h2>Detailed results</h2>
          <p>The three most common arrhythmias are described in detail on separate pages.</p>
          <div class="ca-subs">
            <a class="ca-sub" href="wpw_results_en.html"><b>WPW</b><span>Recurrence by accessory pathway location and period, radiofrequency vs. cryoablation, and asymptomatic WPW. {f(W['n'])} procedures, success rate {W['success_pct']}%</span><em>WPW results</em></a>
            <a class="ca-sub" href="avnrt_results_en.html"><b>AVNRT</b><span>Atrioventricular nodal reentrant tachycardia: common vs. other types, radiofrequency vs. cryoablation. {f(R['avnrt']['n'])} procedures</span><em>AVNRT results</em></a>
            <a class="ca-sub" href="pvc_results_en.html"><b>PVC/NSVT</b><span>Premature ventricular contractions and non-sustained VT: results by site (RVOT, RV inflow and others). {f(R['pvc']['n'])} procedures</span><em>PVC/NSVT results</em></a>
          </div>
          <p class="doc-note">Methods: from our department's ablation database, we counted all {f(O['n'])} records ({f(O['patients'])} patients) in which radiofrequency or cryo energy was delivered for an arrhythmia between January 1, 2006 and September 26, 2026. Repeat procedures in the same patient were each counted as one procedure. Recurrence is the number recorded as recurrence in the database (the length of follow-up was not standardized).</p>
        </section>

        <section class="doc-card glass" id="related" data-reveal>
          <h2>Related pages</h2>
          <ul class="doc-links">
            <li><a href="papers_en.html#p2020-hr"><span>Outcomes of 1,021 procedures (Heart Rhythm 2020)<small>Our paper on 1,021 ablation procedures from 2006 to 2018</small></span></a></li>
            <li><a href="trainees.html" hreflang="ja"><span>Doctors who trained with us (Japanese)<small>Doctors who trained in pediatric electrophysiology since the department was founded in 2009</small></span></a></li>
          </ul>
        </section>
      </div>
    </main>

    <footer class="page-foot">
      <div class="links"><a href="index_en.html">Top page</a><a href="wpw_results_en.html">WPW</a><a href="avnrt_results_en.html">AVNRT</a><a href="pvc_results_en.html">PVC/NSVT</a><a href="ablation.html" hreflang="ja">日本語</a></div>
      <p>Tsugutoshi Suzuki's website · since 1997</p>
      <img src="for_top_page/gif/PoweredByMac_tang.gif" width="88" height="31" alt="Powered by Mac">
    </footer>
  </div>

  <script src="assets/ca.js?v={V_CJ}" defer></script>
  <script src="assets/tsugu.js?v={V_TJ}" defer></script>
</body>
</html>
'''
(ROOT / 'ablation_en.html').write_text(html, encoding='utf-8')
print('ok')
