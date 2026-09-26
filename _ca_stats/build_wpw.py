#!/usr/bin/env python3
"""wpw_results.html を results_v2.json から丸ごと作り直す"""
import re
exec(open(__import__('pathlib').Path(__file__).resolve().parent.joinpath('ca_helpers.py')).read())

W = R['wpw']; T = {t['period']: t for t in W['table']}
L3 = ['左側', '中隔', '右側']; PS = ['2006–2012', '2013–2018', '2019–2026']
old = (ROOT / 'wpw_results.html').read_text(encoding='utf-8')
head_part = old.split('<body')[0]
head_part = re.sub(r'ca\.css\?v=\w+', f'ca.css?v={V_CA}', head_part)
head_part = re.sub(r'tsugu\.css\?v=\w+', f'tsugu.css?v={V_T}', head_part)
head_part = re.sub(r'<meta name="description" content="[^"]*">',
                   '<meta name="description" content="大阪市立総合医療センター 小児不整脈科で2006年から2026年までに行ったWPWのアブレーション治療の成績。副伝導路の位置（左側・中隔・右側）と治療時期ごとの治療件数・成功率・再発率、顕性・間欠性・潜在性ごとの位置の割合、高周波と冷凍、無症候性WPWのAP-VA。">', head_part)
t19, t06 = T['2019–2026'], T['2006–2012']

# ---- 概要
rec_tiles = ''.join(kpi(f'<span class="ca-key" aria-hidden="true"></span>{l}', t19[l]['recur_pct'], '%', f'<span class="nw">2006–2012年</span><span class="nw">は{t06[l]["recur_pct"]}%</span>') for l in L3)
rec_tiles += kpi('3部位の合計', t19['3部位合計']['recur_pct'], '%', f'<span class="nw">再発{t19["3部位合計"]["recur"]}件 ÷ {t19["3部位合計"]["n"]}件、</span><span class="nw">2006–2012年は{t06["3部位合計"]["recur_pct"]}%</span>', 'ca-kpi--all')
suc_tiles = ''.join(kpi(f'<span class="ca-key" style="background:var(--c-ok)" aria-hidden="true"></span>{l}', t19[l]['success_pct'], '%', f'<span class="nw">成功{t19[l]["success"]}件 ÷ {t19[l]["n"]}件</span>') for l in L3)
suc_tiles += kpi('3部位の合計', t19['3部位合計']['success_pct'], '%', f'<span class="nw">成功{t19["3部位合計"]["success"]}件 ÷ {t19["3部位合計"]["n"]}件、</span><span class="nw">2006–2012年は{t06["3部位合計"]["success_pct"]}%</span>', 'ca-kpi--ok')
lower_all = all(t19[l]['recur_pct'] < min(T['2006–2012'][l]['recur_pct'], T['2013–2018'][l]['recur_pct']) for l in L3)
note_sum = '2019–2026年の再発率は、左側・中隔・右側のいずれの位置でも、それ以前の2つの期間より低くなっています。' if lower_all else '2019–2026年の3部位合計の再発率は、それ以前の期間より低くなっています。'

# ---- 病型ごとの位置（患者単位）
TL = {t['type']: t for t in W['type_loc']}
SMALL = {'顕性': 'いつもデルタ波が出る', '間欠性': 'デルタ波が出たり消えたりする', '潜在性': 'デルタ波が出ない（逆向きにだけ伝わる）'}
type_pies = ''
for tn in ['顕性', '間欠性', '潜在性']:
    t = TL[tn]
    type_pies += pie_multi(tn, f'{SMALL[tn]}（{t["patients"]}人）', [('左側', t['左側'], '--c-l'), ('中隔', t['中隔'], '--c-s'), ('右側', t['右側'], '--c-r')], t['patients'], '人', f'{tn}の副伝導路の位置').replace('件</small>', '例</small>').replace('件（', '例（')
