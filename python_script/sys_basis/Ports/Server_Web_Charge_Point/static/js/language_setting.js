function update_language () {
    const lang_setting = localStorage.getItem('display_language') || 'en';
    set_language_package(lang_setting);
}

function set_language_package (lang_str) {
    /* 设置语言包
    设置语言包后，会自动更新页面上的文本
    如果语言包不存在，会使用默认语言包*/
    if (lang_str == 'zh') { 
        apply_language_package(lang_pkg_zh);
        window.lang_dict = lang_pkg_zh;
    }
    else if (lang_str == 'en') {
        apply_language_package(lang_pkg_en);
        window.lang_dict = lang_pkg_en;
    }
    else if (lang_str == 'de') {
        apply_language_package(lang_pkg_de);
        window.lang_dict = lang_pkg_de;
    }
    else {
        apply_language_package(lang_pkg_en);
        window.lang_dict = lang_pkg_en;
    }
}
function apply_language_package (language_package) { 
    for (const [key, value] of Object.entries(language_package)) {
        const element = document.getElementById(key);
        if (element) {
            if (key == 'username' || key == 'password') {
                element.placeholder = value;
            }
            else if (element.tagName == 'SELECT') {
                element.value = value;
            }
            else if (element.tagName == 'INPUT') {
                element.value = value;
            }
            else {
                element.textContent = value;
            }
        }
    }
}

update_language();