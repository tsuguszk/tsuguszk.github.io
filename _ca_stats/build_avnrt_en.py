#!/usr/bin/env python3
"""avnrt_results_en.html（AVNRTの成績の英語版）を作る。内容は build_avnrt.py と同じ"""
_here = __import__('pathlib').Path(__file__).resolve().parent
exec(open(_here / 'ca_helpers.py').read()); exec(open(_here / 'ca_helpers_en.py').read())

AVR = R['avnrt']
G = {'通常型': AVR['groups'][0], '非通常型': AVR['groups'][1]}
FS = AVR['first_session']
LAB = {'通常型': 'Typical', '非通常型': 'Atypical'}
types_pie = pie_multi_en('Procedures', f'All {AVR["n"]} procedures', [(LAB['通常型'], G['通常型']['n'], '--c-g1'), (LAB['非通常型'], G['非通常型']['n'], '--c-g2')], AVR['n'], '', 'Proportion of AVNRT types')
rows = ''.join(f'<tr><th scope="row">{LAB[k]}</th><td>{g["n"]}</td><td>{g["patients"]}</td><td>{g["success_pct"]}</td><td>{g["recur_pct"]}</td></tr>' for k, g in G.items())
table_card = f'''            <figure class="pie-card" style="display:block">
              <figcaption><b>Results by type</b><small>All procedures (including repeat procedures)</small></figcaption>
              <div class="doc-scroll"><table class="doc-table ca-table" style="min-width:0"><thead><tr><th scope="col">Type</th><th scope="col" class="num">Proc.</th><th scope="col" class="num">Patients</th><th scope="col" class="num">Success %</th><th scope="col" class="num">Recur. %</th></tr></thead><tbody>{rows}</tbody></table></div>
            </figure>
'''
rate_pies = ''
for k, g in G.items():
    rate_pies += pie2_en(f'{LAB[k]}: success rate', f'of {g["n"]} procedures', g['success_pct'], '--c-ok', 'Success', g['success'], 'Other', g['n'] - g['success'])
for k, g in G.items():
    rate_pies += pie2_en(f'{LAB[k]}: recurrence rate', f'of {g["n"]} procedures', g['recur_pct'], '--c-re', 'Recurrence', g['recur'], 'No recurrence', g['n'] - g['recur'])
en_pies = ''.join(pie_multi_en(LAB[k], f'{g["n"]} procedures', [('Radiofrequency', g['energy']['RF']['n'], '--c-rf'), ('Cryo', g['energy']['Cryo']['n'], '--c-cryo'), ('Both', g['energy']['RF+Cryo']['n'], '--c-both')], g['n'], '', f'Energy in {LAB[k].lower()} AVNRT') for k, g in G.items())
ebp = [(p['period'], [('Radiofrequency', p['RF'], '--c-rf'), ('Cryo', p['Cryo'], '--c-cryo'), ('Both', p['RF+Cryo'], '--c-both')]) for p in AVR['energy_by_period']]
first_groups = []
for k in ['通常型', '非通常型']:
    grp = []
    for e, nm, c in [('RF', 'Radiofrequency', 'var(--c-rf)'), ('Cryo', 'Cryo', 'var(--c-cryo)')]:
        d = FS[k][e]
        grp.append((d['recur_pct'], c, f"{d['recur_pct']}%", f'{LAB[k]} · {nm}', f"{d['recur']} recurrences / {d['n']} procedures",
                    f"{LAB[k]}, {nm}: recurrence rate {d['recur_pct']}% ({d['recur']} of {d['n']} procedures)", d['recur_pct']))
    first_groups.append(grp)
first_chart = bars_chart('Bar chart of recurrence rate by type and energy in first procedures', 'Recurrence rate (%)', [0, 5, 10, 15, 20], None, first_groups, [LAB['通常型'], LAB['非通常型']],
                         legend=legend_en([('Radiofrequency (RF)', '--c-rf'), ('Cryo', '--c-cryo')]),
                         hint='Hover over a bar (tap on a phone) to see the numbers of recurrences and procedures.')
first_rows = ''; all_rows = ''
for k in ['通常型', '非通常型']:
    for e, nm in [('RF', 'radiofrequency'), ('Cryo', 'cryo'), ('RF+Cryo', 'both')]:
        d = FS[k][e]
        first_rows += f'<tr><th scope="row">{LAB[k]}<br>{nm}</th><td>{d["n"]}</td><td>{d["success_pct"]}</td><td>{d["recur"]}</td><td>{d["recur_pct"]}</td></tr>\n'
        d = G[k]['energy'][e]
        all_rows += f'<tr><th scope="row">{LAB[k]}<br>{nm}</th><td>{d["n"]}</td><td>{d["success"]}</td><td>{d["success_pct"]}</td><td>{d["recur"]}</td><td>{d["recur_pct"]}</td></tr>\n'
