#!/usr/bin/env python3
"""avnrt_results.html を作り直す（通常型(typical)・非通常型(atypical)、成功率・再発率は円、冷凍と高周波の再発率は初回治療に限定）"""
import re
exec(open(__import__('pathlib').Path(__file__).resolve().parent.joinpath('ca_helpers.py')).read())

AVR = R['avnrt']
G = {'通常型': AVR['groups'][0], '非通常型': AVR['groups'][1]}
FS = AVR['first_session']
LAB = {'通常型': '通常型（typical）', '非通常型': '非通常型（atypical）'}
old = (ROOT / 'avnrt_results.html').read_text(encoding='utf-8')
head_part = old.split('<body')[0]
head_part = re.sub(r'<meta name="description" content="[^"]*">',
                   '<meta name="description" content="大阪市立総合医療センター 小児不整脈科のAVNRT（房室結節リエントリー性頻拍）アブレーションの成績。通常型（typical）と非通常型（atypical）の成功率・再発率、高周波と冷凍の件数と初回治療での再発率の比較。">', head_part)
head_part = re.sub(r'ca\.css\?v=\w+', f'ca.css?v={V_CA}', head_part)
head_part = re.sub(r'tsugu\.css\?v=\w+', f'tsugu.css?v={V_T}', head_part)

types_pie = pie_multi('治療件数', f'全{AVR["n"]}件', [(LAB['通常型'], G['通常型']['n'], '--c-g1'), (LAB['非通常型'], G['非通常型']['n'], '--c-g2')], AVR['n'], '件', 'AVNRTの型の割合')
SHORT = {'通常型': '通常型<br><small>（typical）</small>', '非通常型': '非通常型<br><small>（atypical）</small>'}
rows = ''.join(f'<tr><th scope="row">{SHORT[k]}</th><td>{g["n"]}</td><td>{g["patients"]}</td><td>{g["success_pct"]}</td><td>{g["recur_pct"]}</td></tr>' for k, g in G.items())
table_card = f'''            <figure class="pie-card" style="display:block">
              <figcaption><b>型ごとの成績</b><small>全治療（2回目以降の治療も含む）</small></figcaption>
              <div class="doc-scroll"><table class="doc-table ca-table" style="min-width:0"><thead><tr><th scope="col">型</th><th scope="col" class="num">件数</th><th scope="col" class="num">患者</th><th scope="col" class="num">成功%</th><th scope="col" class="num">再発%</th></tr></thead><tbody>{rows}</tbody></table></div>
            </figure>
'''
rate_pies = ''
for k, g in G.items():
    rate_pies += pie2(f'{LAB[k]}の成功率', f'{g["n"]}件のうち', g['success_pct'], '--c-ok', '成功', g['success'], 'それ以外', g['n'] - g['success'], '')
for k, g in G.items():
    rate_pies += pie2(f'{LAB[k]}の再発率', f'{g["n"]}件のうち', g['recur_pct'], '--c-re', '再発', g['recur'], '再発なし', g['n'] - g['recur'], '')

en_pies = ''.join(pie_multi(LAB[k], f'{g["n"]}件', [('高周波', g['energy']['RF']['n'], '--c-rf'), ('冷凍', g['energy']['Cryo']['n'], '--c-cryo'), ('両方', g['energy']['RF+Cryo']['n'], '--c-both')], g['n'], '件', f'{LAB[k]}の治療方法') for k, g in G.items())
ebp = [(p['period'] + '年', [('高周波', p['RF'], '--c-rf'), ('冷凍', p['Cryo'], '--c-cryo'), ('両方', p['RF+Cryo'], '--c-both')]) for p in AVR['energy_by_period']]
leg_e = '<ul class="ca-legend" aria-label="凡例"><li><span class="ca-sw" style="--c:var(--c-rf)" aria-hidden="true"></span>高周波</li><li><span class="ca-sw" style="--c:var(--c-cryo)" aria-hidden="true"></span>冷凍</li><li><span class="ca-sw" style="--c:var(--c-both)" aria-hidden="true"></span>両方</li></ul>'

first_groups = []
for k in ['通常型', '非通常型']:
    grp = []
    for e, nm, c in [('RF', '高周波', 'var(--c-rf)'), ('Cryo', '冷凍', 'var(--c-cryo)')]:
        d = FS[k][e]
        grp.append((d['recur_pct'], c, f"{d['recur_pct']}%", f'{LAB[k]} · {nm}', f"再発 {d['recur']}件 / 治療 {d['n']}件",
                    f"{LAB[k]}、{nm}：再発率{d['recur_pct']}%（再発{d['recur']}件、治療{d['n']}件）", d['recur_pct']))
    first_groups.append(grp)
