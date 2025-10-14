from datetime import datetime
from enum import Enum

class Role(Enum):
    ADMIN = "ADMIN"
    RESIDENT = "RESIDENT"
    ACCOUNTANT = "ACCOUNTANT"


# Ánh xạ quyền theo từng vai trò
ROLE_GRANTS = {
    Role.ADMIN: {"FEE.CREATE", "FEE.COLLECT", "REPORT.VIEW", "USER.MANAGE"},
    Role.ACCOUNTANT: {"FEE.CREATE", "FEE.COLLECT", "REPORT.VIEW"},
    Role.RESIDENT: {"FEE.PAY", "FEE.VIEW", "PROFILE.UPDATE"}
}


class User:
    def __init__(self, user_id, username, password, full_name, email, phone, active=True):
        self.id = user_id
        self.username = username
        self.password = password       # (ghi chú: thực tế nên lưu password hash)
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.active = active
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_login_at = None

        self.roles = set()        # ví dụ: {Role.ADMIN}
        self.permissions = set()  # quyền cụ thể

    def add_role(self, role: Role):
        """Thêm vai trò cho user"""
        self.roles.add(role)

    def add_permission(self, permission: str):
        """Thêm quyền riêng lẻ"""
        self.permissions.add(permission)

    def has_permission(self, permission: str) -> bool:
        """Kiểm tra quyền"""
        # Kiểm tra trong quyền riêng hoặc quyền kế thừa từ roles
        return (
            permission in self.permissions
            or any(permission in ROLE_GRANTS[r] for r in self.roles)
        )

    def login(self, tk: str, mk: str) -> bool:
        """Đăng nhập: kiểm tra username + password"""
        if not self.active:
            print("Tài khoản bị khóa.")
            return False
        if self.username == tk and self.password == mk:
            self.last_login_at = datetime.now()
            print(f"Đăng nhập thành công: {self.username}")
            return True
        else:
            print("Sai tài khoản hoặc mật khẩu.")
            return False


# -------------------- Ví dụ sử dụng --------------------

if __name__ == "__main__":
    admin = User(1, "admin", "12345", "Quản trị viên", "admin@example.com", "0900000000")
    admin.add_role(Role.ADMIN)

    # Đăng nhập thử
    admin.login("admin", "12345")

    # Kiểm tra quyền
    print("Có quyền tạo phí không?", admin.has_permission("FEE.CREATE"))   # True
    print("Có quyền xem hồ sơ không?", admin.has_permission("PROFILE.UPDATE"))  # False
