document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const body = document.body;
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', function() {
            body.classList.toggle('sidebar-toggled');
        });
    }
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && body.classList.contains('sidebar-toggled')) {
            body.classList.remove('sidebar-toggled');
        }
    });
    // Logic này nên được đặt trong script của trang chính (ví dụ: FeeManagement.html) 
    // Nhưng nếu muốn đặt trong đây, cần đảm bảo HTML đã tải xong.
});

