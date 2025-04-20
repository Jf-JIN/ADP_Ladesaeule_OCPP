
const div_description_light = document.getElementById('description_of_light');

function update_light_description () {
    div_description_light.innerHTML = `<table class="light-table">
    <thead style="background-color: #f0f0f0;">
        <tr>
        <th>${lang_dict.light_description.title_status}</th>
        <th>${lang_dict.light_description.title_description}</th>
        <th>${lang_dict.light_description.title_meaning}</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <td>🟢 ${lang_dict.light_description.status_ready}</td>
        <td>🟢🟢🟢🟢 (${lang_dict.light_description.description_ready}) </td>
        <td>${lang_dict.light_description.meaning_ready}</td>
        </tr>
        <tr>
        <td>🟢 ${lang_dict.light_description.status_prepare}</td>
        <td>🟢◯🟢◯ (${lang_dict.light_description.description_prepare}) </td>
        <td>${lang_dict.light_description.meaning_prepare}</td>
        </tr>
        <tr>
        <td>🟢 ${lang_dict.light_description.status_charging}</td>
        <td>🟢🟢◯◯ (${lang_dict.light_description.description_charging}) </td>
        <td>${lang_dict.light_description.meaning_charging}</td>
        </tr>
        <tr>
        <td>🟢 ${lang_dict.light_description.status_evse_shelly_error}</td>
        <td>🟢◯🟢◯◯◯———— (${lang_dict.light_description.description_evse_shelly_error}) </td>
        <td>${lang_dict.light_description.meaning_evse_shelly_error}</td>
        </tr>
    </tbody>
    </table>`
}

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
    update_light_description();
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