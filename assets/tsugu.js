/* トップ下半分・報道・学会ページの動き
   0. ヘッダーの実際の高さを測ってCSS変数に反映
   1. [data-reveal] をスクロールでふわっと表示
   2. .zs（新聞記事）をスクロールに合わせて約30%拡大
   3. 記事の拡大ビューア
   4. 学会ページの年ナビの現在地表示
   5. 写真の拡大表示（ロードバイクのページ） */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('nx-js');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  function ease(u) { return u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; }

  /* ---------- 0. ヘッダーの実際の高さ ----------
     --nav-h はCSSで決め打ちの目安値。実機（特にiPad Safari）では
     env(safe-area-inset-top) 等の分だけヘッダーが --nav-h より高くなることがあり、
     決め打ちのままだとヘッダー直下に置いた要素（スクロール進行バー・年ナビ等）が
     ヘッダーの下に隠れてしまう。ここで実際の高さを測って --header-h に反映し、
     ヘッダーの下端を基準にする箇所はすべて --header-h を使う。 */
  var localnav = document.querySelector('.nx .localnav');
  var nxRoot = document.querySelector('.nx');
  if (localnav && nxRoot) {
    var syncHeaderHeight = function () {
      var h = localnav.offsetHeight;
      // --header-h は .nx 自身が既定値(var(--nav-h))を持つため、
      // 祖先(html等)ではなく .nx 自身に設定しないと上書きできない
      if (h) { nxRoot.style.setProperty('--header-h', h + 'px'); }
    };
    syncHeaderHeight();
    if ('ResizeObserver' in window) {
      new ResizeObserver(syncHeaderHeight).observe(localnav);
    } else {
      window.addEventListener('resize', syncHeaderHeight);
    }
    window.addEventListener('orientationchange', function () { setTimeout(syncHeaderHeight, 300); });
    window.addEventListener('load', syncHeaderHeight);
  }

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

  /* ---------- 2. 記事のスクロール拡大 ----------
     記事1本あたり画面1枚弱のスクロールで、全体表示 → 注目点に向かって約30%拡大。
     文字を読むのは「記事を拡大して読む」ボタンの役目なので、ここでは操作の軽さを優先する。
     data-focus : 拡大の中心 "x,y"（画像内の位置 0〜1）。省略時は中央
     data-zoom  : 最大倍率（全体表示に対する倍率）。省略時は 1.3 */
  var TRAVEL = .75;            // 固定表示している間のスクロール量（画面の高さ単位）

  function Story(sec) {
    this.sec = sec;
    this.stage = sec.querySelector('.zs-stage');
    this.view = sec.querySelector('.zs-view');
    this.img = sec.querySelector('.zs-img');
    this.cap = sec.querySelector('.zs-cap');
    this.W = +this.img.getAttribute('width');
    this.H = +this.img.getAttribute('height');
    var f = (sec.getAttribute('data-focus') || '.5,.5').split(',');
    this.fx = +f[0]; this.fy = +f[1];
    this.zoom = +sec.getAttribute('data-zoom') || 1.3;
    sec.style.setProperty('--zs-len', (1 + TRAVEL).toFixed(2));
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
    this.fit = Math.min((R.x1 - R.x0 - 2 * padX) / this.W, (R.y1 - R.y0 - 2 * padY) / this.H);
    this.R = R;
    this.sMax = this.fit * this.zoom;
    this.img.style.width = (this.W * this.sMax).toFixed(1) + 'px';
    this.img.style.height = (this.H * this.sMax).toFixed(1) + 'px';
  };

  Story.prototype.update = function () {
    var rect = this.sec.getBoundingClientRect();
    var vh = window.innerHeight;
    var near = rect.bottom > -vh * .5 && rect.top < vh * 1.5;
    this.sec.classList.toggle('zs-active', near);
    if (!near || !this.R) { return; }

    var travel = Math.max(1, this.sec.offsetHeight - this.stage.offsetHeight);
    // 固定表示になる少し前（画面に入ってくる間）から動き始める
    var p = clamp((-rect.top + vh * .35) / (travel + vh * .35), 0, 1);
    var u = ease(clamp(p / .85, 0, 1));
    var s = this.fit * (.92 + (this.zoom - .92) * u);
    var R = this.R, W = this.W, H = this.H;
    var hw = (R.x1 - R.x0) / 2 / s, hh = (R.y1 - R.y0) / 2 / s;
    var fx = .5 + (this.fx - .5) * u, fy = .5 + (this.fy - .5) * u;
    var cx = W <= 2 * hw ? W / 2 : clamp(fx * W, hw, W - hw);
    var cy = H <= 2 * hh ? H / 2 : clamp(fy * H, hh, H - hh);
    var tx = (R.x0 + R.x1) / 2 - s * cx, ty = (R.y0 + R.y1) / 2 - s * cy;
    this.img.style.transform = 'translate3d(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px,0) scale(' + (s / this.sMax).toFixed(5) + ')';
    this.img.style.opacity = (.35 + .65 * clamp(p / .25, 0, 1)).toFixed(3);
    this.sec.style.setProperty('--zs-p', p.toFixed(4));
  };

  var stories = [];
  if (!reduceMotion.matches) {
    document.querySelectorAll('.nx .zs').forEach(function (sec) { stories.push(new Story(sec)); });
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

  /* ---------- 5. 写真の拡大表示 ---------- */
  var lb = document.getElementById('nx-lightbox');
  if (lb && typeof lb.showModal === 'function') {
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption');
    document.querySelectorAll('[data-lightbox]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var img = btn.querySelector('img');
        var cap = btn.parentElement.querySelector('figcaption');
        // 表示する大きさを画面から計算して px で指定する。
        // Safari は拡大表示の枠の幅を説明文の長さで決めてしまい、写真が小さく出ることがあるため
        var w = +(img.naturalWidth || img.getAttribute('width')), h = +(img.naturalHeight || img.getAttribute('height'));
        if (w && h) {
          var s = Math.min(1, Math.min(window.innerWidth * 0.96, 1200) / w, (window.innerHeight * 0.94 - 60) / h);
          lbImg.style.width = Math.round(w * s) + 'px';
          lbImg.style.height = Math.round(h * s) + 'px';
          lbCap.style.width = Math.round(w * s) + 'px';
        } else {
          lbImg.style.width = lbImg.style.height = lbCap.style.width = '';
        }
        lbImg.src = img.currentSrc || img.src;
        lbImg.alt = img.alt;
        lbCap.textContent = cap ? cap.textContent : '';
        var open = function () { if (!lb.open) { lb.showModal(); } };
        if (lbImg.decode) { lbImg.decode().then(open, open); } else { open(); }
      });
    });
    lb.querySelector('[data-lb-close]').addEventListener('click', function () { lb.close(); });
    lb.addEventListener('click', function (e) { if (e.target === lb) { lb.close(); } });
    lb.addEventListener('close', function () { lbImg.removeAttribute('src'); });
  }
}());
