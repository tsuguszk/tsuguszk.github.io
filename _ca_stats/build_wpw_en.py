#!/usr/bin/env python3
"""wpw_results_en.html（WPWの成績の英語版）を results_v2.json から作る。内容は build_wpw.py と同じ"""
_here = __import__('pathlib').Path(__file__).resolve().parent
exec(open(_here / 'ca_helpers.py').read()); exec(open(_here / 'ca_helpers_en.py').read())

W = R['wpw']; T = {t['period']: t for t in W['table']}
L3 = ['左側', '中隔', '右側']; PS = ['2006–2012', '2013–2018', '2019–2026']
t19, t06 = T['2019–2026'], T['2006–2012']
E3 = {l: LOC_EN[l] for l in L3}

rec_tiles = ''.join(kpi(f'<span class="ca-key" aria-hidden="true"></span>{E3[l]}', t19[l]['recur_pct'], '%', f'<span class="nw">{t06[l]["recur_pct"]}% in</span> <span class="nw">2006–2012</span>') for l in L3)
rec_tiles += kpi('All three sites', t19['3部位合計']['recur_pct'], '%', f'<span class="nw">{t19["3部位合計"]["recur"]} of {t19["3部位合計"]["n"]};</span> <span class="nw">{t06["3部位合計"]["recur_pct"]}% in 2006–2012</span>', 'ca-kpi--all')
suc_tiles = ''.join(kpi(f'<span class="ca-key" style="background:var(--c-ok)" aria-hidden="true"></span>{E3[l]}', t19[l]['success_pct'], '%', f'<span class="nw">{t19[l]["success"]} of {t19[l]["n"]}</span>') for l in L3)
suc_tiles += kpi('All three sites', t19['3部位合計']['success_pct'], '%', f'<span class="nw">{t19["3部位合計"]["success"]} of {t19["3部位合計"]["n"]};</span> <span class="nw">{t06["3部位合計"]["success_pct"]}% in 2006–2012</span>', 'ca-kpi--ok')
lower_all = all(t19[l]['recur_pct'] < min(T['2006–2012'][l]['recur_pct'], T['2013–2018'][l]['recur_pct']) for l in L3)
note_sum = 'In 2019–2026 the recurrence rate was lower than in the two earlier periods at every site: left, septal and right.' if lower_all else 'In 2019–2026 the recurrence rate for all three sites combined was lower than in the earlier periods.'

TL = {t['type']: t for t in W['type_loc']}
SMALL = {'顕性': 'delta wave always present', '間欠性': 'delta wave comes and goes', '潜在性': 'no delta wave (retrograde conduction only)'}
type_pies = ''
for tn in ['顕性', '間欠性', '潜在性']:
    t = TL[tn]
    type_pies += pie_multi_en(TYPE_EN[tn], f'{SMALL[tn]} ({t["patients"]} patients)', [('Left', t['左側'], '--c-l'), ('Septal', t['中隔'], '--c-s'), ('Right', t['右側'], '--c-r')], t['patients'], '', f'Accessory pathway location in {TYPE_EN[tn].lower()} WPW')
bt = ''.join(f"                <tr><th scope=\"row\">{TYPE_EN[b['type']]}</th><td>{b['n']}</td><td>{b['success_pct']}</td><td>{b['recur_pct']}</td></tr>\n" for b in W['by_type'])

groups = []
for l in L3:
    g = []
    for i, p in enumerate(PS):
        d = T[p][l]
        g.append((d['recur_pct'], f'var(--p{i + 1})', f"{d['recur_pct']}%", f'{E3[l]} · {p}', f"{d['recur']} recurrences / {d['n']} procedures",
                  f"{E3[l]}, {p}: recurrence rate {d['recur_pct']}% ({d['recur']} of {d['n']} procedures)", d['recur_pct'] if i == 2 else ''))
    groups.append(g)
chart = bars_chart('Bar chart of recurrence rate by WPW location and period', 'Recurrence rate (%)', [0, 5, 10, 15, 20], None, groups, [E3[l] for l in L3],
                   legend=legend_en([('2006–2012', '--p1'), ('2013–2018', '--p2'), ('2019–2026', '--p3')]),
                   hint='Hover over a bar (tap on a phone) to see the numbers of recurrences and procedures. All numbers are in the tables below.')

