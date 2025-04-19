

const client_console = document.getElementById('client_console_contain');
const opt_console = document.getElementById('opt_console_contain');
const gui_websocket_console = document.getElementById('gui_websocket_console_contain');
const watcher_contain = document.getElementById('watcher_contain');

const page_zh = document.getElementById("svg_zh");
const page_en = document.getElementById("svg_en");
const page_de = document.getElementById("svg_de");

socket.on('update_data', (data) => {
    function isHTML (content) {
        // 使用正则表达式判断内容是否是HTML
        const htmlRegex = /<\/?[a-z][\s\S]*>/i;
        return htmlRegex.test(content);
    }

    function updateConsole (consoleElement, content) {
        const wasAtBottom = Math.abs(consoleElement.scrollHeight - consoleElement.scrollTop - consoleElement.clientHeight) < 5;
        if (!content) {
            return;
        }
        if (typeof content === "object") {
            content = JSON.stringify(content, null, 2);
        }
        try {
            content = content.replace(/--<([^>]+)>/g, '--< $1 >');
        }
        catch (e) {
            console.log(e);
        }
        if (isHTML(content)) {
            consoleElement.innerHTML += content + '<br>';
        } else {
            // consoleElement.textContent += `\n${content}\n`;
            consoleElement.innerHTML += `<span>${content.replace('\\n', '<br>')}</span><br>`;
        }
        if (wasAtBottom) {
            consoleElement.scrollTop = consoleElement.scrollHeight;
        }
    }
    if (data.console) {
        updateConsole(client_console, data.console);
    }
    if (data.figure) {
        loadImage(data.figure);
    }
    if (data.watching_data) {
        //    写入函数，读取数据并创建表格
        loadWatchingData(data.watching_data);
    }
    if (data.alert_message) {
        msg_type = data.alert_message.type
        msg = data.alert_message.message
        if (msg_type == 'success') {
            var title = lang_dict.success
        } else if (msg_type == 'error') {
            title = lang_dict.error
        }
        else if (msg_type == 'warning') {
            title = lang_dict.warning
        }
        else if (msg_type == 'info') {
            title = lang_dict.info
        }
        else if (msg_type == 'question') {
            title = lang_dict.question
        }
        if (!isAllowMessageFromServerPopup) {
            message_in_waiting = {
                'title': title,
                'text': msg,
                'type': msg_type
            }
            return;
        }
        Swal.fire(title, msg, msg_type);
    }
    // if (data.txt) {
    //     updateConsole(opt_console, data.opt_console);
    // }
    // if (data.txt) {
    //     updateConsole(gui_websocket_console, data.gui_websocket_console);
    // }
});

const title_home = document.getElementById('title_home');
const title_console = document.getElementById('title_console');
const title_image = document.getElementById('title_image');
const title_manual_input = document.getElementById('title_manual_input');

const page_home = document.getElementById('page_home');
const page_console = document.getElementById('page_console');
const page_image = document.getElementById('page_image');
const page_manual_input = document.getElementById('page_manual_input');

function changePage (pageElement) {
    page_home.style.display = 'none';
    page_console.style.display = 'none';
    page_image.style.display = 'none';
    page_manual_input.style.display = 'none';
    pageElement.style.display = 'block';
}

function handleTitleClick (selectedElement) {
    title_home.classList.remove('title_selected');
    title_console.classList.remove('title_selected');
    title_image.classList.remove('title_selected');
    title_manual_input.classList.remove('title_selected');
    selectedElement.classList.add('title_selected');
    if (selectedElement == title_home) {
        changePage(page_home);
    } else if (selectedElement == title_console) {
        changePage(page_console);
    } else if (selectedElement == title_image) {
        changePage(page_image);
    } else if (selectedElement == title_manual_input) {
        changePage(page_manual_input);
    }

}

title_home.addEventListener('click', () => {
    handleTitleClick(title_home);
    // socket.emit('input_data', 'home1');
});

title_console.addEventListener('click', () => {
    handleTitleClick(title_console);
    // socket.emit('input_data', 'home');
});

title_image.addEventListener('click', () => {
    handleTitleClick(title_image);
});

title_manual_input.addEventListener('click', () => {
    handleTitleClick(title_manual_input);
});

page_zh.addEventListener("click", () => {
    localStorage.setItem("display_language", "zh");
    update_language();
});

page_en.addEventListener("click", () => {
    localStorage.setItem("display_language", "en");
    update_language();
});

page_de.addEventListener("click", () => {
    localStorage.setItem("display_language", "de");
    update_language();
});

const btn_reset_raspberry_pi_no_error = document.getElementById('reset_raspberry_pi_no_error');
btn_reset_raspberry_pi_no_error.addEventListener('click', () => {
    socket.emit('input_data', { "reset_raspberry_pi_no_error": { "evse_id": document.getElementById('reset_no_error_evse_id').value } });
})

