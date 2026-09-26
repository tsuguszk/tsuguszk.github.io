/* アブレーションの成績ページの棒グラフのツールチップ（マウス・タップ・キーボードで同じ内容を出す）。
   棒 .ca-bar に data-tip（大きな数字）、data-name（何の棒か）、data-sub（補足）を書く。色は棒の .ca-fill から取る */
(function () {
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  document.querySelectorAll('.ocgh-abl .ca-plot').forEach(function (plot) {
    var tip = plot.querySelector('.ca-tip');
    if (!tip) return;
    var current = null;

    function show(bar) {
      if (current && current !== bar) current.classList.remove('is-on');
      current = bar;
      bar.classList.add('is-on');
      var d = bar.dataset;
      var fill = bar.querySelector('.ca-fill');
      tip.textContent = '';
      tip.appendChild(el('b', '', d.tip));
      var name = el('span', 't-name');
      var key = el('i');
      key.style.background = getComputedStyle(fill).backgroundColor;
      name.appendChild(key);
      name.appendChild(document.createTextNode(d.name));
      tip.appendChild(name);
      if (d.sub) tip.appendChild(el('span', 't-sub', d.sub));
      tip.hidden = false;

      var pr = plot.getBoundingClientRect();
      var fr = fill.getBoundingClientRect();
      var tw = tip.offsetWidth, th = tip.offsetHeight;
      var x = fr.left + fr.width / 2 - pr.left - tw / 2;
      x = Math.max(0, Math.min(x, pr.width - tw));
      var y = fr.top - pr.top - th - 8;
      if (y < 0) y = fr.top - pr.top + 8;
      tip.style.left = x + 'px';
      tip.style.top = y + 'px';
    }

    function hide() {
      tip.hidden = true;
      if (current) current.classList.remove('is-on');
      current = null;
    }

    plot.querySelectorAll('.ca-bar').forEach(function (bar) {
      bar.addEventListener('pointerenter', function () { show(bar); });
      bar.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse' && document.activeElement !== bar) hide(); });
      bar.addEventListener('focus', function () { show(bar); });
      bar.addEventListener('blur', hide);
      bar.addEventListener('click', function () { show(bar); });
    });
    document.addEventListener('pointerdown', function (e) {
      if (current && !plot.contains(e.target)) hide();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(); });
    window.addEventListener('resize', hide);
  });
}());
