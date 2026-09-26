## Imported Claude Cowork project instructions

## アブレーション成績の4ページ（生成物）

- `ablation.html`・`wpw_results.html`・`avnrt_results.html`・`pvc_results.html` は `_ca_stats/` のスクリプトで作る生成物。HTML を直接直さず、`_ca_stats/build_*.py` か `assets/ca.css` を直してから `python3 _ca_stats/build_all.py` で作り直し、4ページと `_hospital/`（病院サイト用）をまとめてコミットする。
- 作り直したら `git diff` で、意図した部分以外が変わっていないか確かめる。
- CSS・JS の版番号は自動（`tsugu.css`/`tsugu.js` は `index.html` の番号、`ca.css`/`ca.js` は中身のハッシュ）。手で書き換えない。
- 集計値 `_ca_stats/results_v2.json` を作る `analyze_v2.py` と CA データの Excel はユーザーの Mac（Google ドライブ）にだけある。クラウドでは集計し直せない。