E = AVR['energy']; fn = AVR['first_n']

# ---- 時期ごとの高周波と冷凍の再発率（集計値に energy_recur_by_period があるときだけ出す）
recent_html = ''
recent_jump = ''
ERP = AVR.get('energy_recur_by_period')
if ERP:
    _rg, _rx, _rrows = [], [], ''
    for row in ERP:
        _g = []
        for e, enm, c in [('RF', 'Radiofrequency', 'var(--c-rf)'), ('Cryo', 'Cryo', 'var(--c-cryo)')]:
            d = row[e]
            if d['n']:
                _g.append((d['recur_pct'], c, f"{d['recur_pct']}%", f"{row['period']} · {enm}", f"{d['recur']} recurrences / {d['n']} procedures",
                           f"{row['period']}, {enm}: recurrence rate {d['recur_pct']}% ({d['recur']} of {d['n']} procedures)", str(d['recur_pct'])))
        if _g:
            _rg.append(_g); _rx.append(row['period'])
        for e, enm in [('RF', 'radiofrequency'), ('Cryo', 'cryo'), ('RF+Cryo', 'both')]:
            d = row[e]
            if d['n']:
                _rrows += f'<tr><th scope="row">{row["period"]}<br>{enm}</th><td>{d["n"]}</td><td>{d["success_pct"]}</td><td>{d["recur"]}</td><td>{d["recur_pct"]}</td></tr>\n'
    _rchart = bars_chart('Bar chart of recurrence rate for radiofrequency and cryo by period', 'Recurrence rate (%)', [0, 5, 10, 15, 20], None, _rg, _rx,
                         legend=legend_en([('Radiofrequency (RF)', '--c-rf'), ('Cryo', '--c-cryo')]),
                         hint='Hover over a bar (tap on a phone) to see the numbers of recurrences and procedures.')
    recent_jump = '<a href="#period">By period</a>'
    recent_html = f'''        <section class="doc-card glass" id="period" data-reveal>
          <h2>Recurrence by period in typical AVNRT (radiofrequency vs. cryo)</h2>
          <p>We divided typical AVNRT procedures into three periods and compared recurrence rates for radiofrequency and cryo (atypical AVNRT is not included; repeat procedures are included). We began using cryo in 2016, so there are no cryo procedures in 2006–2012.</p>
{_rchart}          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">Period / energy</th><th scope="col" class="num">Procedures</th><th scope="col" class="num">Success (%)</th><th scope="col" class="num">Recurrences</th><th scope="col" class="num">Recurrence (%)</th></tr></thead>
              <tbody>
{_rrows}              </tbody>
            </table>
          </div>
          <p class="ca-note-small">"Both" is not shown in the chart because there were few procedures. Follow-up is shorter for more recent procedures, so recurrence rates may look lower. In small groups, a difference of one or two procedures changes the rate a lot.</p>
        </section>

'''