// **************************显示图片**************************

const blank_pic = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAxXpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBBDsQgCLz7in2CMIj6HLvtJvuDff6i0qZtSuI4MGREwvb7fsKrB5MESbloVY0WUqVyM1LijDaQogw813p+qYdDYCvBbsy0qPfvdToM5tWMpZNRebuwXIUq7l9uRv4Q+kRsZHWj6kbgKZAbNJ9Ua8nnLyxbvEaZJ3RYNQ67lKd2zyXb9tZk74B5AyEaAjoHQD8poBmBIUGskaDGARlIPokt5GlPe4Q/zrxaRK4mdLsAAAGEaUNDUElDQyBwcm9maWxlAAB4nH2RPUjDQBzFX1NFkWoFK4g4ZKhOdlERx1LFIlgobYVWHUwu/YImDUmKi6PgWnDwY7Hq4OKsq4OrIAh+gLgLToouUuL/kkKLGA+O+/Hu3uPuHSA0Kkw1u6KAqllGKh4Ts7lVsecVfgwgiGEMSszUE+nFDDzH1z18fL2L8Czvc3+OfiVvMsAnEkeZbljEG8Szm5bOeZ84xEqSQnxOPGnQBYkfuS67/Ma56LDAM0NGJjVPHCIWix0sdzArGSrxDHFYUTXKF7IuK5y3OKuVGmvdk78wkNdW0lynOYY4lpBAEiJk1FBGBRYitGqkmEjRfszDP+r4k+SSyVUGI8cCqlAhOX7wP/jdrVmYnnKTAjGg+8W2P8aBnl2gWbft72Pbbp4A/mfgSmv7qw1g7pP0elsLHwHBbeDiuq3Je8DlDjDypEuG5Eh+mkKhALyf0TflgKFboG/N7a21j9MHIENdLd8AB4fARJGy1z3e3dvZ279nWv39AGzGcqSNRJteAAANdmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDphYzUwM2FkNi0zM2ZhLTQ4ZmItOTBmMS1jNjZlNjU2NjQxNmIiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6Yjg1N2E1MGUtNzMzZC00ZDljLTg1OWUtZDFlYTIxNTdiYmNjIgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZTRlYzY3MWItZDU4NC00Njg3LTlmNTMtZTQ2Yzk0NTg1NmUzIgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iV2luZG93cyIKICAgR0lNUDpUaW1lU3RhbXA9IjE3NDE5NjY0NzQ0OTkwMDIiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zNiIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjU6MDM6MTRUMTY6MzQ6MzErMDE6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDI1OjAzOjE0VDE2OjM0OjMxKzAxOjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6YTQ2NjcxZGQtMDlmOC00ZWQzLTkyYTEtNzE4NTIyNDRiNWYyIgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKFdpbmRvd3MpIgogICAgICBzdEV2dDp3aGVuPSIyMDI1LTAzLTE0VDE2OjM0OjM0Ii8+CiAgICA8L3JkZjpTZXE+CiAgIDwveG1wTU06SGlzdG9yeT4KICA8L3JkZjpEZXNjcmlwdGlvbj4KIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0idyI/PnT6oVkAAAAGYktHRAARAJYA20xcylMAAAAJcEhZcwAADsEAAA7BAbiRa+0AAAAHdElNRQfpAw4PIiIjbq3wAAAAF0lEQVQY02N8K6PCQAxgYiASjCqkjkIA8i4BQVzyl6cAAAAASUVORK5CYII="
const figChargePoint = document.getElementById("cp_fig");
const figOptimisation = document.getElementById("opt_fig");
function loadImage (data) {
    if (!data) {
        figChargePoint.src = blank_pic;
        return
    }

    if ('cp_fig' in data) {
        let base64Data = data.cp_fig.trim();
        if (base64Data.startsWith('data:image')) {
            base64Data = base64Data.split(',')[1];
        }
        figChargePoint.src = `data:image/png;base64,${base64Data}`;
        // figChargePoint.src = data.cp_fig.startsWith("data:image/png;base64,")
        //     ? data.cp_fig
        //     : `data:image/png;base64,${data.cp_fig}`;
    }
    figChargePoint.onerror = () => {
        figChargePoint.src = blank_pic;
    };
    if ('opt_fig' in data) {
        figOptimisation.src = data.opt_fig.startsWith("data:image/png;base64,")
            ? data.opt_fig
            : `data:image/png;base64,${data.opt_fig}`;
    }
    figOptimisation.onerror = () => {
        figChargePoint.src = blank_pic;
    };
}
handleTitleClick(title_home);


