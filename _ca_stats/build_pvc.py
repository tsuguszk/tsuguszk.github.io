#!/usr/bin/env python3
"""pvc_results.html を集計結果（results_v2.json の "pvc"）から作る"""
import re
exec(open(__import__('pathlib').Path(__file__).resolve().parent.joinpath('ca_helpers.py')).read())

PV = R['pvc']; G = PV['groups']; OD = PV['other_detail']
NAMES = [g['name'] for g in G]
COL = ['var(--c-g1)', 'var(--c-g2)', 'var(--c-g3)']
old = (ROOT / 'pvc_results.html').read_text(encoding='utf-8')
head_part = old.split('<body')[0]
head_part = re.sub(r'ca\.css\?v=\w+', f'ca.css?v={V_CA}', head_part)
head_part = re.sub(r'tsugu\.css\?v=\w+', f'tsugu.css?v={V_T}', head_part)


def chart(title, aria, unit, ticks, key, fmt, hint=''):
    groups = [[(g[key], COL[i], fmt(g), n, f"治療 {g['n']}件・患者 {g['patients']}人", f"{n}：{fmt(g)}", fmt(g))] for i, (g, n) in enumerate(zip(G, NAMES))]
    html = bars_chart(aria, unit, ticks, None, groups, NAMES, hint=hint)
    return html.replace('<figure class="ca-chart">', f'<figure class="ca-chart">\n            <h3>{title}</h3>', 1)


