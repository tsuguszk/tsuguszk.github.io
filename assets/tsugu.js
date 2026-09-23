/* トップ下半分・報道・学会ページの動き
   1. [data-reveal] をスクロールでふわっと表示
   2. .zs（新聞記事）をスクロールに合わせて、全体表示 → 文字が読める大きさまで拡大 → 次の箇所へ移動 → 縮小
   3. 記事の拡大ビューア
   4. 学会ページの年ナビの現在地表示 */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('nx-js');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  function ease(u) { return u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; }

  /* ---------- 1. ふわっと表示 ---------- */
  var reveals = document.querySelectorAll('.nx [data-reveal]');
  if ('IntersectionObserver' in window && !reduceMotion.matches) {
    var revealer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); revealer.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: .06 });
    reveals.forEach(function (el) { revealer.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- 2. 記事の超拡大スクロール ----------
     data-char : 元画像での本文1文字の大きさ(px)
     data-path : 読む順に並べた注目点 [{x,y,z,w,t,h}]
       x,y 画像内の位置(0〜1) / z 拡大度(0=全体, 1=本文が読める大きさ)
       w   その箇所の幅(0〜1)。横書きの行が画面からはみ出さないよう倍率を抑える
       t   表示する説明 / h その箇所で止まる長さ(画面の高さ単位) */
  var TRANSITION = .7;

  function Story(sec) {
    this.sec = sec;
    this.stage = sec.querySelector('.zs-stage');
    this.view = sec.querySelector('.zs-view');
    this.img = sec.querySelector('.zs-img');
    this.cap = sec.querySelector('.zs-cap');
    this.step = sec.querySelector('.zs-step');
    this.bar = sec.querySelector('.zs-bar');
    this.W = +this.img.getAttribute('width');
    this.H = +this.img.getAttribute('height');
    this.charPx = +sec.getAttribute('data-char') || 30;

    var path = JSON.parse(sec.getAttribute('data-path') || '[]');
    var S = [{ x: .5, y: .5, k: .6, o: .2, h: 0, label: '' },
             { x: .5, y: .5, z: 0, o: 1, h: .4, label: '全体' }];
    path.forEach(function (p, i) {
      S.push({ x: p.x, y: p.y, z: p.z == null ? 1 : p.z, w: p.w, o: 1, h: p.h == null ? .5 : p.h,
               label: (i + 1) + ' / ' + path.length + '　' + (p.t || '') });
    });
    S.push({ x: .5, y: .5, z: 0, o: 1, h: .3, label: '全体' });
    S.push({ x: .5, y: .5, k: .6, o: .2, h: 0, label: '' });

    var t = 0;
    S.forEach(function (s, i) { s.start = t; t += s.h; if (i < S.length - 1) { t += TRANSITION; } });
    this.S = S;
    this.len = t;
    this.lastLabel = null;
    sec.style.setProperty('--zs-len', (this.len + 1).toFixed(3));
    sec.classList.add('zs-on');
  }

  Story.prototype.layout = function () {
    var vw = this.view.clientWidth, vh = this.view.clientHeight;
    if (!vw || !vh) { return; }
    var capRect = this.cap.getBoundingClientRect(), viewRect = this.view.getBoundingClientRect();
    var side = vw >= 1000 && vw / vh > 1.1;
    // 画像を見せる領域（説明パネルに隠れない部分）
    var R = side
      ? { x0: capRect.right - viewRect.left + 20, x1: vw, y0: 0, y1: vh }
      : { x0: 0, x1: vw, y0: 0, y1: capRect.top - viewRect.top - 10 };
    if (R.y1 - R.y0 < vh * .45) { R.y1 = vh; }
    var padX = vw < 600 ? 12 : 36, padY = vw < 600 ? 14 : 26;
    var fit = Math.min((R.x1 - R.x0 - 2 * padX) / this.W, (R.y1 - R.y0 - 2 * padY) / this.H);
    var target = vw < 600 ? 17 : (vw < 1100 ? 19 : 21);
    var W = this.W, H = this.H, charPx = this.charPx;

    this.R = R;
    this.cx = (R.x0 + R.x1) / 2;
    this.cy = (R.y0 + R.y1) / 2;
    this.V = this.S.map(function (s) {
      var sc;
      if (s.k) {
        sc = fit * s.k;
      } else {
        var read = target / charPx;
        if (s.w) { read = Math.min(read, (R.x1 - R.x0) * .94 / (s.w * W)); }
        read = Math.max(read, fit * 1.05);
        sc = fit * Math.pow(read / fit, s.z);
      }
      // 画面を覆える大きさなら、画像の端が領域の内側に入り込まないよう注目点を寄せる
      var hw = (R.x1 - R.x0) / 2 / sc, hh = (R.y1 - R.y0) / 2 / sc;
      var cx = W <= 2 * hw ? W / 2 : clamp(s.x * W, hw, W - hw);
      var cy = H <= 2 * hh ? H / 2 : clamp(s.y * H, hh, H - hh);
      return { s: sc, cx: cx, cy: cy, o: s.o };
    });
    this.sMax = Math.max.apply(null, this.V.map(function (v) { return v.s; }));
    this.img.style.width = (W * this.sMax).toFixed(1) + 'px';
    this.img.style.height = (H * this.sMax).toFixed(1) + 'px';
  };

  Story.prototype.update = function () {
    var rect = this.sec.getBoundingClientRect();
    var vh = window.innerHeight;
    var near = rect.bottom > -vh * .5 && rect.top < vh * 1.5;
    this.sec.classList.toggle('zs-active', near);
    if (!near || !this.V) { return; }

    var travel = Math.max(1, this.sec.offsetHeight - this.stage.offsetHeight);
    var p = clamp(-rect.top / travel, 0, 1);
    var t = p * this.len;
    var S = this.S, V = this.V, a = V[0], b = V[0], u = 0, idx = 0;
    for (var i = 0; i < S.length; i++) {
      var holdEnd = S[i].start + S[i].h;
      if (t <= holdEnd || i === S.length - 1) { a = b = V[i]; idx = i; break; }
      if (t < S[i + 1].start) {
        u = ease((t - holdEnd) / TRANSITION);
        a = V[i]; b = V[i + 1]; idx = u < .5 ? i : i + 1;
        break;
      }
    }
    var s = Math.exp(Math.log(a.s) + (Math.log(b.s) - Math.log(a.s)) * u);
    var cx = a.cx + (b.cx - a.cx) * u;
    var cy = a.cy + (b.cy - a.cy) * u;
    var o = a.o + (b.o - a.o) * u;
    var tx = this.cx - s * cx, ty = this.cy - s * cy;
    this.img.style.transform = 'translate3d(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px,0) scale(' + (s / this.sMax).toFixed(5) + ')';
    this.img.style.opacity = o.toFixed(3);
    this.sec.style.setProperty('--zs-p', p.toFixed(4));
    this.sec.classList.toggle('zs-reading', S[idx].z > .5);

    var label = S[idx].label;
    if (this.step && label && label !== this.lastLabel) {
      this.step.querySelector('span').textContent = label;
      this.lastLabel = label;
    }
  };

  var stories = [];
  if (!reduceMotion.matches) {
    document.querySelectorAll('.nx .zs[data-path]').forEach(function (sec) { stories.push(new Story(sec)); });
  }

  var ticking = false;
  function frame() {
    ticking = false;
    for (var i = 0; i < stories.length; i++) { stories[i].update(); }
  }
  function requestFrame() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(frame); }
  }
  function relayout() {
    stories.forEach(function (st) { st.layout(); });
    requestFrame();
  }
  if (stories.length) {
    relayout();
    var lastW = window.innerWidth, lastH = window.innerHeight;
    window.addEventListener('scroll', requestFrame, { passive: true });
    window.addEventListener('resize', function () {
      // iPhone のアドレスバーの出入りによる小さな高さ変化では組み直さない
      if (window.innerWidth !== lastW || Math.abs(window.innerHeight - lastH) > 120) {
        lastW = window.innerWidth; lastH = window.innerHeight; relayout();
      } else {
        requestFrame();
      }
    });
    window.addEventListener('orientationchange', function () { setTimeout(relayout, 300); });
    window.addEventListener('load', relayout);
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(relayout); }
  }

  /* ---------- 3. 拡大ビューア ---------- */
  var viewer = document.getElementById('nx-viewer');
  if (viewer && typeof viewer.showModal === 'function') {
    var vImg = viewer.querySelector('img');
    var vTitle = viewer.querySelector('[data-v-title]');
    var scroller = viewer.querySelector('.scroller');
    var zoom = 1, baseW = 0;

    function setZoom(z) {
      var cxr = (scroller.scrollLeft + scroller.clientWidth / 2) / Math.max(1, scroller.scrollWidth);
      var cyr = (scroller.scrollTop + scroller.clientHeight / 2) / Math.max(1, scroller.scrollHeight);
      zoom = clamp(z, .25, 2.5);
      vImg.style.width = Math.round(baseW * zoom) + 'px';
      scroller.scrollLeft = cxr * scroller.scrollWidth - scroller.clientWidth / 2;
      scroller.scrollTop = cyr * scroller.scrollHeight - scroller.clientHeight / 2;
    }

    document.querySelectorAll('[data-viewer]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var W = +btn.getAttribute('data-w'), charPx = +btn.getAttribute('data-char') || 30;
        var target = window.innerWidth < 600 ? 17 : 21;
        baseW = W * target / charPx;
        zoom = 1;
        vImg.alt = btn.getAttribute('data-title') || '';
        vTitle.textContent = btn.getAttribute('data-title') || '記事';
        vImg.style.width = Math.round(baseW) + 'px';
        vImg.src = btn.getAttribute('data-viewer');
        viewer.showModal();
        var rtl = btn.getAttribute('data-dir') === 'rtl';
        requestAnimationFrame(function () {
          scroller.scrollTop = 0;
          scroller.scrollLeft = rtl ? scroller.scrollWidth : 0;
        });
      });
    });
    viewer.querySelector('[data-v-in]').addEventListener('click', function () { setZoom(zoom * 1.25); });
    viewer.querySelector('[data-v-out]').addEventListener('click', function () { setZoom(zoom / 1.25); });
    viewer.querySelector('[data-v-close]').addEventListener('click', function () { viewer.close(); });
    viewer.addEventListener('close', function () { vImg.removeAttribute('src'); });
  }

  /* ---------- 4. 年ナビの現在地 ---------- */
  var yearnav = document.querySelector('.nx .yearnav');
  if (yearnav && 'IntersectionObserver' in window) {
    var links = {};
    yearnav.querySelectorAll('a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var yearObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) { return; }
        var a = links[e.target.id];
        if (!a) { return; }
        Object.keys(links).forEach(function (k) { links[k].classList.remove('is-cur'); });
        a.classList.add('is-cur');
        yearnav.scrollTo({ left: a.offsetLeft - yearnav.clientWidth / 2 + a.offsetWidth / 2, behavior: 'smooth' });
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    document.querySelectorAll('.nx .year[id]').forEach(function (y) { yearObserver.observe(y); });
  }
}());
