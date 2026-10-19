#!/usr/bin/env python3
"""pvc_results_en.html（PVC/NSVTの成績の英語版）を作る。内容は build_pvc.py と同じ"""
_here = __import__('pathlib').Path(__file__).resolve().parent
exec(open(_here / 'ca_helpers.py').read()); exec(open(_here / 'ca_helpers_en.py').read())

PV = R['pvc']; G = PV['groups']; OD = PV['other_detail']
NAME_EN = {'RVOT': 'RVOT', 'RV inflow': 'RV inflow', 'その他': 'Other'}
OD_EN = {'LVOT': 'LVOT', 'RV apex': 'RV apex', '左脚後枝': 'Left posterior fascicle', '左脚前枝': 'Left anterior fascicle', '僧帽弁輪': 'Mitral annulus', 'その他の部位': 'Other sites', '部位の記録なし': 'Site not recorded'}
NAMES = [NAME_EN[g['name']] for g in G]
COL = ['var(--c-g1)', 'var(--c-g2)', 'var(--c-g3)']


def chart(title, aria, unit, ticks, key, fmt, hint=''):
    groups = [[(g[key], COL[i], fmt(g), n, f"{g['n']} procedures · {g['patients']} patients", f"{n}: {fmt(g)}", fmt(g))] for i, (g, n) in enumerate(zip(G, NAMES))]
    html = bars_chart(aria, unit, ticks, None, groups, NAMES, hint=hint)
    return html.replace('<figure class="ca-chart">', f'<figure class="ca-chart">\n            <h3>{title}</h3>', 1)


