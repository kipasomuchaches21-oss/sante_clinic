// ── ШАПКА СКРОЛЛ ─────────────────────────────────
window.addEventListener('scroll', () => {
  document.getElementById('header').classList.toggle('header--scrolled', window.scrollY > 20);
});

// ── БУРГЕР МЕНЮ ──────────────────────────────────
document.getElementById('burger')?.addEventListener('click', () => {
  document.getElementById('nav').classList.toggle('open');
});

// ── УМНЫЙ ПОИСК ──────────────────────────────────
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
let searchTimer;

searchInput?.addEventListener('input', () => {
  clearTimeout(searchTimer);
  const q = searchInput.value.trim();
  if (q.length < 2) { searchResults.classList.remove('open'); return; }
  searchTimer = setTimeout(async () => {
    const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    if (!data.length) { searchResults.classList.remove('open'); return; }
    searchResults.innerHTML = data.map(item => `
      <a href="${item.url}" class="search-result-item">
        <span class="title">${item.title}</span>
        <span class="section">${item.section}</span>
      </a>
    `).join('');
    searchResults.classList.add('open');
  }, 280);
});

searchInput?.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    window.location.href = `/search?q=${encodeURIComponent(searchInput.value)}`;
  }
});

document.addEventListener('click', e => {
  if (!e.target.closest('.search-wrap')) searchResults?.classList.remove('open');
});

// ── МОДАЛЬНЫЕ ОКНА ───────────────────────────────
function openModal(type) {
  document.getElementById('modalOverlay').classList.add('open');
  document.querySelectorAll('.modal').forEach(m => m.classList.remove('open'));
  document.getElementById(`modal-${type}`)?.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('modalOverlay').classList.remove('open');
  document.querySelectorAll('.modal').forEach(m => m.classList.remove('open'));
  document.body.style.overflow = '';
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

// ── ОТПРАВКА ФОРМ ─────────────────────────────────
async function submitForm(e, type) {
  e.preventDefault();
  const form = e.target;
  const data = Object.fromEntries(new FormData(form));
  try {
    const res = await fetch(`/api/${type}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const json = await res.json();
    document.querySelectorAll('.modal').forEach(m => m.classList.remove('open'));
    document.getElementById('successText').textContent = json.message;
    document.getElementById('modal-success').classList.add('open');
    form.reset();
  } catch {
    alert('Ошибка. Попробуйте позже.');
  }
}

// ── АККОРДЕОН FAQ ─────────────────────────────────
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const wasOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    if (!wasOpen) item.classList.add('open');
  });
});

// ── ПОДПИСКА ──────────────────────────────────────
document.querySelector('.subscribe-form')?.addEventListener('submit', e => {
  e.preventDefault();
  const input = e.target.querySelector('input');
  alert(`Спасибо! ${input.value} добавлен в рассылку.`);
  input.value = '';
});

// ── АНИМАЦИЯ ПОЯВЛЕНИЯ ───────────────────────────
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.service-card, .doctor-card, .review-card, .blog-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity .5s ease, transform .5s ease';
  observer.observe(el);
});
