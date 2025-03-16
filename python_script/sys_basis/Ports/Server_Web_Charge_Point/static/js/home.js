

const client_console = document.getElementById('client_console_contain');
const opt_console = document.getElementById('opt_console_contain');
const gui_websocket_console = document.getElementById('gui_websocket_console_contain');

const page_zh = document.getElementById("svg_zh");
const page_en = document.getElementById("svg_en");
const page_de = document.getElementById("svg_de");

socket.on('update_data', (data) => {
    console.log(data);
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

const blank_pic = "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAxXpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBBDsQgCLz7in2CMIj6HLvtJvuDff6i0qZtSuI4MGREwvb7fsKrB5MESbloVY0WUqVyM1LijDaQogw813p+qYdDYCvBbsy0qPfvdToM5tWMpZNRebuwXIUq7l9uRv4Q+kRsZHWj6kbgKZAbNJ9Ua8nnLyxbvEaZJ3RYNQ67lKd2zyXb9tZk74B5AyEaAjoHQD8poBmBIUGskaDGARlIPokt5GlPe4Q/zrxaRK4mdLsAAAGEaUNDUElDQyBwcm9maWxlAAB4nH2RPUjDQBzFX1NFkWoFK4g4ZKhOdlERx1LFIlgobYVWHUwu/YImDUmKi6PgWnDwY7Hq4OKsq4OrIAh+gLgLToouUuL/kkKLGA+O+/Hu3uPuHSA0Kkw1u6KAqllGKh4Ts7lVsecVfgwgiGEMSszUE+nFDDzH1z18fL2L8Czvc3+OfiVvMsAnEkeZbljEG8Szm5bOeZ84xEqSQnxOPGnQBYkfuS67/Ma56LDAM0NGJjVPHCIWix0sdzArGSrxDHFYUTXKF7IuK5y3OKuVGmvdk78wkNdW0lynOYY4lpBAEiJk1FBGBRYitGqkmEjRfszDP+r4k+SSyVUGI8cCqlAhOX7wP/jdrVmYnnKTAjGg+8W2P8aBnl2gWbft72Pbbp4A/mfgSmv7qw1g7pP0elsLHwHBbeDiuq3Je8DlDjDypEuG5Eh+mkKhALyf0TflgKFboG/N7a21j9MHIENdLd8AB4fARJGy1z3e3dvZ279nWv39AGzGcqSNRJteAAANdmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDphYzUwM2FkNi0zM2ZhLTQ4ZmItOTBmMS1jNjZlNjU2NjQxNmIiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6Yjg1N2E1MGUtNzMzZC00ZDljLTg1OWUtZDFlYTIxNTdiYmNjIgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZTRlYzY3MWItZDU4NC00Njg3LTlmNTMtZTQ2Yzk0NTg1NmUzIgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iV2luZG93cyIKICAgR0lNUDpUaW1lU3RhbXA9IjE3NDE5NjY0NzQ0OTkwMDIiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zNiIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjU6MDM6MTRUMTY6MzQ6MzErMDE6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDI1OjAzOjE0VDE2OjM0OjMxKzAxOjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6YTQ2NjcxZGQtMDlmOC00ZWQzLTkyYTEtNzE4NTIyNDRiNWYyIgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKFdpbmRvd3MpIgogICAgICBzdEV2dDp3aGVuPSIyMDI1LTAzLTE0VDE2OjM0OjM0Ii8+CiAgICA8L3JkZjpTZXE+CiAgIDwveG1wTU06SGlzdG9yeT4KICA8L3JkZjpEZXNjcmlwdGlvbj4KIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0idyI/PnT6oVkAAAAGYktHRAARAJYA20xcylMAAAAJcEhZcwAADsEAAA7BAbiRa+0AAAAHdElNRQfpAw4PIiIjbq3wAAAAF0lEQVQY02N8K6PCQAxgYiASjCqkjkIA8i4BQVzyl6cAAAAASUVORK5CYII="

function loadImage (data) {
    const figChargePoint = document.getElementById("cp_fig");
    const figOptimisation = document.getElementById("opt_fig");

    if ('cp_fig' in data) { 
        figChargePoint.src = data.cp_fig.startsWith("data:image/png;base64,")
            ? data.cp_fig
            : `data:image/png;base64,${data.cp_fig}`;
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


