document.addEventListener("DOMContentLoaded", function () {
  const roleInput = document.getElementById("user-role-id");
  const roleId = parseInt(roleInput?.value || "0", 10); // ✅ convert to number

  const menuNotLoggedIn = document.getElementById("menu-not-logged-in");
  const menuAdmin = document.getElementById("menu-accountmanage");
  const menuAccount = document.getElementById("menu-account");

  function resetSidebar() {
    if (menuNotLoggedIn) menuNotLoggedIn.style.display = "none";
    if (menuAdmin) menuAdmin.style.display = "none";
    if (menuAccount) menuAccount.style.display = "none";
  }

  resetSidebar();

  if (roleId === 1) {
    if (menuAdmin) menuAdmin.style.display = "block";
  } else if (roleId === 3 || roleId === 2) {
    // ✅ OR
    if (menuAccount) menuAccount.style.display = "block";
  } else {
    if (menuNotLoggedIn) menuNotLoggedIn.style.display = "block";
  }
});
