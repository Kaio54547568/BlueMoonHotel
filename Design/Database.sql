--
-- CSDL: db_bluemoon_management
-- Mô tả: Quản lý và thu phí chung cư BlueMoon.
--

DROP DATABASE IF EXISTS `db_bluemoon_management`;
CREATE DATABASE `db_bluemoon_management` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `db_bluemoon_management`;

-- ----------------------------
-- Cấu trúc các bảng
-- ----------------------------

-- Bảng: HoKhau (Thông tin hộ gia đình)
CREATE TABLE `HoKhau` (
    `idHoKhau` INT AUTO_INCREMENT PRIMARY KEY,
    `soCanHo` VARCHAR(10) NOT NULL UNIQUE COMMENT 'Số căn hộ (duy nhất)',
    `tenChuHo` VARCHAR(100) NOT NULL COMMENT 'Tên chủ hộ',
    `soDienThoai` VARCHAR(15),
    `ngayChuyenVao` DATE,
    `trangThai` ENUM('Đang ở', 'Đã chuyển đi') NOT NULL DEFAULT 'Đang ở'
) ENGINE=InnoDB;

-- Bảng: NhanKhau (Thành viên trong hộ khẩu)
CREATE TABLE `NhanKhau` (
    `idNhanKhau` INT AUTO_INCREMENT PRIMARY KEY,
    `idHoKhau` INT NOT NULL COMMENT 'FK: HoKhau.idHoKhau',
    `hoTen` VARCHAR(100) NOT NULL,
    `ngaySinh` DATE,
    `gioiTinh` ENUM('Nam', 'Nữ', 'Khác') DEFAULT 'Nam',
    `quanHeVoiChuHo` VARCHAR(50),
    `ghiChu` TEXT COMMENT 'Ghi chú tạm trú, tạm vắng',
    FOREIGN KEY (`idHoKhau`) REFERENCES `HoKhau`(`idHoKhau`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Bảng: TaiKhoan (Tài khoản người dùng hệ thống)
CREATE TABLE `TaiKhoan` (
    `idTaiKhoan` INT AUTO_INCREMENT PRIMARY KEY,
    `tenDangNhap` VARCHAR(50) NOT NULL UNIQUE,
    `matKhau` VARCHAR(255) NOT NULL COMMENT 'Mật khẩu (đã hash)',
    `hoTenNguoiDung` VARCHAR(100) NOT NULL,
    `vaiTro` ENUM('Admin', 'Kế toán') NOT NULL DEFAULT 'Kế toán' COMMENT 'Phân quyền người dùng'
) ENGINE=InnoDB;

-- Bảng: KhoanThu (Các loại phí và đóng góp)
CREATE TABLE `KhoanThu` (
    `idKhoanThu` INT AUTO_INCREMENT PRIMARY KEY,
    `tenKhoanThu` VARCHAR(255) NOT NULL,
    `loaiPhi` ENUM('Bắt buộc', 'Tự nguyện') NOT NULL DEFAULT 'Bắt buộc',
    `soTien` DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    `donViTinh` VARCHAR(50) COMMENT 'VD: VND/hộ, VND/m2'
) ENGINE=InnoDB;

-- Bảng: ThuPhiHoKhau (Lịch sử giao dịch thu phí)
CREATE TABLE `ThuPhiHoKhau` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `idHoKhau` INT NOT NULL COMMENT 'FK: HoKhau.idHoKhau',
    `idKhoanThu` INT NOT NULL COMMENT 'FK: KhoanThu.idKhoanThu',
    `ngayThu` DATE NOT NULL,
    `soTienDaThu` DECIMAL(12, 2) NOT NULL,
    `ghiChu` TEXT,
    FOREIGN KEY (`idHoKhau`) REFERENCES `HoKhau`(`idHoKhau`) ON DELETE CASCADE,
    FOREIGN KEY (`idKhoanThu`) REFERENCES `KhoanThu`(`idKhoanThu`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------
-- View và Trigger
-- ----------------------------

-- View: V_ThongTinThuPhi - Tổng hợp chi tiết các khoản đã thu phí.
CREATE VIEW `V_ThongTinThuPhi` AS
SELECT
    hk.soCanHo,
    hk.tenChuHo,
    kt.tenKhoanThu,
    kt.loaiPhi,
    tphk.soTienDaThu,
    tphk.ngayThu
FROM
    `ThuPhiHoKhau` AS tphk
JOIN
    `HoKhau` AS hk ON tphk.idHoKhau = hk.idHoKhau
JOIN
    `KhoanThu` AS kt ON tphk.idKhoanThu = kt.idKhoanThu
ORDER BY
    hk.soCanHo, tphk.ngayThu DESC;

-- Trigger: TG_KiemTraNgayThu - Không cho phép ngày thu ở tương lai.
DELIMITER $$
CREATE TRIGGER `TG_KiemTraNgayThu`
BEFORE INSERT ON `ThuPhiHoKhau`
FOR EACH ROW
BEGIN
    IF NEW.ngayThu > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ngày thu không hợp lệ.';
    END IF;
END$$
DELIMITER ;

-- ----------------------------
-- Dữ liệu mẫu
-- ----------------------------

-- INSERT INTO `HoKhau` (`soCanHo`, `tenChuHo`, `soDienThoai`, `ngayChuyenVao`, `trangThai`) VALUES
-- ('A1001', 'Nguyễn Văn An', '0901112222', '2023-01-15', 'Đang ở'),
-- ('B2005', 'Trần Thị Bình', '0912223333', '2023-03-20', 'Đang ở'),
-- ('C3010', 'Lê Văn Cường', '0983334444', '2023-02-01', 'Đã chuyển đi');

-- INSERT INTO `NhanKhau` (`idHoKhau`, `hoTen`, `ngaySinh`, `gioiTinh`, `quanHeVoiChuHo`) VALUES
-- (1, 'Nguyễn Văn An', '1980-05-20', 'Nam', 'Chủ hộ'),
-- (1, 'Nguyễn Thị Lan', '1982-10-10', 'Nữ', 'Vợ'),
-- (2, 'Trần Thị Bình', '1990-07-25', 'Nữ', 'Chủ hộ');

-- INSERT INTO `TaiKhoan` (`tenDangNhap`, `matKhau`, `hoTenNguoiDung`, `vaiTro`) VALUES
-- ('admin', 'pass123', 'Quản trị viên', 'Admin'),
-- ('ketoan01', 'pass456', 'Nguyễn Thị Mai', 'Kế toán');

-- INSERT INTO `KhoanThu` (`tenKhoanThu`, `loaiPhi`, `soTien`, `donViTinh`) VALUES
-- ('Phí dịch vụ chung cư T10/2025', 'Bắt buộc', 500000.00, 'VND/hộ'),
-- ('Phí quản lý T10/2025', 'Bắt buộc', 250000.00, 'VND/hộ'),
-- ('Quỹ khuyến học 2025', 'Tự nguyện', 100000.00, 'VND/hộ');

-- INSERT INTO `ThuPhiHoKhau` (`idHoKhau`, `idKhoanThu`, `ngayThu`, `soTienDaThu`, `ghiChu`) VALUES
-- (1, 1, '2025-10-05', 500000.00, 'Tiền mặt'),
-- (1, 3, '2025-10-05', 100000.00, 'Đóng góp'),
-- (2, 1, '2025-10-08', 500000.00, 'Chuyển khoản');