function loadWatchingData (data) {
    // 清空容器
    watcher_contain.innerHTML = '';

    if (!data) return;
    if (data.current_time) {
         const watchingDataTime = document.createElement('h1');
         watchingDataTime.innerHTML = data.current_time;
         // watchingDataTime.style.textAlign = 'center';
         watchingDataTime.style.marginBottom = '20px';
         watchingDataTime.style.fontSize = '20px';
         watcher_contain.appendChild(watchingDataTime);
     }

    // ========== EVSE 部分 ==========
    if (data.evse) {
        const evseTitle = document.createElement('h3');
        evseTitle.textContent = lang_dict.evse_data;
        watcher_contain.appendChild(evseTitle);

        const evseTable = document.createElement('table');
        evseTable.style.borderCollapse = 'collapse';
        evseTable.style.width = '100%';
        evseTable.style.marginBottom = '20px';

        const evseHeaders = [
            lang_dict.register_address, lang_dict.register_description, lang_dict.register_value, lang_dict.function_code, lang_dict.status, lang_dict.isError,
            lang_dict.exception_code, lang_dict.dev_id, lang_dict.transaction_id, lang_dict.bits, lang_dict.address
        ];

        const evseThead = document.createElement("thead");
        const evseHeaderRow = document.createElement("tr");
        evseHeaders.forEach(h => {
            const th = document.createElement("th");
            th.textContent = h;
            th.style.border = "1px solid #ccc";
            th.style.padding = "6px";
            th.style.backgroundColor = "#f0f0f0";
            evseHeaderRow.appendChild(th);
        });
        evseThead.appendChild(evseHeaderRow);
        evseTable.appendChild(evseThead);

        const evseTbody = document.createElement("tbody");
        for (const addr in data.evse) {
            const item = data.evse[addr];
            const row = document.createElement("tr");
            let reg_description
            if (addr in lang_dict.reg_description) {
                reg_description = lang_dict.reg_description[addr]
            } else {
                reg_description = `-`
            }
            const values = [
                addr,
                reg_description,
                JSON.stringify(item.registers),
                item.function_code,
                item.status,
                item.isError,
                item.exception_code,
                item.dev_id,
                item.transaction_id,
                JSON.stringify(item.bits),
                item.address,
            ];

            values.forEach(val => {
                const td = document.createElement("td");
                td.textContent = val !== undefined ? val : "-";
                //                td.textContent = (val === undefined || val === null || (Array.isArray(val) && val.length === 0)) ? '-' : val;
                td.style.border = "1px solid #ccc";
                td.style.padding = "6px";
                row.appendChild(td);
            });

            evseTbody.appendChild(row);
        }
        evseTable.appendChild(evseTbody);
        watcher_contain.appendChild(evseTable);
    }

    // ========== Shelly 部分 ==========
    if (data.shelly) {
        const shellyTitle = document.createElement('h3');
        shellyTitle.textContent = lang_dict.Shelly_data;
        watcher_contain.appendChild(shellyTitle);

        const shellyTable = document.createElement('table');
        shellyTable.style.borderCollapse = 'collapse';
        shellyTable.style.width = '100%';

        const shellyHeaders = [lang_dict.phase, lang_dict.power, lang_dict.pf, lang_dict.current, lang_dict.voltage, lang_dict.is_valid, lang_dict.total];

        const shellyThead = document.createElement("thead");
        const shellyHeaderRow = document.createElement("tr");
        shellyHeaders.forEach(h => {
            const th = document.createElement("th");
            th.textContent = h;
            th.style.border = "1px solid #ccc";
            th.style.padding = "6px";
            th.style.backgroundColor = "#f0f0f0";
            shellyHeaderRow.appendChild(th);
        });
        shellyThead.appendChild(shellyHeaderRow);
        shellyTable.appendChild(shellyThead);

        const shellyTbody = document.createElement("tbody");
        for (const key in data.shelly) {
            if (isNaN(parseInt(key))) continue;  // 跳过非编号项

            const item = data.shelly[key];
            const row = document.createElement("tr");

            const values = [
                key,
                item.power,
                item.pf,
                item.current,
                item.voltage,
                item.is_valid,
                item.total,
            ];

            values.forEach(val => {
                const td = document.createElement("td");
                td.textContent = val !== undefined ? val : "-";
                td.style.border = "1px solid #ccc";
                td.style.padding = "6px";
                row.appendChild(td);
            });

            shellyTbody.appendChild(row);
        }
        shellyTable.appendChild(shellyTbody);
        watcher_contain.appendChild(shellyTable);

        // 添加额外信息：charged_energy 和 overall is_valid
        const extraInfo = document.createElement('div');
        extraInfo.style.marginTop = "10px";
        extraInfo.innerHTML = `
    <p><strong>${lang_dict.charged_energy}:</strong> ${data.shelly.charged_energy}</p>
    <p><strong>${lang_dict.Shelly_is_valid}:</strong> ${data.shelly.is_valid}</p>`
        watcher_contain.appendChild(extraInfo);
    }
}