WE = W['energy']; ab = W['ablated']; CL = W['cryo_loc']
e_rows = ''.join(f"                <tr><th scope=\"row\">{nm}</th><td>{WE[k]['n']}</td><td>{WE[k]['success_pct']}</td><td>{WE[k]['recur_pct']}</td></tr>\n" for k, nm in [('RF', 'Radiofrequency (RF)'), ('Cryo', 'Cryo'), ('RF+Cryo', 'Both')])
ebp = [(p['period'], [('Radiofrequency', p['RF'], '--c-rf'), ('Cryo', p['Cryo'], '--c-cryo'), ('Both', p['RF+Cryo'], '--c-both')]) for p in W['energy_by_period']]
_c = CL['Cryo']; _rest = [f"{_c['右側']} right"] + ([f"{_c['左側']} left"] if _c['左側'] else [])
_noloc = WE['Cryo']['n'] - _c['中隔'] - _c['右側'] - _c['左側']
if _noloc > 0: _rest.append(f"{_noloc} with no location recorded")
cryo_note = f"Of the {WE['Cryo']['n']} procedures with cryo alone, {_c['中隔']} were for septal pathways (others: {', '.join(_rest)})"

A = W['asymptomatic']; n = A['records']; no, yes, unk = A['apva'].get('なし', 0), A['apva'].get('あり', 0), A['apva'].get('不明', 0)
a_rows = ''.join(f"                <tr><th scope=\"row\">{E3[l]}</th><td>{A['by_loc'][l]['n']}</td><td class=\"hi\">{A['by_loc'][l]['なし']}</td><td>{A['by_loc'][l]['あり']}</td>" + (f"<td>{A['by_loc'][l]['不明']}</td>" if unk else '') + f"<td>{A['by_loc'][l]['なし'] / A['by_loc'][l]['n'] * 100:.0f}</td></tr>\n" for l in L3)
a_st = stacks_en([(E3[l], [('No AP-VA', A['by_loc'][l]['なし'], '--c-ok'), ('AP-VA present', A['by_loc'][l]['あり'], '--c-re')] + ([('Unknown', A['by_loc'][l]['不明'], '--c-rest')] if unk else [])) for l in L3])
a_leg = '<ul class="ca-legend" aria-label="Legend"><li><span class="ca-sw" style="--c:var(--c-ok)" aria-hidden="true"></span>No AP-VA</li><li><span class="ca-sw" style="--c:var(--c-re)" aria-hidden="true"></span>AP-VA present</li>' + ('<li><span class="ca-sw" style="--c:var(--c-rest)" aria-hidden="true"></span>Unknown</li>' if unk else '') + '</ul>'


def trow(key):
    return ''.join(f"                <tr><th scope=\"row\">{E3[l]}</th>" + ''.join(f"<td>{T[p][l][key]}</td>" for p in PS) + f"<td class=\"total\">{T['全期間'][l][key]}</td></tr>\n" for l in L3)


def table(title, key, last):
    return f'''          <h3>{title}</h3>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead>
                <tr><th scope="col">WPW location</th><th scope="col" class="num">2006–2012</th><th scope="col" class="num">2013–2018</th><th scope="col" class="num">2019–2026</th><th scope="col" class="num">{last}</th></tr>
              </thead>
              <tbody>
{trow(key)}              </tbody>
              <tfoot>
                <tr><th scope="row">All*</th>{''.join(f"<td>{T[p]['3部位合計'][key]}</td>" for p in PS + ['全期間'])}</tr>
              </tfoot>
            </table>
          </div>

'''


tables = table('Procedures', 'n', 'Total') + table('Recurrences', 'recur', 'Total') + table('Recurrence rate (%)', 'recur_pct', 'All periods') + table('Successful procedures', 'success', 'Total') + table('Success rate (%)', 'success_pct', 'All periods')