bt = ''.join(f"                <tr><th scope=\"row\">{b['type']}</th><td>{b['n']}</td><td>{b['success_pct']}</td><td>{b['recur_pct']}</td></tr>\n" for b in W['by_type'])

# ---- 再発率のグラフ（位置×期間）
groups = []
for l in L3:
    g = []
    for i, p in enumerate(PS):
        d = T[p][l]
        g.append((d['recur_pct'], f'var(--p{i + 1})', f"{d['recur_pct']}%", f'{l} · {p}年', f"再発 {d['recur']}件 / 治療 {d['n']}件",
                  f"{l}、{p}年：再発率{d['recur_pct']}%（再発{d['recur']}件、治療{d['n']}件）", d['recur_pct'] if i == 2 else ''))
    groups.append(g)
chart = bars_chart('WPWの位置と期間ごとの再発率の棒グラフ', '再発率（%）', [0, 5, 10, 15, 20], None, groups, L3,
                   legend=legend([('2006–2012年', '--p1'), ('2013–2018年', '--p2'), ('2019–2026年', '--p3')]),
                   hint='棒にマウスを合わせる（スマホではタップする）と、再発件数と治療件数も表示されます。すべての数字は下の集計表にあります。')

# ---- 治療方法
WE = W['energy']; ab = W['ablated']; CL = W['cryo_loc']
e_rows = ''.join(f"                <tr><th scope=\"row\">{nm}</th><td>{WE[k]['n']}</td><td>{WE[k]['success_pct']}</td><td>{WE[k]['recur_pct']}</td></tr>\n" for k, nm in [('RF', '高周波（RF）'), ('Cryo', '冷凍（Cryo）'), ('RF+Cryo', '両方')])
ebp = [(p['period'] + '年', [('高周波', p['RF'], '--c-rf'), ('冷凍', p['Cryo'], '--c-cryo'), ('両方', p['RF+Cryo'], '--c-both')]) for p in W['energy_by_period']]
leg_e = '<ul class="ca-legend" aria-label="凡例"><li><span class="ca-sw" style="--c:var(--c-rf)" aria-hidden="true"></span>高周波</li><li><span class="ca-sw" style="--c:var(--c-cryo)" aria-hidden="true"></span>冷凍</li><li><span class="ca-sw" style="--c:var(--c-both)" aria-hidden="true"></span>両方</li></ul>'
cryo_note = f"冷凍だけで治療した{WE['Cryo']['n']}件のうち{CL['Cryo']['中隔']}件は中隔の副伝導路" + (f"（残りは右側{CL['Cryo']['右側']}件）" if CL['Cryo']['左側'] == 0 else f"（右側{CL['Cryo']['右側']}件、左側{CL['Cryo']['左側']}件）")

# ---- 無症候性WPW
A = W['asymptomatic']; n = A['records']; no, yes, unk = A['apva'].get('なし', 0), A['apva'].get('あり', 0), A['apva'].get('不明', 0)
a_rows = ''.join(f"                <tr><th scope=\"row\">{l}</th><td>{A['by_loc'][l]['n']}</td><td class=\"hi\">{A['by_loc'][l]['なし']}</td><td>{A['by_loc'][l]['あり']}</td>" + (f"<td>{A['by_loc'][l]['不明']}</td>" if unk else '') + f"<td>{A['by_loc'][l]['なし'] / A['by_loc'][l]['n'] * 100:.0f}</td></tr>\n" for l in L3)
a_st = stacks([(l, [('AP-VAなし', A['by_loc'][l]['なし'], '--c-ok'), ('AP-VAあり', A['by_loc'][l]['あり'], '--c-re')] + ([('不明', A['by_loc'][l]['不明'], '--c-rest')] if unk else [])) for l in L3])
a_leg = '<ul class="ca-legend" aria-label="凡例"><li><span class="ca-sw" style="--c:var(--c-ok)" aria-hidden="true"></span>AP-VAなし</li><li><span class="ca-sw" style="--c:var(--c-re)" aria-hidden="true"></span>AP-VAあり</li>' + ('<li><span class="ca-sw" style="--c:var(--c-rest)" aria-hidden="true"></span>不明</li>' if unk else '') + '</ul>'


