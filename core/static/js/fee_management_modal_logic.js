document.addEventListener('DOMContentLoaded', function() {
    const tablePanel = document.getElementById('income-container'); 
    const modal = document.getElementById('mainModal');
    const modalContent = modal.querySelector('.modal-content');

    // 2. Logic MỞ/ĐÓNG MODAL
    function openModal() {
        modal.classList.add('show');
        document.body.classList.add('modal-open'); 
    }
    function closeModal() {
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
        modalContent.innerHTML = ''; 
    }
    function attachModalListeners() {
        const form = modalContent.querySelector('form');
        if (form) {
            form.addEventListener('submit', handleFormSubmission, { once: true }); // Sử dụng { once: true } để đảm bảo chỉ chạy 1 lần
        }
        const closeButton = modalContent.querySelector('.modal-close-btn');
        if (closeButton) {
            closeButton.addEventListener('click', closeModal, { once: true });
        }
    }
    function handleFormSubmission(e) {
        e.preventDefault();
        const form = e.currentTarget;
        const url = form.action;
        const formData = new FormData(form);
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' } 
        })
        .then(response => {
            if (response.ok && response.status === 200) {
                closeModal();
                window.location.reload(); 
                return;
            }
            if (response.headers.get('content-type')?.includes('text/html')) {
                return response.text();
            }
            throw new Error(`Lỗi HTTP ${response.status}: Vui lòng kiểm tra lại kết nối.`);
        })
        .then(html => {
            if (html) {
                modalContent.innerHTML = html;
                attachModalListeners();
            }
        })
        .catch(error => {
            console.error('Lỗi Submit Form Modal:', error);
            modalContent.innerHTML = `<div class="form-container"><h3 style="color: red; text-align: center;">Lỗi Xử Lý</h3><p style="text-align: center;">${error.message}</p><div class="form-actions" style="margin-top: 30px; text-align: center;"><button type="button" class="btn btn-secondary-outline modal-close-btn" style="min-width: 180px;"><i class="fa-solid fa-xmark"></i> Đóng</button></div></div>`;
            openModal();
            attachModalListeners();
        });
    }
    // 3. Hàm xử lý tải nội dung và mở Modal
    function loadAndOpenModal(url) {
        closeModal(); 
        
        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Không thể tải nội dung. Vui lòng kiểm tra kết nối hoặc thử lại. (Status: ' + response.status + ')');
            }
            return response.text();
        })
        .then(html => {
            modalContent.innerHTML = html;
            openModal();
            attachModalListeners();
        })
        .catch(error => {
            console.error('Lỗi tải nội dung Modal:', error);
            modalContent.innerHTML = `<div class="form-container"><h3 style="color: red; text-align: center;">Lỗi Tải Nội Dung</h3><p style="text-align: center;">${error.message}</p><div class="form-actions" style="margin-top: 30px; text-align: center;"><button type="button" class="btn btn-secondary-outline modal-close-btn" style="min-width: 180px;"><i class="fa-solid fa-xmark"></i> Đóng</button></div></div>`;
            openModal();
            attachModalListeners(); 
        });
    }

    // 4. Lắng nghe sự kiện click cho các nút MỞ MODAL
    if (tablePanel) {
        tablePanel.addEventListener('click', function(e) {
            const triggerButton = e.target.closest('button.modal-trigger') || e.target.closest('#createNewFeeBtn');
            
            if (triggerButton) { 
                e.preventDefault(); 
                const triggerUrl = triggerButton.getAttribute('data-url');
                loadAndOpenModal(triggerUrl);
            }
        });
    }
    
    // 5. Đóng modal khi click ra ngoài lớp phủ
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // 6. Đóng modal bằng phím Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModal();
        }
    });
});