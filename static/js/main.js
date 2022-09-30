document.addEventListener("DOMContentLoaded", function () {
  hljs.highlightAll();
});

let alertWrapper = document.querySelector(".alert");
let alertClose = document.querySelector(".alert__close");

if (alertWrapper) {
  alertClose.addEventListener(
    "click",
    () => (alertWrapper.style.display = "none")
  );
}

function message() {
  warning.style.display = "block";
  setTimeout(function () {
    warning.style.display = "none";
  }, 7000);
}

function deactivate() {
  warning.style.display = "block";
  setTimeout(function () {
    warning.style.display = "none";
  }, 20000);
}
function delete_account() {
  delete_warning.style.display = "block";
  setTimeout(function () {
    delete_warning.style.display = "none";
  }, 20000);
}
