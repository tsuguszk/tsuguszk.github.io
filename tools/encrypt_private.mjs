#!/usr/bin/env node
/*
 * アルバム・所思雑感ページをパスワードで暗号化して公開用に書き出す。
 *
 *   node tools/encrypt_private.mjs
 *
 * - 元のページ: _private_src/index.html（写真も _private_src/ に置く。先頭が _ のフォルダは GitHub Pages で公開されない）
 * - 書き出し先: private/index.html（暗号化済み。これだけを公開する）
 * - _private_src/ 内の画像はページに埋め込んでから暗号化するので、写真もパスワードなしでは見られない。
 *   ../ で始まるサイト共通の画像（背景・タイトル画像など）は埋め込まずにそのまま参照する。
 * - パスワードは実行時に画面で2回入力する（画面には表示されない）。どこにも保存しない。
 * - 暗号方式: PBKDF2-SHA256（60万回）で鍵を作り、AES-256-GCM で暗号化。ブラウザ側で復号する。
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { webcrypto } from 'node:crypto';
import readline from 'node:readline';

const crypto = webcrypto;
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC_DIR = join(ROOT, '_private_src');
const SRC = join(SRC_DIR, 'index.html');
const OUT = join(ROOT, 'private', 'index.html');
const ITERATIONS = 600000;
const MIME = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp' };

function inlineImages(html) {
  let count = 0;
  const out = html.replace(/(<img\b[^>]*?\bsrc=")([^"]+)(")/gi, (m, before, src, after) => {
    if (/^(https?:|data:|\.\.\/)/i.test(src)) { return m; }
    const file = join(SRC_DIR, src);
    const mime = MIME[extname(file).toLowerCase()];
    if (!mime || !existsSync(file)) { throw new Error('画像が見つかりません: _private_src/' + src); }
    count++;
    return before + 'data:' + mime + ';base64,' + readFileSync(file).toString('base64') + after;
  });
  return { html: out, count };
}

function askHidden(question) {
  return new Promise((res) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: true });
    rl._writeToOutput = (s) => { if (s.includes(question)) { rl.output.write(question); } };
    rl.question(question, (answer) => { rl.close(); process.stdout.write('\n'); res(answer); });
  });
}

const b64 = (u8) => Buffer.from(u8).toString('base64');

async function main() {
  if (!existsSync(SRC)) { throw new Error('元のページがありません: ' + SRC); }
  const { html, count } = inlineImages(readFileSync(SRC, 'utf8'));

  const pw1 = await askHidden('パスワード: ');
  if (pw1.length < 6) { throw new Error('パスワードは6文字以上にしてください'); }
  const pw2 = await askHidden('もう一度: ');
  if (pw1 !== pw2) { throw new Error('2回の入力が一致しません'); }

  const enc = new TextEncoder();
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const base = await crypto.subtle.importKey('raw', enc.encode(pw1), 'PBKDF2', false, ['deriveKey']);
  const key = await crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: ITERATIONS, hash: 'SHA-256' },
    base, { name: 'AES-GCM', length: 256 }, false, ['encrypt']);
  const data = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(html)));

  const payload = JSON.stringify({ v: 1, it: ITERATIONS, s: b64(salt), iv: b64(iv), d: b64(data) });
  writeFileSync(OUT, page(payload));
  console.log(`書き出しました: private/index.html（写真 ${count} 枚を埋め込み、${(data.length / 1024 / 1024).toFixed(1)} MB）`);
}

function page(payload) {
  return `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>アルバム・所思雑感</title>
  <style>
    body { margin: 0; padding: 16px; background: #8bf5c5 url("../for_top_page/gif/back.gif"); color: #17372c; text-align: center;
      font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans JP", Meiryo, sans-serif; }
    .box { max-width: 360px; margin: 24px auto; padding: 24px 22px; border-radius: 16px; background: rgba(255,255,255,.85); box-shadow: 0 10px 30px -14px rgba(8,58,38,.4); }
    h1 { margin: 0 0 6px; font-size: 1.25rem; }
    p { margin: 6px 0 14px; font-size: .9rem; color: #4d7262; }
    input[type=password] { box-sizing: border-box; width: 100%; padding: 10px 12px; border: 1px solid #bcd; border-radius: 10px; font-size: 16px; }
    label.rem { display: block; margin: 10px 0 0; font-size: .85rem; color: #4d7262; }
    button { margin-top: 14px; width: 100%; min-height: 44px; border: 0; border-radius: 999px; background: #0e3a2a; color: #fff; font-size: 1rem; font-weight: 700; cursor: pointer; }
    .err { min-height: 1.4em; margin: 10px 0 0; color: #a3372c; font-size: .9rem; }
    a { color: #006600; }
  </style>
</head>
<body>
  <p><a href="../index.html" aria-label="トップページへ"><img src="../for_top_page/gif/title.gif" width="273" height="84" alt="つぐとしのweb site" style="max-width:100%;height:auto;border:0;"></a></p>
  <form class="box" id="f">
    <h1>アルバム・所思雑感</h1>
    <p>このページはパスワードが必要です。</p>
    <input type="password" id="pw" autocomplete="current-password" placeholder="パスワード" required autofocus>
    <label class="rem"><input type="checkbox" id="rem"> この端末で記憶する</label>
    <button type="submit" id="go">開く</button>
    <div class="err" id="err" role="alert"></div>
  </form>
  <p><a href="../index.html">トップページへ戻る</a></p>
  <script id="payload" type="application/json">${payload}</script>
  <script>
  (function () {
    var P = JSON.parse(document.getElementById('payload').textContent);
    var STORE = 'tsugu-private-key';
    function u8(b) { return Uint8Array.from(atob(b), function (c) { return c.charCodeAt(0); }); }
    function b64(buf) { return btoa(String.fromCharCode.apply(null, new Uint8Array(buf))); }
    async function open(key) {
      var plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: u8(P.iv) }, key, u8(P.d));
      var html = new TextDecoder().decode(plain);
      document.open(); document.write(html); document.close();
    }
    async function derive(pw) {
      var base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveKey']);
      return crypto.subtle.deriveKey({ name: 'PBKDF2', salt: u8(P.s), iterations: P.it, hash: 'SHA-256' },
        base, { name: 'AES-GCM', length: 256 }, true, ['decrypt']);
    }
    // 記憶した鍵があれば自動で開く（暗号化し直すと無効になる）
    try {
      var saved = JSON.parse(localStorage.getItem(STORE) || 'null');
      if (saved && saved.s === P.s) {
        crypto.subtle.importKey('raw', u8(saved.k), 'AES-GCM', false, ['decrypt']).then(open)
          .catch(function () { localStorage.removeItem(STORE); });
      }
    } catch (e) {}
    document.getElementById('f').addEventListener('submit', async function (ev) {
      ev.preventDefault();
      var btn = document.getElementById('go'), err = document.getElementById('err');
      btn.disabled = true; btn.textContent = '確認中…'; err.textContent = '';
      try {
        var key = await derive(document.getElementById('pw').value);
        if (document.getElementById('rem').checked) {
          try { localStorage.setItem(STORE, JSON.stringify({ s: P.s, k: b64(await crypto.subtle.exportKey('raw', key)) })); } catch (e) {}
        }
        await open(key);
      } catch (e) {
        err.textContent = 'パスワードが違います。';
        btn.disabled = false; btn.textContent = '開く';
      }
    });
  }());
  </script>
</body>
</html>
`;
}

main().catch((e) => { console.error('エラー: ' + e.message); process.exit(1); });
