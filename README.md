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
| `assets/tsugu.css` | トップ下半分・報道・学会ページの共通デザイン（すべて `.nx` の中に限定。スマホ〜599px／iPad 600〜1099px／Mac 1100px〜） |
| `assets/tsugu.js` | 上記ページのふわっと表示、新聞記事の超拡大スクロール、記事の拡大ビューア、学会ページの年ナビ |
| `assets/showcase.css` / `assets/showcase.js` | Codex版（`index_codex.html`）専用。参考として残しているだけ |
| `page_rfca/page.css` | `page_rfca/` 配下（アブレーション関連ページ）の共通スタイル |

従来ページ固有の指定はそのページの `<style>` に書く。

## トップと活動記録

| ファイル | 内容 |
| --- | --- |
| `index.html` | トップページ。「FVPとWPWの鑑別資料」の行と、その下のリンク・Google／Amazon／楽天の検索窓までは従来と同じレイアウト。「鈴木嗣敏の活動の記録」から下を `assets/tsugu.css` で作り直し |
| `index_2608version.html` | 作り直す前のトップページ（2026/9/21版） |
| `index_codex.html` | Codex が作った案（参考） |
| `media.html` | 新聞記事・テレビ報道 |
| `society.html` | 学会での仕事と、2012年以降の講演・セミナー記録（講演資料フォルダ「_講演・講義」のプログラム・依頼状をもとに作成） |

### 新聞記事のスクロール拡大（`media.html`）

記事ごとの `<section class="zs">` は、画面1枚弱のスクロールで「全体表示 → 約30%拡大」する（2026/9/23、操作性を優先して短くした）。
文字を読むのは「記事を拡大して読む」ボタンの拡大ビューアで行う。

- `data-focus` : 拡大の中心 `"x,y"`（画像内の位置 0〜1。見出しのあたりを指定）
- `data-zoom` : 最大倍率（省略時 1.3）
- ビューアのボタンの `data-char` : 元画像での本文1文字の大きさ（px）。文字が読める倍率で開くための基準

記事画像（`assets/media/*.webp`）は元PDFに埋め込まれた画像を原寸のまま取り出して作成。
2014年の読売新聞記事は `for_top_page/20140420yomiuri.pdf` から記事部分を切り出したもの（旧リンク先 `newspaper/yomiuri1404.pdf` は欠落していた）。
動画は Codex が作った軽量版（`assets/media/jet-*-stream.mp4`）を再生し、元の `movie/*.m4v` へのリンクも残している。
「視差効果を減らす」設定の端末では拡大の動きを止め、記事を普通に縦に並べる。

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

## アルバム・所思雑感（パスワード付きページ）

`private/index.html` は、アルバム（PL学園時代・鳥取大学時代・大学卒業後・家族）と所思雑感（新しい順）を1ページにまとめたもの。
GitHub Pages ではサーバー側でアクセスを制限できないため、ページの中身と写真を暗号化して公開し、ブラウザでパスワードを入れると復号して表示する。

- 元のページと写真: `_private_src/`（git で管理する。先頭が `_` のフォルダは GitHub Pages が公開しないので、サイトの URL からは開けない。GitHub のリポジトリ画面では見える）
  - `_private_src/index.html` … ページ本体。編集はここで行う
  - `_private_src/album/…`、`_private_src/shoshi.gif` … ページ内の画像
- 暗号化して書き出す（パスワードを画面で2回入力。表示されない）:

```bash
node tools/encrypt_private.mjs
```

- 書き出された `private/index.html` だけをコミットする。写真はページに埋め込まれて一緒に暗号化される。
- パスワードを変えるときも同じコマンドを実行し直す（「この端末で記憶する」で記憶した端末も入力し直しになる）。
- 暗号方式は PBKDF2-SHA256（60万回）＋ AES-256-GCM。短いパスワードは総当たりで破られうるので、10文字以上を推奨。
- 以前の公開版（`shoshi/`、`private/album/` の HTML と写真）は git の履歴には残っている。

## 大容量配布ファイル

`medical_DL/配布用FVP.zip`（約106MB）は GitHub の上限を超えるため、Google Drive で配布:

- 共有リンク: https://drive.google.com/file/d/1v221r7bXGNi25uzcTgdJtjk4PJNGkRGF/view?usp=sharing
- リンク元: `index_fvp.html`
