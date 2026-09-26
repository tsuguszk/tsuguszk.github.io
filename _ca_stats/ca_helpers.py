#!/usr/bin/env python3
"""results_claude.json → ablation.html（全体）を生成し、wpw_results.html に成功率・治療方法・無症候性WPWを追加する"""
import hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
R = json.load(open(HERE / 'results_v2.json'))
O, W = R['overall'], R['wpw']
f = lambda n: f'{n:,}'


def _ver_in_index(name):
    """トップページ（index.html）に書かれている版番号を使う（サイト全体でそろえて上げている）"""
    m = re.search(re.escape(name) + r'\?v=(\w+)', (ROOT / 'index.html').read_text(encoding='utf-8'))
    return m.group(1)


def _ver_by_content(rel):
    """ファイルの中身から版番号を作る（中身が変われば自動で変わる）"""
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


# 版番号は手で書かない（ブラウザに古いCSS・JSが残らないようにするための番号）
V_T, V_TJ = _ver_in_index('tsugu.css'), _ver_in_index('tsugu.js')
V_CA, V_CJ = _ver_by_content('assets/ca.css'), _ver_by_content('assets/ca.js')


CUR = ' aria-current="page"'  # 今いるページの印（Python 3.11 でも動く書き方）


def nav(cur):
    items = [('ablation.html', '<span class="long">アブレーションの仕事</span><span class="short">全体</span>'), ('wpw_results.html', 'WPW'), ('avnrt_results.html', 'AVNRT'),
             ('pvc_results.html', '<span class="long">PVC/NSVT</span><span class="short">PVC</span>')]
    return '\n'.join(f'          <a href="{h}"{CUR if h == cur else ""}>{t}</a>' for h, t in items)


def kpi(label, value, unit, sub, cls=''):
    return f'''            <div class="ca-kpi{(' ' + cls) if cls else ''}">
              <p class="k-label">{label}</p>
              <p class="k-value">{value}<small>{unit}</small></p>
              <p class="k-sub">{sub}</p>
            </div>
'''


def pie2(title, small, pct_, color, label_on, n_on, label_off, n_off, hole):
    a = f'{pct_:.2f}'
    return f'''            <figure class="pie-card">
              <figcaption><b>{title}</b><small>{small}</small></figcaption>
              <div class="pie" style="background:conic-gradient(var({color}) 0% {a}%, var(--c-rest) {a}% 100%)" role="img" aria-label="{title}：{label_on}{f(n_on)}件（{pct_:.1f}%）、{label_off}{f(n_off)}件"><span class="pie-hole"><b>{pct_:.1f}</b>%</span></div>
              <ul class="pie-legend"><li><span class="pie-sw" style="background:var({color})" aria-hidden="true"></span>{label_on}<b>{f(n_on)}件</b></li><li><span class="pie-sw" style="background:var(--c-rest)" aria-hidden="true"></span>{label_off}<b>{f(n_off)}件</b></li></ul>
            </figure>
'''


def pie_multi(title, small, parts, hole_num, hole_unit, aria_head):
    tot = sum(n for _, n, _ in parts)
    stops, acc, leg, aria = [], 0.0, [], []
    for name, n, color in parts:
        p = n / tot * 100
        stops.append(f'var({color}) {acc:.2f}% {acc + p:.2f}%'); acc += p
        leg.append(f'<li><span class="pie-sw" style="background:var({color})" aria-hidden="true"></span>{name}<b>{p:.0f}%</b><small>{f(n)}件</small></li>')
        aria.append(f'{name}{f(n)}件（{p:.0f}%）')
    return f'''            <figure class="pie-card">
              <figcaption><b>{title}</b><small>{small}</small></figcaption>
              <div class="pie" style="background:conic-gradient({', '.join(stops)})" role="img" aria-label="{aria_head}：{'、'.join(aria)}"><span class="pie-hole"><b>{hole_num}</b>{hole_unit}</span></div>
              <ul class="pie-legend">{''.join(leg)}</ul>
            </figure>
'''


def bars_chart(aria, unit, ticks, k, groups, xlabels, extra_cls='', xtitle='', hint='', legend=''):
    """groups: [[(value, css color, tip, name, sub, aria, show_val)], ...]"""
    grid = ''.join(f'                <div class="ca-grid{" base" if t == 0 else ""}" style="bottom:{t / ticks[-1] * 100:g}%"><span>{t}</span></div>\n' for t in reversed(ticks))
    gs = ''
    for g in groups:
        bs = ''
        for v, c, tip, name, sub, ar, show in g:
            val = f'<span class="ca-val" aria-hidden="true">{show}</span>' if show else ''
            bs += f'                    <button class="ca-bar" type="button" style="--v:{v}" data-tip="{tip}" data-name="{name}" data-sub="{sub}" aria-label="{ar}"><span class="ca-fill" style="--c:{c}"></span>{val}</button>\n'
        gs += f'                  <div class="ca-group">\n{bs}                  </div>\n'
    xs = ''.join(f'<span>{x}</span>' for x in xlabels)
    xt = f'\n              <p class="ca-xtitle" aria-hidden="true">{xtitle}</p>' if xtitle else ''
    hn = f'\n            <figcaption class="ca-hint">{hint}</figcaption>' if hint else ''
    return f'''          <figure class="ca-chart{(' ' + extra_cls) if extra_cls else ''}">{legend}
            <div class="ca-plot" role="group" aria-label="{aria}">
              <p class="ca-unit">{unit}</p>
              <div class="ca-area" style="--k:{100 / ticks[-1]:.4g}%">
{grid}                <div class="ca-groups">
{gs}                </div>
              </div>
              <div class="ca-x" aria-hidden="true">{xs}</div>{xt}
              <div class="ca-tip" aria-hidden="true" hidden></div>
            </div>{hn}
          </figure>
'''


def stacks(rows):
    """rows: [(label, [(name, n, color)])]"""
    out = ''
    for label, parts in rows:
        tot = sum(n for _, n, _ in parts)
        segs = ''.join(f'<i style="--w:{n / tot * 100:.2f}%;--c:var({c})" title="{nm} {n}件">{n if n / tot > .07 else ""}</i>' for nm, n, c in parts if n)
        aria = '、'.join(f'{nm}{n}件' for nm, n, _ in parts)
        out += f'            <li class="ca-stack"><span>{label}</span><div class="ca-stack-bar" role="img" aria-label="{label}：{aria}">{segs}</div></li>\n'
    return f'          <ul class="ca-stacks">\n{out}          </ul>\n'


def legend(items):
    return '\n            <ul class="ca-legend" aria-label="凡例">' + ''.join(
        f'<li><span class="ca-sw" style="--c:var({c})" aria-hidden="true"></span>{n}</li>' for n, c in items) + '</ul>'


