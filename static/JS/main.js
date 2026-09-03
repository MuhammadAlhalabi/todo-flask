function toggleField() {
  const fieldAddTask = document.getElementById("filed-add-task");
  if (fieldAddTask.style.display === "none")
    fieldAddTask.style.display = "block";
  else fieldAddTask.style.display = "none";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function hideAddTask() {
  document.getElementById("filed-add-task").style.display = "none";
}

function editField(editBtn) {
  const container = editBtn.closest(".tasks");
  const input = container.querySelector(".task-title");
  const form = container.querySelector(".task");
  const icon = editBtn.querySelector("i");

  if (input.disabled) {
    input.disabled = false;
    input.focus();
    icon.classList.remove("fa-pen");
    icon.classList.add("fa-check");
  } else {
    form.submit();
  }
}

function toggleMenu(event) {
  if (event) {
    event.stopPropagation();
  }
  document.getElementById("myMenu").classList.toggle("show");
}
