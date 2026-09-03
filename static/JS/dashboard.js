function toggleAll() {
  const section = document.getElementById("personal-data-section");
  if (section.style.display === "none") {
    section.style.display = "block";
  } else {
    section.style.display = "none";
  }
}

function toggleUsername() {
  var userEdit = document.getElementById("username-edit");
  if (userEdit.style.display === "none") userEdit.style.display = "block";
  else userEdit.style.display = "none";
}

function hideeUsername() {
  document.getElementById("username-edit").style.display = "none";
}

function togglePassword() {
  var passEdit = document.getElementById("password-edit");
  if (passEdit.style.display === "none") passEdit.style.display = "block";
  else passEdit.style.display = "none";
}

function hidePassword() {
  document.getElementById("password-edit").style.display = "none";
}

function toggleDelete() {
  var deleteAccount = document.getElementById("filed-delete");
  if (deleteAccount.style.display === "none")
    deleteAccount.style.display = "block";
  else deleteAccount.style.display = "none";
}

function hideDelete() {
  document.getElementById("filed-delete").style.display = "none";
}

function showStat() {
  const showStatistics = document.getElementById("statistics");
  if (showStatistics.style.display === "none")
    showStatistics.style.display = "block";
  else showStatistics.style.display = "none";
}