html = head_en('WPW results', f'Results of catheter ablation for WPW syndrome in the Department of Pediatric Electrophysiology, Osaka City General Hospital, 2006–2026: procedures, success and recurrence rates by accessory pathway location (left, septal, right) and period, location by manifest, intermittent and concealed type, radiofrequency vs. cryo, and AP-VA in asymptomatic WPW.', 'wpw_results.html') + f'''
<body class="nx-body">
  <div class="nx">

{nav_en('wpw_results_en.html', 'wpw_results.html')}
    <main>
      <div class="page-hero ca-hero">
        <p class="eyebrow"><a href="ablation_en.html">Catheter Ablation</a> › WPW · 2006–2026</p>
        <h1><span class="nw">Catheter Ablation</span> <span class="nw">(WPW)</span><span class="h1-sub">Results over 20 years, to 2026</span></h1>
        <p class="sec-lede">Results of <b>catheter ablation for WPW syndrome</b> in our department over the 20 years from my arrival at Osaka City General Hospital in 2006 to 2026. Procedures, success and recurrence are shown by accessory pathway location (left, septal, right) and by period (three periods), together with the location by manifest, intermittent and concealed type, radiofrequency vs. cryoablation, and asymptomatic WPW. See also <a href="ablation_en.html">all ablation data</a>.</p>
        <nav class="jump" aria-label="On this page">
          <a href="#summary">Summary</a><a href="#location">Location by type</a><a href="#chart">Recurrence chart</a><a href="#energy">RF and cryo</a><a href="#asymptomatic">Asymptomatic WPW</a><a href="#tables">Tables</a><a href="#related">Related pages</a>
        </nav>
      </div>

      <div class="doc">
        <section class="doc-card glass" id="summary" data-reveal>
          <h2>Summary</h2>
          <div class="ca-kpis ca-kpis--3">
{kpi('Procedures', W['n'], '', f'<span class="nw">January 2006–September 2026,</span> <span class="nw">{W["patients"]} patients</span>')}{kpi('Overall success rate', W['success_pct'], '%', f'<span class="nw">January 2006–September 2026,</span> <span class="nw">{W["success"]} of {W["n"]}</span>', 'ca-kpi--ok')}{kpi('Overall recurrence rate', W['recur_pct'], '%', f'<span class="nw">January 2006–September 2026,</span> <span class="nw">{W["recur"]} of {W["n"]}</span>')}          </div>

          <p class="ca-kpi-head">Recurrence rate in 2019–2026</p>
          <div class="ca-kpis ca-kpis--4">
{rec_tiles}          </div>

          <p class="ca-kpi-head">Success rate in 2019–2026</p>
          <div class="ca-kpis ca-kpis--4">
{suc_tiles}          </div>

          <p class="doc-note">{note_sum}</p>
        </section>

        <section class="doc-card glass" id="location" data-reveal>
          <h2>Accessory pathway location (manifest, intermittent, concealed)</h2>
          <p>We divided WPW into three types by how the delta wave appears on the ECG and compared the proportions of accessory pathway locations (left, septal, right). Each patient is counted once (repeat procedures are not counted).</p>
          <div class="pies">
{type_pies}          </div>
          <h3>Success and recurrence by type</h3>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">Type</th><th scope="col" class="num">Procedures</th><th scope="col" class="num">Success (%)</th><th scope="col" class="num">Recurrence (%)</th></tr></thead>
              <tbody>
{bt}              </tbody>
            </table>
          </div>
          <p class="doc-note">Concealed pathways were rarely right-sided. I think this finding is not widely known.</p>
          <p class="ca-note-small">When a patient had more than one accessory pathway, each location was counted once (so the location total is slightly larger than the number of patients). Among patients whose type was not recorded, those whose type could be determined from the description of the preprocedural ECG were included in that type; the {W['type_unknown']} patients whose type could not be determined were excluded. Our paper on 1,021 ablation procedures (2006–2018) showed the same tendency (<a href="papers_en.html#p2020-hr">see the paper</a>).</p>
        </section>

        <section class="doc-card glass" id="chart" data-reveal>
          <h2>Recurrence rate by location and period</h2>
{chart}        </section>

        <section class="doc-card glass" id="energy" data-reveal>
          <h2>Radiofrequency and cryoablation</h2>
          <p>Accessory pathways are usually treated by burning with <b>radiofrequency (RF)</b>. Since 2016, for septal pathways right next to the AV node (the electrical pathway of the heart) and in similar situations, we have also used <b>cryoablation</b>, which treats by freezing. The breakdown of {ab} procedures:</p>
          <div class="pies pies--2">
{pie_multi_en('Energy', f'{ab} procedures', [('Radiofrequency', WE['RF']['n'], '--c-rf'), ('Cryo', WE['Cryo']['n'], '--c-cryo'), ('Both', WE['RF+Cryo']['n'], '--c-both')], ab, '', 'Proportion of energy sources')}            <figure class="pie-card" style="display:block">
              <figcaption><b>By period</b><small>Cryo since 2016</small></figcaption>
              {ENERGY_LEG}
{stacks_en(ebp)}            </figure>
          </div>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">Energy</th><th scope="col" class="num">Procedures</th><th scope="col" class="num">Success (%)</th><th scope="col" class="num">Recurrence (%)</th></tr></thead>
              <tbody>
{e_rows}              </tbody>
            </table>
          </div>
          <p class="ca-note-small">"Both" means radiofrequency and cryo were both used in one procedure. {cryo_note}. Because the treated sites differ, success and recurrence rates cannot be compared directly.</p>
        </section>

        <section class="doc-card glass" id="asymptomatic" data-reveal>
          <h2>Asymptomatic WPW</h2>
          <p><b>{n} procedures</b> were performed in patients whose delta wave was found by school heart screening or similar and who had no tachycardia (no symptoms). Without retrograde conduction from the ventricle to the atrium over the accessory pathway (<b>AP-VA</b>), the usual WPW tachycardia (atrioventricular reentrant tachycardia) does not occur.</p>
          <div class="ca-kpis ca-kpis--3">
{kpi('Asymptomatic WPW', n, '', f'<span class="nw">{A["success"]} successful,</span> <span class="nw">{A["recur"]} recurrences</span>')}{kpi('No AP-VA', no, '', f'<span class="nw">{no / n * 100:.0f}% of {n}</span>', 'ca-kpi--ok')}{kpi('AP-VA present', yes, '', f'<span class="nw">{yes / n * 100:.0f}% of {n}</span>' + (f' <span class="nw">({unk} unknown)</span>' if unk else ''))}          </div>
          <h3>AP-VA by location</h3>
          {a_leg}
{a_st}          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">Pathway location</th><th scope="col" class="num">Cases</th><th scope="col" class="num">No AP-VA</th><th scope="col" class="num">AP-VA present</th>{'<th scope="col" class="num">Unknown</th>' if unk else ''}<th scope="col" class="num">No AP-VA (%)</th></tr></thead>
              <tbody>
{a_rows}              </tbody>
            </table>
          </div>
          <p class="ca-note-small">The {n} cases are procedure records ({A['patients']} patients; {A['second']} were treated twice). The {A['multi']} cases with two or more pathways are counted at each location, so the location total is slightly larger than {n}. AP-VA was determined from the "WPW with AP_VA" / "WPW without AP_VA" fields in the procedure records; when these were blank, from the record of VA conduction (via the accessory pathway) in the electrophysiology study.</p>
        </section>

        <section class="doc-card glass" id="tables" data-reveal>
          <h2>Tables</h2>

{tables}          <p class="ca-note-small">* The "All" row is the sum of left, septal and right (success and recurrence rates = successes or recurrences ÷ procedures). Procedures with more than one pathway are counted at each location, so "All" is slightly larger than the number of procedures ({W['n']}).</p>
          <p class="doc-note">Methods: from our department's ablation database, we counted all {W['n']} procedures ({W['patients']} patients) treated as WPW {METHODS_DATES}. Repeat procedures in the same patient were each counted as one procedure. Success means that conduction over the accessory pathway was eliminated at the end of the procedure, or that symptoms improved. Recurrence is the number recorded as recurrence in the database (the length of follow-up was not standardized).</p>
        </section>

        <section class="doc-card glass" id="related" data-reveal>
          <h2>Related pages</h2>
          <ul class="doc-links">
            <li><a href="ablation_en.html"><span>Catheter Ablation (all procedures)<small>Age and weight distribution, success and recurrence rates, results by arrhythmia</small></span></a></li>
            <li><a href="avnrt_results_en.html"><span>AVNRT results<small>Typical vs. atypical, radiofrequency vs. cryo</small></span></a></li>
            <li><a href="pvc_results_en.html"><span>PVC/NSVT results<small>Procedures and recurrence by site: RVOT, RV inflow and others</small></span></a></li>
            <li><a href="papers_en.html#p2020-hr"><span>Outcomes of 1,021 procedures (Heart Rhythm 2020)<small>Our paper on 1,021 pediatric ablation procedures at our hospital</small></span></a></li>
          </ul>
        </section>
      </div>
    </main>

{foot_en([('index_en.html', 'Top page'), ('ablation_en.html', 'Catheter Ablation'), ('wpw_results.html', '日本語')])}'''
(ROOT / 'wpw_results_en.html').write_text(html, encoding='utf-8')
print('ok', 'lower_all', lower_all)
