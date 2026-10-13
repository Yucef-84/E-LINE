const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');

function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', '메뉴 열기');
  mobileNav.classList.remove('is-open');
  mobileNav.inert = true;
}

menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
  mobileNav.classList.toggle('is-open', open);
  mobileNav.inert = !open;
});
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
window.matchMedia('(min-width: 601px)').addEventListener('change', event => {
  if (event.matches) closeMenu();
});

const cards = [...document.querySelectorAll('.photo-card')];
const filters = [...document.querySelectorAll('[data-filter]')];
const grid = document.querySelector('.photo-grid');
const galleryStatus = document.querySelector('#gallery-status');
let visibleCards = [...cards];

filters.forEach(filter => filter.addEventListener('click', () => {
  const category = filter.dataset.filter;
  filters.forEach(button => button.setAttribute('aria-pressed', String(button === filter)));
  cards.forEach(card => { card.hidden = category !== 'all' && card.dataset.category !== category; });
  visibleCards = cards.filter(card => !card.hidden);
  grid.classList.toggle('is-filtered', category !== 'all');
  galleryStatus.textContent = `${filter.textContent.trim().replace(/\s+12$/, '')} 사진 ${visibleCards.length}장을 표시합니다.`;
}));

const lightbox = document.querySelector('.lightbox');
const lightboxImage = document.querySelector('#lightbox-image');
const lightboxTitle = document.querySelector('#lightbox-title');
const lightboxCategory = document.querySelector('#lightbox-category');
const lightboxCounter = document.querySelector('#lightbox-counter');
let activeIndex = 0;
let openingCard;

function showImage(index) {
  activeIndex = (index + visibleCards.length) % visibleCards.length;
  const card = visibleCards[activeIndex];
  lightboxImage.src = `assets/images/${card.dataset.image}-1200.webp`;
  lightboxImage.alt = card.querySelector('img').alt;
  lightboxTitle.textContent = card.dataset.title;
  lightboxCategory.textContent = card.dataset.note;
  lightboxCounter.textContent = `${String(activeIndex + 1).padStart(2, '0')} / ${String(visibleCards.length).padStart(2, '0')}`;
}

cards.forEach(card => card.addEventListener('click', () => {
  openingCard = card;
  showImage(visibleCards.indexOf(card));
  lightbox.showModal();
  document.body.classList.add('modal-open');
}));
document.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
document.querySelector('.lightbox-prev').addEventListener('click', () => showImage(activeIndex - 1));
document.querySelector('.lightbox-next').addEventListener('click', () => showImage(activeIndex + 1));
lightbox.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    showImage(activeIndex + (event.key === 'ArrowLeft' ? -1 : 1));
  }
});
lightbox.addEventListener('click', event => {
  if (event.target !== lightbox) return;
  const bounds = lightbox.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) lightbox.close();
});
lightbox.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  lightboxImage.removeAttribute('src');
  openingCard?.focus({ preventScroll: true });
});

let touchStartX;
lightboxImage.addEventListener('touchstart', event => { touchStartX = event.changedTouches[0].clientX; }, { passive: true });
lightboxImage.addEventListener('touchend', event => {
  if (touchStartX === undefined) return;
  const distance = event.changedTouches[0].clientX - touchStartX;
  if (Math.abs(distance) > 55) showImage(activeIndex + (distance < 0 ? 1 : -1));
  touchStartX = undefined;
}, { passive: true });

document.querySelector('.copy-email').addEventListener('click', async () => {
  const status = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText('nedjma@steibu.com');
    status.textContent = '이메일 주소를 복사했습니다.';
  } catch {
    status.textContent = '주소를 직접 복사해 주세요: nedjma@steibu.com';
  }
});
document.querySelector('#year').textContent = String(new Date().getFullYear());

if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.about-intro, .about-bottom, .section-heading, .casting-layout, .profile-layout, .downloads, .contact-main').forEach(element => {
    element.classList.add('reveal');
    observer.observe(element);
  });
  document.documentElement.classList.add('motion-ready');
}
