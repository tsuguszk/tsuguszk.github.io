(function () {
  'use strict';

  const stories = Array.from(document.querySelectorAll('[data-story]'));
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const narrowScreen = window.matchMedia('(max-width: 780px)');
  let ticking = false;

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function updateStories() {
    ticking = false;
    if (reducedMotion.matches || narrowScreen.matches) {
      stories.forEach(function (story) {
        story.style.setProperty('--story-scale', '1');
        story.style.setProperty('--story-opacity', '1');
      });
      return;
    }

    stories.forEach(function (story) {
      const rect = story.getBoundingClientRect();
      const travel = Math.max(1, rect.height - window.innerHeight);
      const progress = clamp(-rect.top / travel, 0, 1);
      let scale;
      if (story.dataset.storyMode === 'grow') {
        scale = .68 + (.32 * Math.min(progress / .44, 1));
      } else if (progress < .27) {
        scale = .68 + (.32 * progress / .27);
      } else if (progress < .72) {
        scale = 1;
      } else {
        scale = 1 - (.32 * (progress - .72) / .28);
      }
      story.style.setProperty('--story-scale', scale.toFixed(3));
      story.style.setProperty('--story-opacity', String(clamp(.72 + scale * .28, .7, 1)));
    });
  }

  function requestUpdate() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(updateStories);
    }
  }

  if (stories.length) {
    updateStories();
    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate);
    reducedMotion.addEventListener('change', requestUpdate);
    narrowScreen.addEventListener('change', requestUpdate);
  }

  const zoomDialog = document.getElementById('zoom-dialog');
  if (zoomDialog) {
    const zoomImage = zoomDialog.querySelector('img');
    const zoomTitle = zoomDialog.querySelector('[data-zoom-title]');
    document.querySelectorAll('[data-zoom-image]').forEach(function (button) {
      button.addEventListener('click', function () {
        zoomImage.src = button.dataset.zoomImage;
        zoomImage.alt = button.dataset.zoomAlt || '';
        zoomTitle.textContent = button.dataset.zoomAlt || '記事を拡大';
        zoomDialog.showModal();
      });
    });
    zoomDialog.querySelector('[data-close-zoom]').addEventListener('click', function () {
      zoomDialog.close();
    });
    zoomDialog.addEventListener('click', function (event) {
      if (event.target === zoomDialog) zoomDialog.close();
    });
    zoomDialog.addEventListener('close', function () {
      zoomImage.removeAttribute('src');
    });
  }
}());
