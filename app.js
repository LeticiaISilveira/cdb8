const themeSwitch = document.querySelector(".theme-switch");
const themeSwitchLabel = document.querySelector("#theme-switch-label");

themeSwitch.addEventListener("click", () => {
  const isGreen = document.documentElement.dataset.theme !== "green";
  document.documentElement.dataset.theme = isGreen ? "green" : "pink";
  themeSwitch.setAttribute("aria-checked", String(isGreen));
  const nextTheme = isGreen ? "rosa" : "verde";
  themeSwitch.setAttribute("aria-label", `Mudar para tema ${nextTheme}`);
  themeSwitchLabel.textContent = nextTheme[0].toUpperCase() + nextTheme.slice(1);
});

const goldButton = document.querySelector(".secondary");

goldButton.addEventListener("pointermove", (event) => {
  const bounds = goldButton.getBoundingClientRect();
  const x = ((event.clientX - bounds.left) / bounds.width) * 100;
  const y = ((event.clientY - bounds.top) / bounds.height) * 100;

  goldButton.style.setProperty("--light-x", `${x}%`);
  goldButton.style.setProperty("--light-y", `${y}%`);
});

goldButton.addEventListener("pointerleave", () => {
  goldButton.style.removeProperty("--light-x");
  goldButton.style.removeProperty("--light-y");
});