tops = lambda mx, step: [int(step * 4 * -(-mx // (step * 4)) / 4 * i) for i in range(5)]
cnt_chart = chart('部位別の治療件数', '部位別の治療件数の棒グラフ', '治療件数（件）', tops(max(g['n'] for g in G), 10), 'n', lambda g: f"{g['n']}件",
                  'RVOTは右室流出路、RV inflowは右室流入路です。棒に触れると患者数も表示されます。')
suc_chart = chart('部位別の成功率', '部位別の成功率の棒グラフ', '成功率（%）', [0, 25, 50, 75, 100], 'success_pct', lambda g: f"{g['success_pct']}%")
rec_chart = chart('部位別の再発率', '部位別の再発率の棒グラフ', '再発率（%）', tops(max(g['recur_pct'] for g in G), 5), 'recur_pct', lambda g: f"{g['recur_pct']}%",
                  '棒にマウスを合わせる（スマホではタップする）と、件数が表示されます。')
loc_pie = pie_multi('部位の割合', f'治療{PV["n"]}件', [(n, g['n'], c) for n, g, c in zip(NAMES, G, ['--c-g1', '--c-g2', '--c-g3'])], PV['n'], '件', 'PVC/NSVTの部位')
suc_pie = pie2('治療直後の成功', f'治療{PV["n"]}件', PV['success_pct'], '--c-ok', '成功', PV['success'], 'その他', PV['n'] - PV['success'], '')
od_rows = ''.join(f'<tr><th scope="row">{k}</th><td>{v}件</td></tr>' for k, v in OD.items() if v)
od_sum = sum(OD.values()); oth_n = G[2]['n']
rows = ''.join(f'<tr><th scope="row">{n}</th><td>{g["n"]}件</td><td>{g["patients"]}人</td><td>{g["success"]}件</td><td>{g["success_pct"]}%</td><td>{g["recur"]}件</td><td>{g["recur_pct"]}%</td></tr>' for n, g in zip(NAMES, G))

body = f'''<body class="nx-body">
  <div class="nx">

    <header class="localnav">
      <div class="in">
        <a class="logo" href="index.html" aria-label="トップページへ"><img src="for_top_page/gif/title.gif" width="273" height="84" alt="つぐとしのweb site"></a>
        <nav aria-label="サイト内">
          <a href="index.html">トップ</a>
{nav('pvc_results.html')}
        </nav>
      </div>
    </header>

    <main>
      <div class="page-hero ca-hero">
        <p class="eyebrow"><a href="ablation.html">アブレーションの仕事</a> › PVC/NSVT · 2006–2026</p>
        <h1><span class="nw">アブレーション治療</span><span class="nw">（PVC/NSVT）</span><span class="h1-sub">2026年までの20年間の成績</span></h1>
        <p class="sec-lede">2006年から2026年までに当科で行った<b>PVC（心室期外収縮）/NSVT（非持続性心室頻拍）のアブレーション治療</b>の成績です。PVCは心室から予定より早く出る拍動、NSVTは心室の速い拍動が短く続く状態です。治療した部位ごとの件数、成功率、再発率を示します。アブレーションは、細い管を使って不整脈の原因部分を治療する方法です。</p>
        <nav class="jump" aria-label="このページの目次">
          <a href="#summary">概要</a><a href="#location">部位の割合</a><a href="#rates">成功率・再発率</a><a href="#other">その他の内訳</a><a href="#tables">集計表</a><a href="#related">関連ページ</a>
        </nav>
      </div>

      <div class="doc">
        <section class="doc-card glass" id="summary" data-reveal>
          <h2>概要</h2>
          <div class="ca-kpis ca-kpis--3">
{kpi('治療件数', PV['n'], '件', f'患者{PV["patients"]}人')}{kpi('成功率', PV['success_pct'], '%', f'成功{PV["success"]}件 ÷ 治療{PV["n"]}件', 'ca-kpi--ok')}{kpi('再発率', PV['recur_pct'], '%', f'再発{PV["recur"]}件 ÷ 治療{PV["n"]}件')}          </div>
          <p class="doc-note">成功は治療直後の記録から判定した割合です。再発はデータベースに再発と記録された割合です。</p>
        </section>

        <section class="doc-card glass" id="location" data-reveal>
          <h2>治療した部位</h2>
          <p>治療記録を、右心室から肺動脈へ向かう部分（RVOT＝右室流出路）、右心室へ血液が入る部分（RV inflow＝右室流入路）、その他に分けました。</p>
{cnt_chart}          <div class="pies pies--2">
{loc_pie}{suc_pie}          </div>
        </section>

        <section class="doc-card glass" id="rates" data-reveal>
          <h2>部位別の成功率と再発率</h2>
          <p>成功率は治療直後の成功件数、再発率は記録された再発件数を、それぞれの部位の治療件数で割った値です。</p>
{suc_chart}{rec_chart}        </section>

        <section class="doc-card glass" id="other" data-reveal>
          <h2>「その他」の内訳</h2>
          <p>「その他」に含まれる部位の記録です。LVOTは左心室から大動脈へ向かう部分、左脚後枝・左脚前枝は心臓の電気が伝わる経路、僧帽弁輪は左心房と左心室の間の弁の周囲を指します。</p>
          <div class="doc-scroll"><table class="doc-table ca-table"><thead><tr><th scope="col">部位</th><th scope="col" class="num">記録件数</th></tr></thead><tbody>{od_rows}</tbody></table></div>
          <p class="ca-note-small">1回の治療で2つ以上の部位が記録されたものは、それぞれの部位に数えています。そのため内訳の合計（{od_sum}件）は、「その他」の治療件数（{oth_n}件）より多くなります。</p>
        </section>

        <section class="doc-card glass" id="tables" data-reveal>
          <h2>集計表と集計方法</h2>
          <div class="doc-scroll"><table class="doc-table ca-table"><thead><tr><th scope="col">部位</th><th scope="col" class="num">治療件数</th><th scope="col" class="num">患者数</th><th scope="col" class="num">成功件数</th><th scope="col" class="num">成功率</th><th scope="col" class="num">再発件数</th><th scope="col" class="num">再発率</th></tr></thead><tbody>{rows}</tbody><tfoot><tr><th scope="row">合計</th><td>{PV['n']}件</td><td>{PV['patients']}人</td><td>{PV['success']}件</td><td>{PV['success_pct']}%</td><td>{PV['recur']}件</td><td>{PV['recur_pct']}%</td></tr></tfoot></table></div>
          <p class="ca-note-small">各部位の患者数を足すと、全体の患者数と一致しないことがあります。同じ患者さんが別の部位で複数回治療を受けた場合、各部位で数えるためです。</p>
          <p class="doc-note">集計方法：当科のアブレーション治療データベースから、2006年1月1日〜2026年9月26日にPVC（心室期外収縮）/NSVT（非持続性心室頻拍）として治療した記録{PV['n']}件（患者{PV['patients']}人）を集計しました。同じ患者さんの2回目以降の治療も1件として数えています。成功は治療直後の成功・改善・消失の記録を数えました。再発はデータベースに再発と記録されたものを数えた粗率で、追跡期間の長さは揃えていません。</p>
        </section>

        <section class="doc-card glass" id="related" data-reveal>
          <h2>関連ページ</h2>
          <ul class="doc-links">
            <li><a href="ablation.html"><span>アブレーションの仕事<small>治療全体の成績</small></span></a></li>
            <li><a href="wpw_results.html"><span>WPW<small>WPWの治療成績</small></span></a></li>
            <li><a href="avnrt_results.html"><span>AVNRT<small>房室結節リエントリー性頻拍の治療成績</small></span></a></li>
          </ul>
        </section>
      </div>
    </main>

    <footer class="page-foot">
      <div class="links"><a href="index.html">トップページ</a><a href="ablation.html">アブレーションの仕事</a><a href="wpw_results.html">WPW</a><a href="avnrt_results.html">AVNRT</a></div>
      <p>つぐとしのweb site · 1997.1.1 開設</p>
      <img src="for_top_page/gif/PoweredByMac_tang.gif" width="88" height="31" alt="Powered by Mac">
    </footer>
  </div>

  <script src="assets/ca.js?v={V_CJ}" defer></script>
  <script src="assets/tsugu.js?v={V_TJ}" defer></script>
</body>
</html>
'''
(ROOT / 'pvc_results.html').write_text(head_part + body, encoding='utf-8')
print('ok')
