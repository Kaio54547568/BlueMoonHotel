// Tải partial sidebar rồi gắn bật/tắt trượt
export async function loadSidebar({
  mountId = "sidebar-root",
  src = "./sidebar.html",
  toggleBtnId = "sidebarToggle",
  overlayId = "sidebarOverlay",
} = {}) {
  const holder = document.getElementById(mountId);
  if (!holder) return;

  const res = await fetch(src);
  const html = await res.text();
  const tmp = document.createElement("div");
  tmp.innerHTML = html;
  const aside = tmp.querySelector("aside.sidebar") || tmp.firstElementChild;
  if (!aside) {
    holder.innerHTML = '<p style="color:red">Không tải được sidebar.</p>';
    return;
  }
  holder.replaceWith(aside);

  const btn = document.getElementById(toggleBtnId);
  const overlay = document.getElementById(overlayId);
  const mq = window.matchMedia("(max-width: 992px)");

  function setOpen(open) {
    const isMobile = mq.matches;

    // Sidebar luôn trượt ở cả desktop & mobile
    aside.classList.toggle("is-open", open);

    // Desktop: đẩy content sang phải (có CSS body.sidebar-open ...)
    document.body.classList.toggle("sidebar-open", open && !isMobile);

    // Mobile: bật overlay, desktop thì tắt overlay
    if (overlay) overlay.classList.toggle("show", open && isMobile);

    if (btn) btn.setAttribute("aria-expanded", String(open));
  }

  // Nếu đổi giữa mobile/desktop thì đóng lại cho sạch
  mq.addEventListener("change", () => setOpen(false));

  btn &&
    btn.addEventListener("click", () =>
      setOpen(!aside.classList.contains("is-open"))
    );
  overlay && overlay.addEventListener("click", () => setOpen(false));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setOpen(false);
  });
}