first_chart = bars_chart('初回治療の型と治療方法ごとの再発率の棒グラフ', '再発率（%）', [0, 5, 10, 15, 20], None, first_groups, [LAB['通常型'], LAB['非通常型']],
                         legend=legend([('高周波（RF）', '--c-rf'), ('冷凍（Cryo）', '--c-cryo')]),
                         hint='棒にマウスを合わせる（スマホではタップする）と、再発件数と治療件数も表示されます。')
first_rows = ''
for k in ['通常型', '非通常型']:
    for e, nm in [('RF', '高周波'), ('Cryo', '冷凍'), ('RF+Cryo', '両方')]:
        d = FS[k][e]
        first_rows += f'<tr><th scope="row">{LAB[k]}<br>{nm}</th><td>{d["n"]}</td><td>{d["success_pct"]}</td><td>{d["recur"]}</td><td>{d["recur_pct"]}</td></tr>\n'
all_rows = ''
for k in ['通常型', '非通常型']:
    for e, nm in [('RF', '高周波'), ('Cryo', '冷凍'), ('RF+Cryo', '両方')]:
        d = G[k]['energy'][e]
        all_rows += f'<tr><th scope="row">{LAB[k]}<br>{nm}</th><td>{d["n"]}</td><td>{d["success"]}</td><td>{d["success_pct"]}</td><td>{d["recur"]}</td><td>{d["recur_pct"]}</td></tr>\n'
E = AVR['energy']
fn = AVR['first_n']

