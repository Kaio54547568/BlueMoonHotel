document.addEventListener('DOMContentLoaded', function() {
    
    // 1. LOGIC TOGGLE (Ẩn/Hiện Menu)
    const menuBtn = document.getElementById('userMenuBtn');
    const userMenu = document.getElementById('userMenu'); 
    const overlay = document.getElementById('userMenuOverlay');

    if (menuBtn && userMenu && overlay) {
        menuBtn.addEventListener('click', () => {
            userMenu.classList.toggle('show');
            overlay.classList.toggle('show');
        });

        overlay.addEventListener('click', () => {
            userMenu.classList.remove('show');
            overlay.classList.remove('show');
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === "Escape") {
                userMenu.classList.remove('show');
                overlay.classList.remove('show');
            }
        });
    }

    // 2. LOGIC ĐĂNG XUẤT AN TOÀN (POST Request)
    const logoutItem = document.querySelector('.user-menu-item[data-action="logout"]');

    if (!logoutItem) return;

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    logoutItem.addEventListener('click', function(e) {
        e.preventDefault(); 
        const logoutUrl = this.href;
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = logoutUrl;
        
        const csrftoken = getCookie('csrftoken');
        if (csrftoken) {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrftoken;
            form.appendChild(csrfInput);
        } else {
            console.error("Lỗi bảo mật: CSRF token không được tìm thấy.");
            return;
        }

        document.body.appendChild(form);
        form.submit();
    });
});