# ---- 集計表
def trow(key):
    return ''.join(f"                <tr><th scope=\"row\">{l}</th>" + ''.join(f"<td>{T[p][l][key]}</td>" for p in PS) + f"<td class=\"total\">{T['全期間'][l][key]}</td></tr>\n" for l in L3)


def table(title, key, last):
    return f'''          <h3>{title}</h3>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead>
                <tr><th scope="col">WPWの位置</th><th scope="col" class="num">2006–2012年</th><th scope="col" class="num">2013–2018年</th><th scope="col" class="num">2019–2026年</th><th scope="col" class="num">{last}</th></tr>
              </thead>
              <tbody>
{trow(key)}              </tbody>
              <tfoot>
                <tr><th scope="row">全体※</th>{''.join(f"<td>{T[p]['3部位合計'][key]}</td>" for p in PS + ['全期間'])}</tr>
              </tfoot>
            </table>
          </div>

'''


tables = table('治療件数', 'n', '合計') + table('再発件数', 'recur', '合計') + table('再発率（%）', 'recur_pct', '全期間') + table('成功件数', 'success', '合計') + table('成功率（%）', 'success_pct', '全期間')

body = f'''<body class="nx-body">
  <div class="nx">

    <header class="localnav">
      <div class="in">
        <a class="logo" href="index.html" aria-label="トップページへ"><img src="for_top_page/gif/title.gif" width="273" height="84" alt="つぐとしのweb site"></a>
        <nav aria-label="サイト内">
          <a href="index.html">トップ</a>
{nav('wpw_results.html')}
        </nav>
      </div>
    </header>

    <main>
      <div class="page-hero ca-hero">
        <p class="eyebrow"><a href="ablation.html">アブレーションの仕事</a> › WPW · 2006–2026</p>
        <h1><span class="nw">アブレーション治療</span><span class="nw">（WPW）</span><span class="h1-sub">2026年までの20年間の成績</span></h1>
        <p class="sec-lede">2006年に大阪市立総合医療センター 小児不整脈科に赴任してから、2026年までの20年間に当科で行った<b>WPWのアブレーション治療</b>の成績です。副伝導路の位置（左側・中隔・右側）と治療した時期（3つの期間）に分けて、治療件数・成功率・再発をまとめ、顕性・間欠性・潜在性ごとの位置の割合、高周波と冷凍の治療方法、症状のない（無症候性）WPWも示しました。<a href="ablation.html">アブレーション全体のデータ</a>もご覧ください。</p>
        <nav class="jump" aria-label="このページの目次">
          <a href="#summary">概要</a><a href="#location">位置の割合</a><a href="#chart">再発率のグラフ</a><a href="#energy">高周波と冷凍</a><a href="#asymptomatic">無症候性WPW</a><a href="#tables">集計表</a><a href="#related">関連ページ</a>
        </nav>
      </div>

      <div class="doc">
        <section class="doc-card glass" id="summary" data-reveal>
          <h2>概要</h2>
          <div class="ca-kpis ca-kpis--3">
{kpi('治療件数', W['n'], '件', f'<span class="nw">2006年1月–2026年9月、</span><span class="nw">患者{W["patients"]}人</span>')}{kpi('全体の成功率', W['success_pct'], '%', f'<span class="nw">2006年1月–2026年9月、</span><span class="nw">成功{W["success"]}件 ÷ {W["n"]}件</span>', 'ca-kpi--ok')}{kpi('全体の再発率', W['recur_pct'], '%', f'<span class="nw">2006年1月–2026年9月、</span><span class="nw">再発{W["recur"]}件 ÷ {W["n"]}件</span>')}          </div>

          <p class="ca-kpi-head">2019–2026年の再発率</p>
          <div class="ca-kpis ca-kpis--4">
{rec_tiles}          </div>

          <p class="ca-kpi-head">2019–2026年の成功率</p>
          <div class="ca-kpis ca-kpis--4">
{suc_tiles}          </div>

          <p class="doc-note">{note_sum}</p>
        </section>

        <section class="doc-card glass" id="location" data-reveal>
          <h2>副伝導路の位置の割合（顕性・間欠性・潜在性）</h2>
          <p>WPWを、心電図のデルタ波の出かたで3つに分け、副伝導路の位置（左側・中隔・右側）の割合を比べました。1人の患者さんを1回だけ数えています（2回目以降の治療は数えていません）。</p>
          <div class="pies">
{type_pies}          </div>
          <h3>病型ごとの成功率と再発率</h3>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">病型</th><th scope="col" class="num">治療件数</th><th scope="col" class="num">成功率（%）</th><th scope="col" class="num">再発率（%）</th></tr></thead>
              <tbody>
{bt}              </tbody>
            </table>
          </div>
          <p class="doc-note">潜在性は、右側が少ない、というデータです。あまり知られていないデータだと思います。</p>
          <p class="ca-note-small">1人に複数の副伝導路があった場合は、それぞれの位置に1つずつ数えています（そのため位置の合計は人数より少し多くなります）。病型が記録されていなかった患者さんのうち、術前の心電図の記載から判定できた人はその病型に含め、判定できなかった{W['type_unknown']}人は除いています。アブレーション1021例の論文（2006〜2018年）でも、同じ傾向でした（<a href="index_kato_paper.html">論文のページへ</a>）。</p>
        </section>

        <section class="doc-card glass" id="chart" data-reveal>
          <h2>位置別・期間別の再発率</h2>
{chart}        </section>

        <section class="doc-card glass" id="energy" data-reveal>
          <h2>治療方法（高周波と冷凍）</h2>
          <p>副伝導路は、ふつうは<b>高周波（RF）</b>で焼いて治療します。房室結節（心臓の電気の通り道）のすぐ近くにある中隔の副伝導路などでは、2016年から、凍らせて治療する<b>冷凍アブレーション（Cryo）</b>も使っています。{ab}件の内訳です。</p>
          <div class="pies pies--2">
{pie_multi('治療方法', f'{ab}件', [('高周波', WE['RF']['n'], '--c-rf'), ('冷凍', WE['Cryo']['n'], '--c-cryo'), ('両方', WE['RF+Cryo']['n'], '--c-both')], ab, '件', '治療方法の割合')}            <figure class="pie-card" style="display:block">
              <figcaption><b>期間ごとの内訳</b><small>冷凍は2016年から</small></figcaption>
              {leg_e}
{stacks(ebp)}            </figure>
          </div>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">治療方法</th><th scope="col" class="num">治療件数</th><th scope="col" class="num">成功率（%）</th><th scope="col" class="num">再発率（%）</th></tr></thead>
              <tbody>
{e_rows}              </tbody>
            </table>
          </div>
          <p class="ca-note-small">「両方」は、1回の治療で高周波と冷凍の両方を使ったものです。{cryo_note}で、治療する位置が違うため、成功率や再発率は単純には比べられません。</p>
        </section>

        <section class="doc-card glass" id="asymptomatic" data-reveal>
          <h2>無症候性WPW（症状のないWPW）</h2>
          <p>学校心臓検診などで心電図のデルタ波が見つかり、頻拍の発作（症状）はないけれど治療を受けた症例は<b>{n}件</b>でした。副伝導路が心室から心房へ逆向きに電気を伝える性質（<b>AP-VA</b>）がないと、ふつうのWPWの頻拍（房室回帰性頻拍）は起こりません。</p>
          <div class="ca-kpis ca-kpis--3">
{kpi('無症候性WPW', n, '件', f'<span class="nw">成功{A["success"]}件、</span><span class="nw">再発{A["recur"]}件</span>')}{kpi('AP-VAなし', no, '件', f'<span class="nw">{n}件の{no / n * 100:.0f}%</span>', 'ca-kpi--ok')}{kpi('AP-VAあり', yes, '件', f'<span class="nw">{n}件の{yes / n * 100:.0f}%</span>' + (f'<span class="nw">（不明{unk}件）</span>' if unk else ''))}          </div>
          <h3>位置ごとの AP-VA の有無</h3>
          {a_leg}
{a_st}          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">副伝導路の位置</th><th scope="col" class="num">症例数</th><th scope="col" class="num">AP-VAなし</th><th scope="col" class="num">AP-VAあり</th>{'<th scope="col" class="num">不明</th>' if unk else ''}<th scope="col" class="num">なしの割合（%）</th></tr></thead>
              <tbody>
{a_rows}              </tbody>
            </table>
          </div>
          <p class="ca-note-small">{n}件は治療記録の数です（患者さんは{A['patients']}人で、{A['second']}人は2回治療しています）。副伝導路が2本以上あった{A['multi']}件はそれぞれの位置に数えているため、位置の合計は{n}件より少し多くなります。AP-VAの有無は、治療記録の「WPW with AP_VA」「WPW without AP_VA」の項目で判定し、この項目が空だったものは電気生理検査のVA伝導の記録（副伝導路経由）で判定しました。</p>
        </section>

        <section class="doc-card glass" id="tables" data-reveal>
          <h2>集計表</h2>

{tables}          <p class="ca-note-small">※「全体」の行は、左側・中隔・右側の数字を足し合わせた値です（成功率・再発率は、成功・再発の件数 ÷ 治療件数）。複数の副伝導路があった治療はそれぞれの位置に数えているため、「全体」は治療件数（{W['n']}件）より少し多くなります。</p>
          <p class="doc-note">集計方法：当科のアブレーション治療データベースから、2006年1月1日〜2026年9月26日にWPWとして治療した{W['n']}件（患者{W['patients']}人）を集計しました。同じ患者さんの2回目以降の治療も1件として数えています。成功は、治療の終わりに副伝導路の伝導がなくなった、または症状が良くなったものです。再発は、データベースに再発と記録されたものを数えた値です（追跡期間の長さは揃えていません）。</p>
        </section>

        <section class="doc-card glass" id="related" data-reveal>
          <h2>関連ページ</h2>
          <ul class="doc-links">
            <li><a href="ablation.html"><span>アブレーションの仕事（全症例のデータ）<small>年齢・体重の分布、成功率・再発率、不整脈ごとの成績</small></span></a></li>
            <li><a href="avnrt_results.html"><span>AVNRTの成績<small>通常型（typical）と非通常型（atypical）、高周波と冷凍の比較</small></span></a></li>
            <li><a href="pvc_results.html"><span>PVC/NSVTの成績<small>右室流出路・右室流入路・その他の部位ごとの治療件数と再発率</small></span></a></li>
            <li><a href="index_kato_paper.html"><span>1000例の治療成績（Heart Rhythm 2020）<small>当院で行った小児不整脈のアブレーション治療1021例の成績をまとめた論文の紹介</small></span></a></li>
          </ul>
        </section>
      </div>
    </main>

    <footer class="page-foot">
      <div class="links"><a href="index.html">トップページ</a><a href="ablation.html">アブレーションの仕事</a><a href="index.html#anchor78285">資料・アプリ</a></div>
      <p>つぐとしのweb site · 1997.1.1 開設</p>
      <img src="for_top_page/gif/PoweredByMac_tang.gif" width="88" height="31" alt="Powered by Mac">
    </footer>
  </div>

  <script src="assets/ca.js?v=20260926a" defer></script>
  <script src="assets/tsugu.js?v=20260926f" defer></script>
</body>
</html>
'''
(ROOT / 'wpw_results.html').write_text(head_part + body, encoding='utf-8')
print('ok', 'lower_all', lower_all)