body = f'''<body class="nx-body">
  <div class="nx">

    <header class="localnav">
      <div class="in">
        <a class="logo" href="index.html" aria-label="トップページへ"><img src="for_top_page/gif/title.gif" width="273" height="84" alt="つぐとしのweb site"></a>
        <nav aria-label="サイト内">
          <a href="index.html">トップ</a>
{nav('avnrt_results.html')}
        </nav>
      </div>
    </header>

    <main>
      <div class="page-hero ca-hero">
        <p class="eyebrow"><a href="ablation.html">アブレーションの仕事</a> › AVNRT · 2006–2026</p>
        <h1><span class="nw">アブレーション治療</span><span class="nw">（AVNRT）</span><span class="h1-sub">2026年までの20年間の成績</span></h1>
        <p class="sec-lede">2006年から2026年までに当科で行った<b>AVNRT（房室結節リエントリー性頻拍）のアブレーション治療</b>の成績です。AVNRTは、房室結節（心房と心室をつなぐ電気の通り道）のまわりを電気がぐるぐる回って起こる頻拍です。<b>通常型（typical）</b>と<b>非通常型（atypical）</b>に分け、高周波と冷凍の治療方法ごとにもまとめました。</p>
        <nav class="jump" aria-label="このページの目次">
          <a href="#summary">概要</a><a href="#type">通常型と非通常型</a><a href="#energy">高周波と冷凍</a><a href="#first">初回治療の再発率</a><a href="#tables">集計表</a><a href="#related">関連ページ</a>
        </nav>
      </div>

      <div class="doc">
        <section class="doc-card glass" id="summary" data-reveal>
          <h2>概要</h2>
          <div class="ca-kpis ca-kpis--4">
{kpi('治療件数', AVR['n'], '件', f'<span class="nw">患者{AVR["patients"]}人</span>')}{kpi('成功率', AVR['success_pct'], '%', f'<span class="nw">成功{AVR["success"]}件</span> <span class="nw">÷ {AVR["n"]}件</span>', 'ca-kpi--ok')}{kpi('再発率', AVR['recur_pct'], '%', f'<span class="nw">再発{AVR["recur"]}件</span> <span class="nw">÷ {AVR["n"]}件</span>')}{kpi('冷凍を使った治療', E['Cryo']['n'] + E['RF+Cryo']['n'], '件', f'<span class="nw">冷凍のみ{E["Cryo"]["n"]}件、</span><span class="nw">両方{E["RF+Cryo"]["n"]}件</span>')}          </div>
        </section>

        <section class="doc-card glass" id="type" data-reveal>
          <h2>通常型（typical）と非通常型（atypical）</h2>
          <p>AVNRTを、いちばん多い<b>通常型（typical）</b>と、それ以外の<b>非通常型（atypical）</b>に分けました。</p>
          <div class="pies pies--2">
{types_pie}{table_card}          </div>
          <h3>成功率と再発率</h3>
          <div class="pies pies--2">
{rate_pies}          </div>
          <p class="doc-note">通常型の成功率は{G['通常型']['success_pct']}%、非通常型は{G['非通常型']['success_pct']}%でした。</p>
        </section>

        <section class="doc-card glass" id="energy" data-reveal>
          <h2>高周波と冷凍</h2>
          <p>高周波（RF）は熱で、冷凍（Cryo）は冷やして治療する方法です。冷凍は、房室結節を傷つける心配が少ないとされ、2016年から使っています。「両方」は1回の治療で両方を使ったものです。</p>
          <div class="pies pies--2">
{en_pies}          </div>
          <h3>期間ごとの内訳</h3>
          {leg_e}
{stacks(ebp)}        </section>

        <section class="doc-card glass" id="first" data-reveal>
          <h2>初回治療での再発率の比較（高周波と冷凍）</h2>
          <p>高周波と冷凍の再発率を、<b>その患者さんの1回目のAVNRTの治療（{fn}件）</b>に限って比べました。2回目以降の治療（再治療）は除いています。</p>
{first_chart}          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">型・治療方法</th><th scope="col" class="num">治療件数</th><th scope="col" class="num">成功率（%）</th><th scope="col" class="num">再発件数</th><th scope="col" class="num">再発率（%）</th></tr></thead>
              <tbody>
{first_rows}              </tbody>
            </table>
          </div>
          <p class="ca-note-small">「両方」は件数が少ないため、グラフには入れていません。件数の少ない群は、1〜2件の違いで率が大きく動きます。</p>
        </section>

        <section class="doc-card glass" id="tables" data-reveal>
          <h2>集計表（すべての治療）</h2>
          <div class="doc-scroll">
            <table class="doc-table ca-table">
              <thead><tr><th scope="col">型・治療方法</th><th scope="col" class="num">治療件数</th><th scope="col" class="num">成功件数</th><th scope="col" class="num">成功率（%）</th><th scope="col" class="num">再発件数</th><th scope="col" class="num">再発率（%）</th></tr></thead>
              <tbody>
{all_rows}              </tbody>
            </table>
          </div>
          <p class="doc-note">集計方法：当科のアブレーション治療データベースから、2006年1月1日〜2026年9月26日にAVNRTとしてアブレーション（通電）を行った記録{AVR['n']}件（患者{AVR['patients']}人）を集計しました。同じ患者さんの2回目以降の治療も1件として数えています（「初回治療での比較」を除く）。WPWなどと同時に治療した記録（WPWとの同時治療{AVR['with_wpw']}件など）も含みます。通常型（typical）は通常型だけが記録されたもの、非通常型（atypical）はそれ以外の型が記録されたものです。再発は、データベースに再発と記録されたものを数えた値です（追跡期間の長さは揃えていません）。</p>
        </section>

        <section class="doc-card glass" id="related" data-reveal>
          <h2>関連ページ</h2>
          <ul class="doc-links">
            <li><a href="ablation.html"><span>アブレーションの仕事<small>全症例のデータ</small></span></a></li>
            <li><a href="wpw_results.html"><span>WPWの成績<small>副伝導路の位置・時期ごとの成績、高周波と冷凍、無症候性WPW</small></span></a></li>
            <li><a href="pvc_results.html"><span>PVC/NSVTの成績<small>心室期外収縮・非持続性心室頻拍の部位ごとの成績</small></span></a></li>
          </ul>
        </section>
      </div>
    </main>

    <footer class="page-foot">
      <div class="links"><a href="index.html">トップページ</a><a href="ablation.html">アブレーションの仕事</a><a href="wpw_results.html">WPW</a><a href="pvc_results.html">PVC/NSVT</a></div>
      <p>つぐとしのweb site · 1997.1.1 開設</p>
      <img src="for_top_page/gif/PoweredByMac_tang.gif" width="88" height="31" alt="Powered by Mac">
    </footer>
  </div>

  <script src="assets/ca.js?v=20260926a" defer></script>
  <script src="assets/tsugu.js?v=20260926f" defer></script>
</body>
</html>
'''
(ROOT / 'avnrt_results.html').write_text(head_part + body, encoding='utf-8')
print('ok')
