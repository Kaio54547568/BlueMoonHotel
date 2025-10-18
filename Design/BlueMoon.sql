-- Bảng 1: VaiTro
-- Lưu trữ các vai trò (quyền hạn) trong hệ thống để phân quyền.
CREATE TABLE VaiTro (
    id_vaitro SERIAL PRIMARY KEY, -- Mã số định danh duy nhất cho mỗi vai trò.
    ten_vaitro VARCHAR(50) NOT NULL        -- Tên của vai trò (ví dụ: 'Kế toán', 'Tổ trưởng/Tổ phó').
);


-- Bảng 2: TaiKhoan
-- Lưu trữ thông tin tài khoản để người dùng đăng nhập vào hệ thống.
CREATE TABLE TaiKhoan (
    id_taikhoan SERIAL PRIMARY KEY, -- Khóa chính: Mã duy nhất cho mỗi tài khoản.
    username VARCHAR(50) NOT NULL UNIQUE,     -- Tên đăng nhập.
    password VARCHAR(255) NOT NULL,           -- Mật khẩu (đã mã hóa).
    id_vaitro INT,                            -- Khóa ngoại: Xác định tài khoản này thuộc vai trò nào.

    FOREIGN KEY (id_vaitro) REFERENCES VaiTro(id_vaitro)
);


-- Bảng 4: NhanKhau (Tạo trước HoKhau để thiết lập khóa ngoại cho chủ hộ)
-- Lưu trữ thông tin chi tiết của từng cư dân (nhân khẩu).
CREATE TABLE NhanKhau (
    id_nhankhau SERIAL PRIMARY KEY, -- Mã số định danh duy nhất cho mỗi nhân khẩu.
    ho_ten VARCHAR(100) NOT NULL,             -- Họ và tên đầy đủ của nhân khẩu.
    ngay_sinh DATE,                           -- Ngày tháng năm sinh.
    cccd VARCHAR(12) UNIQUE,                  -- Số Căn cước công dân.
    quan_he_chu_ho VARCHAR(50),               -- Mối quan hệ với chủ hộ (ví dụ: 'Vợ', 'Con').
    id_hokhau INT                             -- Khóa ngoại, cho biết nhân khẩu thuộc hộ nào (sẽ thêm sau khi tạo bảng HoKhau).
);


-- Bảng 3: HoKhau
-- Quản lý thông tin của từng hộ gia đình trong chung cư.
CREATE TABLE HoKhau (
    id_hokhau SERIAL PRIMARY KEY,  -- Mã số định danh duy nhất cho mỗi hộ khẩu.
    so_can_ho VARCHAR(20) NOT NULL UNIQUE,    -- Số căn hộ của hộ gia đình.
    dien_tich FLOAT,                          -- Diện tích của căn hộ (để tính phí).
    id_chuho INT UNIQUE,                      -- Khóa ngoại, xác định ai là chủ hộ.
    
    FOREIGN KEY (id_chuho) REFERENCES NhanKhau(id_nhankhau)
);

-- Cập nhật khóa ngoại cho bảng NhanKhau sau khi HoKhau đã được tạo
-- (Phần này giữ nguyên vì nó giải quyết tham chiếu vòng)
ALTER TABLE NhanKhau
ADD CONSTRAINT fk_nhankhau_hokhau
FOREIGN KEY (id_hokhau) REFERENCES HoKhau(id_hokhau);


-- Bảng 5: BienDongNhanKhau
-- Ghi nhận thông tin tạm trú, tạm vắng của cư dân.
CREATE TABLE BienDongNhanKhau (
    id_biendong SERIAL PRIMARY KEY, -- Mã số định danh duy nhất cho mỗi lần biến động.
    loai_biendong VARCHAR(20) NOT NULL,       -- Loại biến động: 'Tạm trú' hoặc 'Tạm vắng'.
    ngay_batdau DATE NOT NULL,                -- Ngày bắt đầu của việc tạm trú/tạm vắng.
    ngay_ketthuc DATE,                        -- Ngày kết thúc (dự kiến).
    ly_do TEXT,                               -- Lý do của việc tạm trú/tạm vắng.
    id_nhankhau INT,                          -- Khóa ngoại, xác định nhân khẩu có biến động.
    
    FOREIGN KEY (id_nhankhau) REFERENCES NhanKhau(id_nhankhau)
);


-- Bảng 6: KhoanThu
-- Định nghĩa các loại phí dịch vụ mà chung cư cần thu.
CREATE TABLE KhoanThu (
    id_khoanthu SERIAL PRIMARY KEY, -- Mã số định danh duy nhất cho mỗi loại phí.
    ten_khoanthu VARCHAR(100) NOT NULL,       -- Tên của khoản thu (ví dụ: 'Phí quản lý').
    don_gia DECIMAL(10, 2) NOT NULL,          -- Mức giá cho một đơn vị tính.
    don_vi_tinh VARCHAR(20) NOT NULL          -- Đơn vị tính phí (ví dụ: 'm2', 'hộ', 'người').
);


-- Bảng 7: DotThuPhi
-- Quản lý các đợt thu phí được tạo ra theo kỳ (tháng/quý).
CREATE TABLE DotThuPhi (
    id_dotthu SERIAL PRIMARY KEY,   -- Mã số định danh duy nhất cho mỗi đợt thu.
    ten_dotthu VARCHAR(100) NOT NULL,         -- Tên của đợt thu (ví dụ: 'Thu phí tháng 10/2025').
    ngay_batdau DATE NOT NULL,                -- Ngày bắt đầu áp dụng thu phí.
    ngay_ketthuc DATE,                        -- Ngày kết thúc (hạn chót) của đợt thu.
    trang_thai VARCHAR(50)                    -- Trạng thái: 'Đang diễn ra', 'Đã kết thúc'.
);


-- Bảng 8: HoaDon
-- Ghi nhận việc thanh toán của một hộ gia đình cho một đợt thu phí cụ thể.
CREATE TABLE HoaDon (
    id_hoadon SERIAL PRIMARY KEY,     -- Mã số định danh duy nhất cho mỗi hóa đơn.
    tong_tien DECIMAL(15, 2) NOT NULL,      -- Tổng số tiền cần nộp hoặc đã nộp.
    ngay_nop DATE,                          -- Ngày hộ gia đình thực hiện thanh toán (NULL nếu chưa nộp).
    trang_thai VARCHAR(50) NOT NULL,        -- Trạng thái thanh toán: 'Đã nộp', 'Chưa nộp'.
    id_hokhau INT,                          -- Khóa ngoại, xác định hóa đơn này của hộ nào.
    id_dotthu INT,                          -- Khóa ngoại, cho biết hóa đơn thuộc đợt thu nào.
    
    FOREIGN KEY (id_hokhau) REFERENCES HoKhau(id_hokhau),
    FOREIGN KEY (id_dotthu) REFERENCES DotThuPhi(id_dotthu)
);