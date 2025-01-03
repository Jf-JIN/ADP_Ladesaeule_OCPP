
const login_zh = document.getElementById("svg_zh");
const login_en = document.getElementById("svg_en");
const login_de = document.getElementById("svg_de");

login_zh.addEventListener("click", () => {
    localStorage.setItem("display_language", "zh");
    update_language();
});

login_en.addEventListener("click", () => {
    localStorage.setItem("display_language", "en");
    update_language();
});

login_de.addEventListener("click", () => {
    localStorage.setItem("display_language", "de");
    update_language();
});

document.getElementById("user_login").onclick = function () {
    window.location.href = "/user";
};

document.getElementById("admin_login").onclick = function () {
    document.getElementById("login_form").submit();
};