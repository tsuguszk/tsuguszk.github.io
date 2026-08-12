# tsuguszk.github.io

鈴木嗣敏のホームページ（GitHub Pages 公開）。

- 公開URL: https://tsuguszk.github.io/ ／ https://www.tsugutoshi.com/（CNAME）
- ホスティング: GitHub Pages
- アクセス解析: Google Analytics 4
  - サイト全体: `G-R0BG9XQGE4`
  - 解析アプリ（`pvc.html` / `qtc/qtc.html`）: `G-GQDY5X09FF`

## 旧サイト

`tsugu.la.coocan.jp`（hi-ho の Lacoocan）は 2026年9月の契約終了までバックアップとして並行運用。

## 編集と公開

1. ローカルで HTML を編集（Dreamweaver または VS Code）
2. GitHub Desktop で Commit → Push
3. 数十秒後に https://tsuguszk.github.io/ に反映

ローカルで表示確認するときは、リポジトリ直下で:

```bash
python3 -m http.server 8000
```

## スタイルシートの構成

| ファイル | 役割 |
| --- | --- |
| `assets/site.css` | サイト共通。文字サイズ・画像の縮小・レイアウト用テーブルのスマホ対応など |
| `page_rfca/page.css` | `page_rfca/` 配下（アブレーション関連ページ）の共通スタイル |
| `shoshi/shoshi.css` | 所思雑感セクションの共通スタイル |

ページ固有の指定はそのページの `<style>` に書く
（以前のように各ファイルへ同じ `@media` をコピーしない）。

`<font>` `<center>` `align` 属性はすべて廃止し、`assets/site.css` の
ユーティリティクラスに置き換えてある。

| クラス | 用途 |
| --- | --- |
| `.center` / `.left` / `.right` | 旧 `<center>` と `align` 属性 |
| `.center-block` | `<p>` の中で中央寄せしたいとき |
| `.fs-xs` / `.fs-sm` / `.fs-lg` / `.fs-xl` / `.fs-xxl` | 旧 `<font size>` |
| `.v-mid` / `.v-top` | 画像の `align="middle"` `align="top"` |
| `.f-left` / `.f-right` | 画像の回り込み |
| `.para` | テーブル等を含んでいたため `<div>` に変えた段落 |

新しいページを作るときのひな型:

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ページ名 - 鈴木嗣敏のホームページ</title>
  <link rel="stylesheet" href="assets/site.css">
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-R0BG9XQGE4"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', 'G-R0BG9XQGE4');
  </script>
</head>
<body>
</body>
</html>
```

## 大容量配布ファイル

`medical_DL/配布用FVP.zip`（約106MB）は GitHub の上限を超えるため、Google Drive で配布:

- 共有リンク: https://drive.google.com/file/d/1v221r7bXGNi25uzcTgdJtjk4PJNGkRGF/view?usp=sharing
- リンク元: `index_fvp.html`
