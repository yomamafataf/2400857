const form = document.querySelector("#account-form");
const passwordInput = document.querySelector("#password");
const errorBox = document.querySelector("#errors");
const submitButton = document.querySelector("#login-button");

function localPasswordErrors(password) {
  const errors = [];
  if (password.length < 10) errors.push("Use at least 10 characters because MFA is not enabled.");
  if (password.length > 128) errors.push("Use no more than 128 characters.");
  if (/[\u0000-\u001f\u007f-\u009f]/u.test(password)) {
    errors.push("Control characters are not allowed.");
  }
  return errors;
}

async function validatePasswordFrontend(password) {
  const localErrors = localPasswordErrors(password);
  if (localErrors.length) return localErrors;

  const response = await fetch("/api/password-check", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({password}),
  });
  if (!response.ok) return ["Password validation is temporarily unavailable."];
  return (await response.json()).errors;
}

function showErrors(errors) {
  errorBox.replaceChildren(...errors.map((message) => {
    const paragraph = document.createElement("p");
    paragraph.textContent = message;
    return paragraph;
  }));
  errorBox.hidden = errors.length === 0;
}

form.addEventListener("submit", async (event) => {
  if (form.dataset.validated === "true") return;
  event.preventDefault();
  submitButton.disabled = true;
  showErrors(await validatePasswordFrontend(passwordInput.value));
  submitButton.disabled = false;
  if (errorBox.hidden) {
    form.dataset.validated = "true";
    form.requestSubmit();
  }
});