html = head_en('AVNRT results', 'Results of catheter ablation for AVNRT (atrioventricular nodal reentrant tachycardia) in the Department of Pediatric Electrophysiology, Osaka City General Hospital: success and recurrence rates for typical and atypical AVNRT, and radiofrequency vs. cryo, including recurrence in first procedures.', 'avnrt_results.html') + f'''
<body class="nx-body">
  <div class="nx">

{nav_en('avnrt_results_en.html', 'avnrt_results.html')}
    <main>
      <div class="page-hero ca-hero">
        <p class="eyebrow"><a href="ablation_en.html">Catheter Ablation</a> › AVNRT · 2006–2026</p>
        <h1><span class="nw">Catheter Ablation</span> <span class="nw">(AVNRT)</span><span class="h1-sub">Results over 20 years, to 2026</span></h1>
        <p class="sec-lede">Results of <b>catheter ablation for AVNRT (atrioventricular nodal reentrant tachycardia)</b> in our department from 2006 to 2026. AVNRT is a tachycardia in which electricity circles around the AV node (the electrical pathway connecting the atria and ventricles). Results are shown separately for <b>typical</b> and <b>atypical</b> AVNRT, and by energy source (radiofrequency and cryo).</p>
        <nav class="jump" aria-label="On this page">
          <a href="#summary">Summary</a><a href="#type">Typical and atypical</a><a href="#energy">RF and cryo</a><a href="#first">Recurrence in first procedures</a>{recent_jump}<a href="#tables">Tables</a><a href="#related">Related pages</a>
        </nav>
      </div>

      <div class="doc">
        <section class="doc-card glass" id="summary" data-reveal>
          <h2>Summary</h2>
          <div class="ca-kpis ca-kpis--4">
{kpi('Procedures', AVR['n'], '', f'<span class="nw">{AVR["patients"]} patients</span>')}{kpi('Success rate', AVR['success_pct'], '%', f'<span class="nw">{AVR["success"]} successful</span> <span class="nw">of {AVR["n"]}</span>', 'ca-kpi--ok')}{kpi('Recurrence rate', AVR['recur_pct'], '%', f'<span class="nw">{AVR["recur"]} recurrences</span> <span class="nw">of {AVR["n"]}</span>')}{kpi('Procedures using cryo', E['Cryo']['n'] + E['RF+Cryo']['n'], '', f'<span class="nw">cryo alone {E["Cryo"]["n"]},</span> <span class="nw">both {E["RF+Cryo"]["n"]}</span>')}          </div>
        </section>

        <section class="doc-card glass" id="type" data-reveal>
          <h2>Typical and atypical AVNRT</h2>
          <p>We divided AVNRT into the most common <b>typical</b> form and all other, <b>atypical</b> forms.</p>
          <div class="pies pies--2">
{types_pie}{table_card}          </div>
          <h3>Success and recurrence</h3>
          <div class="pies pies--2">
{rate_pies}          </div>
          <p class="doc-note">The success rate was {G['通常型']['success_pct']}% for typical AVNRT and {G['非通常型']['success_pct']}% for atypical AVNRT.</p>
        </section>

        <section class="doc-card glass" id="energy" data-reveal>
          <h2>Radiofrequency and cryoablation</h2>
          <p>Radiofrequency (RF) treats with heat and cryoablation (cryo) by freezing. Cryo is considered less likely to damage the AV node, and we have used it since 2016. "Both" means both were used in one procedure.</p>
          <div class="pies pies--2">
{en_pies}          </div>
          <h3>By period</h3>
          {ENERGY_LEG}
{stacks_en(ebp)}        </section>

        <section class="doc-card glass" id="first" data-reveal>
          <h2>Recurrence in first procedures (radiofrequency vs. cryo)</h2>
          <p>We compared recurrence rates for radiofrequency and cryo <b>only in each patient's first AVNRT procedure ({fn} procedures)</b>. Repeat procedures were excluded.</p>
{first_chart}          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">Type / energy</th><th scope="col" class="num">Procedures</th><th scope="col" class="num">Success (%)</th><th scope="col" class="num">Recurrences</th><th scope="col" class="num">Recurrence (%)</th></tr></thead>
              <tbody>
{first_rows}              </tbody>
            </table>
          </div>
          <p class="ca-note-small">"Both" is not shown in the chart because there were few procedures. In small groups, a difference of one or two procedures changes the rate a lot.</p>
        </section>

{recent_html}        <section class="doc-card glass" id="tables" data-reveal>
          <h2>Tables (all procedures)</h2>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">Type / energy</th><th scope="col" class="num">Procedures</th><th scope="col" class="num">Successful</th><th scope="col" class="num">Success (%)</th><th scope="col" class="num">Recurrences</th><th scope="col" class="num">Recurrence (%)</th></tr></thead>
              <tbody>
{all_rows}              </tbody>
            </table>
          </div>
          <p class="doc-note">Methods: from our department's ablation database, we counted all {AVR['n']} records ({AVR['patients']} patients) in which ablation (energy delivery) was performed for AVNRT {METHODS_DATES}. Repeat procedures in the same patient were each counted as one procedure (except in the comparison of first procedures). Records in which AVNRT was treated together with other arrhythmias such as WPW are included ({AVR['with_wpw']} with WPW, among others). Typical means only the typical form was recorded; atypical means another form was recorded. Recurrence is the number recorded as recurrence in the database (the length of follow-up was not standardized).</p>
        </section>

        <section class="doc-card glass" id="related" data-reveal>
          <h2>Related pages</h2>
          <ul class="doc-links">
            <li><a href="ablation_en.html"><span>Catheter Ablation<small>All procedures</small></span></a></li>
            <li><a href="wpw_results_en.html"><span>WPW results<small>Results by accessory pathway location and period, RF vs. cryo, asymptomatic WPW</small></span></a></li>
            <li><a href="pvc_results_en.html"><span>PVC/NSVT results<small>Results by site for premature ventricular contractions and non-sustained VT</small></span></a></li>
          </ul>
        </section>
      </div>
    </main>

{foot_en([('index_en.html', 'Top page'), ('ablation_en.html', 'Catheter Ablation'), ('wpw_results_en.html', 'WPW'), ('pvc_results_en.html', 'PVC/NSVT'), ('avnrt_results.html', '日本語')])}'''
(ROOT / 'avnrt_results_en.html').write_text(html, encoding='utf-8')
print('ok')
