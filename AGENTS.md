## Imported Claude Cowork project instructions

## アブレーション成績の4ページ（生成物）

- `ablation.html`・`wpw_results.html`・`avnrt_results.html`・`pvc_results.html`、英語版の `ablation_en.html`、研修された先生方の `trainees.html` は `_ca_stats/` のスクリプトで作る生成物。HTML を直接直さず、`_ca_stats/build_*.py` か `assets/ca.css` を直してから `python3 _ca_stats/build_all.py` で作り直し、4ページと `_hospital/`（病院サイト用）をまとめてコミットする。
- 作り直したら `git diff` で、意図した部分以外が変わっていないか確かめる。
- CSS・JS の版番号は自動（`tsugu.css`/`tsugu.js` は `index.html` の番号、`ca.css`/`ca.js` は中身のハッシュ）。手で書き換えない。
- 集計値 `_ca_stats/results_v2.json` を作る `analyze_v2.py` と CA データの Excel はユーザーの Mac（Google ドライブ）にだけある。クラウドでは集計し直せない。

## 英語版のページ

- `index_en.html`・`media_en.html`・`society_en.html`・`papers_en.html`・`index_road_en.html`・`rox_en.html`、資料・アプリの `page_rfca/rfca_manual_en.html`・`page_rfca/rfca_admission_en.html`・`page/flash/flash*_en.html`・`index_fvp_en.html`・`qtc/index_qtc_en.html`・`angio/index_angio_en.html` は日本語版を英訳した手書きのページ（アプリ本体の qtc.html・pvc.html・angio_tool.html は日本語のまま）。日本語版を直したときは英語版も同じように直す。
- `ablation_en.html` だけは `_ca_stats/build_ablation_en.py` で作る生成物（数字は日本語版と同じ集計値）。集計に新しい不整脈の名前が増えたら、スクリプトの `CAT_EN` に英語名を足す。
