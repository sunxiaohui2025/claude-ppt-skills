const slides = Array.from(document.querySelectorAll('.slide'));
const pageText = document.querySelector('#pageText');
const progressBar = document.querySelector('#progressBar');
const overview = document.querySelector('#overview');
const overviewGrid = document.querySelector('#overviewGrid');
const editorToast = document.querySelector('#editorToast');
const editToolbar = document.querySelector('#editToolbar');
const editTargetLabel = document.querySelector('#editTargetLabel');
let index = 0;
let editing = false;
let selectedEditElement = null;
let dragState = null;
let deckDirectoryHandle = null;
let htmlFileHandle = null;
let savedTextRange = null;
function toast(message) { editorToast.textContent = message; editorToast.classList.add('active'); clearTimeout(toast.timer); toast.timer = setTimeout(() => editorToast.classList.remove('active'), 3000); }
function showSlide(nextIndex) { index = Math.max(0, Math.min(slides.length - 1, nextIndex)); slides.forEach((slide, i) => slide.classList.toggle('active', i === index)); pageText.textContent = `${String(index + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`; progressBar.style.setProperty('--progress', `${((index + 1) / slides.length) * 100}%`); clearSelection(); }
function toggleOverview(force) { const active = force ?? !overview.classList.contains('active'); overview.classList.toggle('active', active); overview.setAttribute('aria-hidden', String(!active)); if (active) buildOverview(); }
function buildOverview() {
  overviewGrid.innerHTML = '';
  slides.forEach((slide, i) => {
    const card = document.createElement('button');
    card.className = 'overview-card';
    card.type = 'button';
    const iframe = document.createElement('iframe');
    const html = `<!doctype html><html><head><style>${document.querySelector('style').textContent}.footer,.overview,.editor-toast,.edit-toolbar{display:none!important}:root{--stage-top:58px;--stage-bottom:92px;--stage-x:90px}.slide{display:grid!important;position:relative!important;width:1280px!important;height:720px!important;min-width:1280px!important;min-height:720px!important}.slide-stage{transform:none}</style></head><body>${slide.outerHTML}</body></html>`;
    iframe.srcdoc = html;
    const label = document.createElement('span');
    label.textContent = `${i + 1}/${slides.length}`;
    card.append(iframe, label);
    card.addEventListener('click', () => { showSlide(i); toggleOverview(false); });
    overviewGrid.appendChild(card);
    requestAnimationFrame(() => {
      const rect = card.getBoundingClientRect();
      const scale = Math.max(rect.width / 1280, rect.height / 720);
      card.style.setProperty('--preview-scale', String(scale));
    });
  });
}
function textCandidates() { return 'h1,h2,h3,p,li,.claim,.kicker,.meta-tag,.reuse-tag,.chip,.label,.card-title,.grid-title,.hub-node-title'; }
function blockCandidates() { return '.card,.panel,.grid-item,.compare-card,.hub-node,.system-node,.reuse-tag,.delivery-card,.case-panel,.system-node,.metric-note,.story-step'; }
function editableCandidates() { return `${textCandidates()},${blockCandidates()}`; }
function labelForElement(el) { if (!el) return '未选择元素'; const role = el.dataset.role || el.className || el.tagName.toLowerCase(); return `${el.tagName.toLowerCase()} · ${String(role).split(' ')[0]}`; }
function clearSavedTextRange() { savedTextRange = null; }
function clearSelection() { selectedEditElement?.classList.remove('edit-selected'); selectedEditElement = null; clearSavedTextRange(); if (editTargetLabel) editTargetLabel.textContent = '未选择元素'; }
function selectEditElement(el) {
  clearSelection();
  selectedEditElement = el;
  selectedEditElement.classList.add('edit-selected');
  selectedEditElement.setAttribute('data-editable', '');
  if (selectedEditElement.matches(textCandidates())) selectedEditElement.contentEditable = 'true';
  if (editTargetLabel) editTargetLabel.textContent = labelForElement(el);
}
function rangeInActiveSlide(range) {
  const slide = slides[index];
  return Boolean(range && slide?.contains(range.commonAncestorContainer));
}
function currentBrowserTextRange() {
  const selection = window.getSelection?.();
  if (!selection || selection.rangeCount === 0 || selection.isCollapsed) return null;
  const range = selection.getRangeAt(0);
  return rangeInActiveSlide(range) ? range : null;
}
function rememberTextSelection() {
  const range = currentBrowserTextRange();
  if (!range) return false;
  savedTextRange = range.cloneRange();
  if (editTargetLabel) editTargetLabel.textContent = '已选择一段文字';
  return true;
}
function setupEditSelection() {
  slides.forEach((slide) => {
    slide.addEventListener('click', (event) => {
      if (!editing) return;
      if (editToolbar?.contains(event.target)) return;
      if (rememberTextSelection()) return;
      const textTarget = event.target.closest(textCandidates());
      const blockTarget = event.target.closest(blockCandidates());
      const target = textTarget || blockTarget;
      if (!target || !slide.contains(target)) return;
      event.preventDefault();
      event.stopPropagation();
      selectEditElement(target);
    });
    slide.addEventListener('pointerdown', startDrag);
  });
  window.addEventListener('pointermove', onDrag);
  window.addEventListener('pointerup', endDrag);
  document.addEventListener('selectionchange', () => {
    if (!editing) return;
    rememberTextSelection();
  });
}
function setEditing(active) {
  editing = active;
  document.body.classList.toggle('editing', editing);
  editToolbar?.setAttribute('aria-hidden', String(!editing));
  const stage = slides[index]?.querySelector('.slide-stage');
  if (!stage) return;
  stage.contentEditable = 'false';
  if (editing) { stage.focus(); toast('编辑模式：可选中文字。按住 Alt/Option 拖拽移动元素，方向键微调。Cmd/Ctrl+S 保存。'); }
  else { clearSelection(); toast('已退出编辑模式'); }
}
function currentBlock() { return selectedEditElement?.closest(blockCandidates()); }
function fontStep(delta) {
  const target = editTargetForTextAction();
  if (!target) return toast('请先选择元素或一段文字');
  const current = Number(target.dataset.fontScale || 1);
  const next = Math.max(0.5, Math.min(2.5, Math.round((current + delta * 0.06) * 100) / 100));
  target.dataset.fontScale = String(next);
  target.style.setProperty('--edit-font-scale', String(next));
}
function setAttr(name, value) { const target = editTargetForTextAction(); if (!target) return toast('请先选择元素或一段文字'); target.dataset[name] = value; }
function selectedTextRange() {
  const liveRange = currentBrowserTextRange();
  if (liveRange) {
    savedTextRange = liveRange.cloneRange();
    return liveRange;
  }
  return rangeInActiveSlide(savedTextRange) ? savedTextRange.cloneRange() : null;
}
function editableSpanFromSelection() {
  const range = selectedTextRange();
  if (!range) return null;
  let ancestor = range.commonAncestorContainer.nodeType === Node.TEXT_NODE ? range.commonAncestorContainer.parentElement : range.commonAncestorContainer;
  if (ancestor?.classList?.contains('edit-inline')) return ancestor;
  const span = document.createElement('span');
  span.className = 'edit-inline';
  span.setAttribute('data-editable', '');
  try {
    range.surroundContents(span);
  } catch (_) {
    const contents = range.extractContents();
    span.appendChild(contents);
    range.insertNode(span);
  }
  const selection = window.getSelection();
  selection.removeAllRanges();
  const nextRange = document.createRange();
  nextRange.selectNodeContents(span);
  selection.addRange(nextRange);
  savedTextRange = nextRange.cloneRange();
  selectEditElement(span);
  return span;
}
function editTargetForTextAction() {
  return editableSpanFromSelection() || selectedEditElement;
}
function toggleBold() { const target = editTargetForTextAction(); if (!target) return toast('请先选择元素或一段文字'); target.style.fontWeight = target.style.fontWeight === '950' ? '' : '950'; }
function insertBreak() { const target = editTargetForTextAction(); if (!target) return toast('请先选择文字元素'); target.focus?.(); document.execCommand?.('insertHTML', false, '<br>'); }
function clearBreaks() { const target = editTargetForTextAction(); if (!target) return toast('请先选择元素或一段文字'); target.innerHTML = target.innerHTML.replace(/<br\s*\/?>(\n)?/gi, ' '); }
function duplicateElement() {
  if (!selectedEditElement) return toast('请先选择元素');
  const clone = selectedEditElement.cloneNode(true);
  clone.classList.remove('edit-selected');
  clone.removeAttribute('contenteditable');
  selectedEditElement.after(clone);
  selectEditElement(clone);
  toast('已复制当前元素');
}
function deleteElement() {
  if (!selectedEditElement) return toast('请先选择元素');
  if (!confirm('删除当前元素？')) return;
  const el = selectedEditElement;
  clearSelection();
  el.remove();
}
function duplicateBlock() {
  const block = currentBlock();
  if (!block) return duplicateElement();
  const clone = block.cloneNode(true);
  clone.classList.remove('edit-selected');
  clone.querySelectorAll('.edit-selected,[contenteditable]').forEach((n) => { n.classList.remove('edit-selected'); n.removeAttribute('contenteditable'); });
  block.after(clone);
  selectEditElement(clone);
  toast('已复制当前容器');
}
function deleteBlock() {
  const block = currentBlock();
  if (!block) return deleteElement();
  if (!confirm('删除当前容器？')) return;
  clearSelection();
  block.remove();
}
function toggleHighlight() { const block = currentBlock() || selectedEditElement; if (!block) return toast('请先选择元素'); block.classList.toggle('colored-card'); block.classList.toggle('colored'); }
function setDensity(mode) { const slide = slides[index]; slide.classList.remove('density-compact', 'density-loose'); if (mode !== 'normal') slide.classList.add(`density-${mode}`); toast(`页面密度：${mode}`); }
function moveSelected(dx, dy) {
  if (!selectedEditElement) return;
  const x = Number(selectedEditElement.dataset.x || 0) + dx;
  const y = Number(selectedEditElement.dataset.y || 0) + dy;
  selectedEditElement.dataset.x = String(x);
  selectedEditElement.dataset.y = String(y);
  selectedEditElement.style.setProperty('--edit-x', `${x}px`);
  selectedEditElement.style.setProperty('--edit-y', `${y}px`);
}
function resetMove() {
  if (!selectedEditElement) return toast('请先选择元素');
  selectedEditElement.dataset.x = '0';
  selectedEditElement.dataset.y = '0';
  selectedEditElement.style.setProperty('--edit-x', '0px');
  selectedEditElement.style.setProperty('--edit-y', '0px');
}
function sizeTarget() { return currentBlock() || selectedEditElement; }
function widthStep(delta) {
  const target = sizeTarget();
  if (!target) return toast('请先选择元素或卡片');
  const rect = target.getBoundingClientRect();
  const current = Number(target.dataset.editWidth || Math.round(rect.width));
  const next = Math.max(80, current + delta * 24);
  target.dataset.editWidth = String(next);
  target.style.setProperty('--edit-width', `${next}px`);
}
function heightStep(delta) {
  const target = sizeTarget();
  if (!target) return toast('请先选择元素或卡片');
  const rect = target.getBoundingClientRect();
  const current = Number(target.dataset.editMinHeight || Math.round(rect.height));
  const next = Math.max(40, current + delta * 18);
  target.dataset.editMinHeight = String(next);
  target.style.setProperty('--edit-min-height', `${next}px`);
}
function resetSize() {
  const target = sizeTarget();
  if (!target) return toast('请先选择元素或卡片');
  delete target.dataset.editWidth;
  delete target.dataset.editMinHeight;
  target.style.removeProperty('--edit-width');
  target.style.removeProperty('--edit-min-height');
  target.style.removeProperty('width');
  target.style.removeProperty('min-height');
}
function toggleNowrap() {
  if (!selectedEditElement) return toast('请先选择元素');
  const target = selectedEditElement.matches(textCandidates()) ? selectedEditElement : selectedEditElement.querySelector('h1,h2,h3,p,.card-title,.grid-title') || selectedEditElement;
  target.dataset.nowrap = target.dataset.nowrap === 'true' ? 'false' : 'true';
}
function setPaddingMode(mode) {
  const target = sizeTarget();
  if (!target) return toast('请先选择卡片或容器');
  target.dataset.pad = mode;
}
function startDrag(event) {
  if (!editing || !selectedEditElement || event.button !== 0 || !event.altKey) return;
  if (editToolbar?.contains(event.target)) return;
  const target = event.target.closest(editableCandidates());
  if (!target || target !== selectedEditElement) return;
  if (selectedEditElement.matches(textCandidates()) && event.detail >= 2) return;
  dragState = { startX: event.clientX, startY: event.clientY, baseX: Number(selectedEditElement.dataset.x || 0), baseY: Number(selectedEditElement.dataset.y || 0) };
  selectedEditElement.classList.add('dragging');
}
function onDrag(event) {
  if (!dragState || !selectedEditElement) return;
  const x = dragState.baseX + event.clientX - dragState.startX;
  const y = dragState.baseY + event.clientY - dragState.startY;
  selectedEditElement.dataset.x = String(Math.round(x));
  selectedEditElement.dataset.y = String(Math.round(y));
  selectedEditElement.style.setProperty('--edit-x', `${Math.round(x)}px`);
  selectedEditElement.style.setProperty('--edit-y', `${Math.round(y)}px`);
}
function endDrag() { selectedEditElement?.classList.remove('dragging'); dragState = null; }
function applyEditAction(action) {
  const map = {
    'font-dec': () => fontStep(-1), 'font-inc': () => fontStep(1), bold: toggleBold,
    'line-tight': () => setAttr('line', 'tight'), 'line-normal': () => setAttr('line', 'normal'), 'line-loose': () => setAttr('line', 'loose'),
    'color-ink': () => setAttr('color', 'ink'), 'color-clay': () => setAttr('color', 'clay'), 'color-stone': () => setAttr('color', 'stone'),
    'align-left': () => setAttr('align', 'left'), 'align-center': () => setAttr('align', 'center'), 'align-right': () => setAttr('align', 'right'),
    'insert-br': insertBreak, 'clear-br': clearBreaks,
    'width-dec': () => widthStep(-1), 'width-inc': () => widthStep(1), 'size-reset': resetSize,
    'height-dec': () => heightStep(-1), 'height-inc': () => heightStep(1), 'nowrap-toggle': toggleNowrap,
    'pad-compact': () => setPaddingMode('compact'), 'pad-normal': () => setPaddingMode('normal'), 'pad-loose': () => setPaddingMode('loose'),
    'duplicate-element': duplicateElement, 'delete-element': deleteElement, 'reset-move': resetMove,
    'duplicate-block': duplicateBlock, 'toggle-highlight': toggleHighlight, 'delete-block': deleteBlock,
    'density-compact': () => setDensity('compact'), 'density-normal': () => setDensity('normal'), 'density-loose': () => setDensity('loose')
  };
  map[action]?.();
}
editToolbar?.addEventListener('mousedown', (event) => {
  if (event.target.closest('[data-edit]')) event.preventDefault();
});
editToolbar?.addEventListener('click', (event) => { const button = event.target.closest('[data-edit]'); if (!button) return; event.preventDefault(); applyEditAction(button.dataset.edit); });
async function tryServerSave(source, html) {
  if (location.protocol === 'file:') return false;
  try {
    const res = await fetch('/__save_slide', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ source, html }) });
    return res.ok;
  } catch (_) { return false; }
}
async function ensureDeckDirectoryHandle() { if (!('showDirectoryPicker' in window)) return null; if (deckDirectoryHandle) return deckDirectoryHandle; toast('请选择包含 sources/ 的 deck 文件夹，用于保存当前页源文件。'); deckDirectoryHandle = await window.showDirectoryPicker({ mode: 'readwrite' }); return deckDirectoryHandle; }
async function getFileHandleByPath(rootHandle, relativePath) { const parts = relativePath.split('/').filter(Boolean); let handle = rootHandle; for (const part of parts.slice(0, -1)) handle = await handle.getDirectoryHandle(part, { create: false }); return handle.getFileHandle(parts.at(-1), { create: false }); }
async function tryFileSystemAccessSave(source, html) {
  if (!('showDirectoryPicker' in window)) return false;
  try { const root = await ensureDeckDirectoryHandle(); if (!root) return false; const fileHandle = await getFileHandleByPath(root, source); const writable = await fileHandle.createWritable(); await writable.write(html); await writable.close(); return true; }
  catch (error) { console.warn('File System Access source save failed:', error); toast('没有找到 sources/slide 文件。若当前只有单个 HTML，请改用“保存完整 HTML”。'); return false; }
}
function cleanForSave(root) { root.querySelector('body')?.classList.remove('editing'); root.querySelectorAll('.edit-selected').forEach((node) => node.classList.remove('edit-selected')); root.querySelectorAll('[contenteditable]').forEach((node) => node.removeAttribute('contenteditable')); root.querySelector('.overview')?.classList.remove('active'); root.querySelector('.overview')?.setAttribute('aria-hidden', 'true'); root.querySelector('.editor-toast')?.classList.remove('active'); root.querySelector('.edit-toolbar')?.setAttribute('aria-hidden', 'true'); }
function currentFullHtml() { const clone = document.documentElement.cloneNode(true); cleanForSave(clone); clone.querySelectorAll('.slide').forEach((slide, i) => slide.classList.toggle('active', i === index)); return '<!doctype html>\n' + clone.outerHTML; }
function currentSlideHtml() { const clone = slides[index].cloneNode(true); clone.classList.remove('active'); clone.querySelectorAll('.edit-selected').forEach((node) => node.classList.remove('edit-selected')); clone.querySelectorAll('[contenteditable]').forEach((node) => node.removeAttribute('contenteditable')); return clone.outerHTML; }
async function saveFullHtmlFile() { if (!('showSaveFilePicker' in window)) return false; try { if (!htmlFileHandle) htmlFileHandle = await window.showSaveFilePicker({ suggestedName: (document.title || 'deck') + '-edited.html', types: [{ description: 'HTML deck', accept: { 'text/html': ['.html'] } }] }); const writable = await htmlFileHandle.createWritable(); await writable.write(currentFullHtml()); await writable.close(); return true; } catch (error) { console.warn('Full HTML save failed:', error); return false; } }
async function saveCurrentSlide() { const slide = slides[index]; const source = slide?.dataset.source; if (!source) return toast('当前页缺少 data-source，无法保存。'); const html = currentSlideHtml(); if (await tryServerSave(source, html)) return toast(`已通过本地服务保存 ${source}`); if (await tryFileSystemAccessSave(source, html)) return toast(`已保存到源文件 ${source}`); if (await saveFullHtmlFile()) return toast('未找到源文件，已保存为完整 HTML 文件。'); toast('保存失败：请选择包含 sources/ 的 deck 文件夹，或使用 Chrome/Edge 另存完整 HTML。'); }
document.querySelector('#prevBtn').addEventListener('click', () => showSlide(index - 1));
document.querySelector('#nextBtn').addEventListener('click', () => showSlide(index + 1));
window.addEventListener('keydown', (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 's') { event.preventDefault(); saveCurrentSlide(); return; }
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'b') { event.preventDefault(); toggleBold(); return; }
  if ((event.metaKey || event.ctrlKey) && event.shiftKey && event.key.toLowerCase() === 'c') { event.preventDefault(); setAttr('color', 'clay'); return; }
  if (editing && ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(event.key) && selectedEditElement) {
    event.preventDefault();
    const step = event.shiftKey ? 10 : 2;
    if (event.key === 'ArrowUp') moveSelected(0, -step);
    if (event.key === 'ArrowDown') moveSelected(0, step);
    if (event.key === 'ArrowLeft') moveSelected(-step, 0);
    if (event.key === 'ArrowRight') moveSelected(step, 0);
    return;
  }
  if (event.key === 'Escape') { if (editing) setEditing(false); if (overview.classList.contains('active')) toggleOverview(false); if (document.fullscreenElement) document.exitFullscreen?.(); return; }
  if (editing) return;
  if (['ArrowRight', 'PageDown', ' '].includes(event.key)) showSlide(index + 1);
  if (['ArrowLeft', 'PageUp'].includes(event.key)) showSlide(index - 1);
  if (event.key.toLowerCase() === 'f') document.documentElement.requestFullscreen?.();
  if (event.key.toLowerCase() === 'o') toggleOverview();
  if (event.key.toLowerCase() === 'e') setEditing(true);
});
setupEditSelection();
showSlide(0);
