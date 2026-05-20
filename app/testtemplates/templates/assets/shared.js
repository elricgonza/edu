/* ============================================================
   SISTEMA ESCOLAR — shared.js
   Sidebar active link, modal helpers, search/filter, confirm dialog
   ============================================================ */

// ── Active nav link ──────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const page = location.pathname.split('/').pop();
  document.querySelectorAll('.nav-item').forEach(el => {
    if (el.dataset.page === page || el.dataset.page === page.replace('.html',''))
      el.classList.add('active');
  });
});

// ── Modal helpers ────────────────────────────────────────────
function openModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.add('open');
}
function closeModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.remove('open');
}
// Close on overlay click
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay')) e.target.classList.remove('open');
});

// ── Toast notification ────────────────────────────────────────
function showToast(msg, type = 'success') {
  const icons = { success: '✅', danger: '❌', info: 'ℹ️', warning: '⚠️' };
  const t = document.createElement('div');
  t.className = `alert alert-${type}`;
  t.style.cssText = `position:fixed;top:20px;right:20px;z-index:9999;min-width:280px;
    box-shadow:0 8px 32px rgba(26,43,74,.18);animation:toastIn .3s ease;`;
  t.innerHTML = `<span>${icons[type] || '📌'}</span> ${msg}`;
  document.body.appendChild(t);
  setTimeout(() => { t.style.opacity='0'; t.style.transition='opacity .3s'; setTimeout(()=>t.remove(),300); }, 3000);
}
// toast animation
const s = document.createElement('style');
s.textContent = `@keyframes toastIn{from{transform:translateX(40px);opacity:0}to{transform:none;opacity:1}}`;
document.head.appendChild(s);

// ── Confirm dialog (replaces browser confirm) ────────────────
function confirmAction(msg, onConfirm) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay open';
  overlay.innerHTML = `
    <div class="modal" style="max-width:420px">
      <div class="modal-header">
        <div class="modal-icon">⚠️</div>
        <span class="modal-title">Confirmar acción</span>
      </div>
      <div class="modal-body"><p style="font-size:14px;color:var(--text)">${msg}</p></div>
      <div class="modal-footer">
        <button class="btn btn-ghost" id="cfNo">Cancelar</button>
        <button class="btn btn-danger" id="cfYes">🗑️ Confirmar</button>
      </div>
    </div>`;
  document.body.appendChild(overlay);
  overlay.querySelector('#cfNo').onclick  = () => overlay.remove();
  overlay.querySelector('#cfYes').onclick = () => { overlay.remove(); onConfirm(); };
}

// ── Live table search ────────────────────────────────────────
function bindSearch(inputId, tableId) {
  const input = document.getElementById(inputId);
  const tbody = document.querySelector(`#${tableId} tbody`);
  if (!input || !tbody) return;
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase().trim();
    tbody.querySelectorAll('tr').forEach(row => {
      row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
}

// ── Column filter (select) ────────────────────────────────────
function bindFilter(selectId, tableId, colIndex) {
  const sel = document.getElementById(selectId);
  const tbody = document.querySelector(`#${tableId} tbody`);
  if (!sel || !tbody) return;
  sel.addEventListener('change', () => {
    const v = sel.value.toLowerCase();
    tbody.querySelectorAll('tr').forEach(row => {
      const cell = row.cells[colIndex];
      row.style.display = (!v || (cell && cell.textContent.toLowerCase().includes(v))) ? '' : 'none';
    });
  });
}

// ── Simple sortable headers ───────────────────────────────────
function makeSortable(tableId) {
  const table = document.getElementById(tableId);
  if (!table) return;
  const ths = table.querySelectorAll('thead th[data-sort]');
  ths.forEach((th, i) => {
    th.style.cursor = 'pointer';
    th.title = 'Clic para ordenar';
    let asc = true;
    th.addEventListener('click', () => {
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.rows);
      rows.sort((a, b) => {
        const av = a.cells[parseInt(th.dataset.sort)].textContent.trim().toLowerCase();
        const bv = b.cells[parseInt(th.dataset.sort)].textContent.trim().toLowerCase();
        return asc ? av.localeCompare(bv) : bv.localeCompare(av);
      });
      asc = !asc;
      rows.forEach(r => tbody.appendChild(r));
      ths.forEach(t => t.innerHTML = t.innerHTML.replace(/ [▲▼]$/,''));
      th.innerHTML = th.innerHTML + (asc ? ' ▼' : ' ▲');
    });
  });
}