tops = lambda mx, step: [int(step * 4 * -(-mx // (step * 4)) / 4 * i) for i in range(5)]
cnt_chart = chart('Procedures by site', 'Bar chart of procedures by site', 'Procedures', tops(max(g['n'] for g in G), 10), 'n', lambda g: f"{g['n']}",
                  'RVOT is the right ventricular outflow tract and RV inflow the right ventricular inflow tract. Touch a bar to see the number of patients.')
suc_chart = chart('Success rate by site', 'Bar chart of success rate by site', 'Success rate (%)', [0, 25, 50, 75, 100], 'success_pct', lambda g: f"{g['success_pct']}%")
rec_chart = chart('Recurrence rate by site', 'Bar chart of recurrence rate by site', 'Recurrence rate (%)', tops(max(g['recur_pct'] for g in G), 5), 'recur_pct', lambda g: f"{g['recur_pct']}%",
                  'Hover over a bar (tap on a phone) to see the numbers.')
loc_pie = pie_multi_en('Sites', f'{PV["n"]} procedures', [(n, g['n'], c) for n, g, c in zip(NAMES, G, ['--c-g1', '--c-g2', '--c-g3'])], PV['n'], '', 'Sites of PVC/NSVT')
suc_pie = pie2_en('Acute success', f'{PV["n"]} procedures', PV['success_pct'], '--c-ok', 'Success', PV['success'], 'Other', PV['n'] - PV['success'])
od_rows = ''.join(f'<tr><th scope="row">{OD_EN[k]}</th><td>{v}</td></tr>' for k, v in OD.items() if v)
od_sum = sum(OD.values()); oth_n = G[2]['n']
rows = ''.join(f'<tr><th scope="row">{n}</th><td>{g["n"]}</td><td>{g["patients"]}</td><td>{g["success"]}</td><td>{g["success_pct"]}%</td><td>{g["recur"]}</td><td>{g["recur_pct"]}%</td></tr>' for n, g in zip(NAMES, G))

html = head_en('PVC/NSVT results', 'Results of catheter ablation for PVCs (premature ventricular contractions) and NSVT (non-sustained ventricular tachycardia) in the Department of Pediatric Electrophysiology, Osaka City General Hospital: procedures, success and recurrence rates by site.', 'pvc_results.html') + f'''
<body class="nx-body">
  <div class="nx">

{nav_en('pvc_results_en.html', 'pvc_results.html')}
    <main>
      <div class="page-hero ca-hero">
        <p class="eyebrow"><a href="ablation_en.html">Catheter Ablation</a> › PVC/NSVT · 2006–2026</p>
        <h1><span class="nw">Catheter Ablation</span> <span class="nw">(PVC/NSVT)</span><span class="h1-sub">Results over 20 years, to 2026</span></h1>
        <p class="sec-lede">Results of <b>catheter ablation for PVCs (premature ventricular contractions) and NSVT (non-sustained ventricular tachycardia)</b> in our department from 2006 to 2026. A PVC is an early beat arising from the ventricle; NSVT is a short run of fast ventricular beats. Procedures, success and recurrence rates are shown by treated site.</p>
        <nav class="jump" aria-label="On this page">
          <a href="#summary">Summary</a><a href="#location">Sites</a><a href="#rates">Success and recurrence</a><a href="#other">"Other" breakdown</a><a href="#tables">Tables</a><a href="#related">Related pages</a>
        </nav>
      </div>

      <div class="doc">
        <section class="doc-card glass" id="summary" data-reveal>
          <h2>Summary</h2>
          <div class="ca-kpis ca-kpis--3">
{kpi('Procedures', PV['n'], '', f'{PV["patients"]} patients')}{kpi('Success rate', PV['success_pct'], '%', f'{PV["success"]} successful of {PV["n"]}', 'ca-kpi--ok')}{kpi('Recurrence rate', PV['recur_pct'], '%', f'{PV["recur"]} recurrences of {PV["n"]}')}          </div>
          <p class="doc-note">Success is the proportion judged successful from the records immediately after the procedure. Recurrence is the proportion recorded as recurrence in the database.</p>
        </section>

        <section class="doc-card glass" id="location" data-reveal>
          <h2>Treated sites</h2>
          <p>We divided the procedures into the part of the right ventricle leading to the pulmonary artery (RVOT, right ventricular outflow tract), the part where blood enters the right ventricle (RV inflow), and other sites.</p>
{cnt_chart}          <div class="pies pies--2">
{loc_pie}{suc_pie}          </div>
        </section>

        <section class="doc-card glass" id="rates" data-reveal>
          <h2>Success and recurrence by site</h2>
          <p>The success rate is the number of acute successes, and the recurrence rate the number of recorded recurrences, each divided by the number of procedures at that site.</p>
{suc_chart}{rec_chart}        </section>

        <section class="doc-card glass" id="other" data-reveal>
          <h2>Breakdown of "Other"</h2>
          <p>Sites recorded in the "Other" group. The LVOT is the part of the left ventricle leading to the aorta; the left posterior and anterior fascicles are parts of the heart's conduction system; the mitral annulus is the area around the valve between the left atrium and left ventricle.</p>
          <div class="doc-scroll"><table class="doc-table ca-table"><thead><tr><th scope="col">Site</th><th scope="col" class="num">Records</th></tr></thead><tbody>{od_rows}</tbody></table></div>
          <p class="ca-note-small">When two or more sites were recorded in one procedure, each was counted. The breakdown total ({od_sum}) is therefore larger than the number of "Other" procedures ({oth_n}).</p>
        </section>

        <section class="doc-card glass" id="tables" data-reveal>
          <h2>Tables and methods</h2>
          <div class="doc-scroll"><table class="doc-table ca-table"><thead><tr><th scope="col">Site</th><th scope="col" class="num">Procedures</th><th scope="col" class="num">Patients</th><th scope="col" class="num">Successful</th><th scope="col" class="num">Success</th><th scope="col" class="num">Recurrences</th><th scope="col" class="num">Recurrence</th></tr></thead><tbody>{rows}</tbody><tfoot><tr><th scope="row">Total</th><td>{PV['n']}</td><td>{PV['patients']}</td><td>{PV['success']}</td><td>{PV['success_pct']}%</td><td>{PV['recur']}</td><td>{PV['recur_pct']}%</td></tr></tfoot></table></div>
          <p class="ca-note-small">The patient numbers by site may not add up to the total number of patients, because a patient treated more than once at different sites is counted at each site.</p>
          <p class="doc-note">Methods: from our department's ablation database, we counted all {PV['n']} records ({PV['patients']} patients) treated for PVCs (premature ventricular contractions) or NSVT (non-sustained ventricular tachycardia) {METHODS_DATES}. Repeat procedures in the same patient were each counted as one procedure. Success counts records of acute success, improvement or disappearance. Recurrence is the crude rate of recurrences recorded in the database; the length of follow-up was not standardized.</p>
        </section>

        <section class="doc-card glass" id="related" data-reveal>
          <h2>Related pages</h2>
          <ul class="doc-links">
            <li><a href="ablation_en.html"><span>Catheter Ablation<small>Results of all procedures</small></span></a></li>
            <li><a href="wpw_results_en.html"><span>WPW<small>Results for WPW syndrome</small></span></a></li>
            <li><a href="avnrt_results_en.html"><span>AVNRT<small>Results for AV nodal reentrant tachycardia</small></span></a></li>
          </ul>
        </section>
      </div>
    </main>

{foot_en([('index_en.html', 'Top page'), ('ablation_en.html', 'Catheter Ablation'), ('wpw_results_en.html', 'WPW'), ('avnrt_results_en.html', 'AVNRT'), ('pvc_results.html', '日本語')])}'''
(ROOT / 'pvc_results_en.html').write_text(html, encoding='utf-8')
print('ok')
