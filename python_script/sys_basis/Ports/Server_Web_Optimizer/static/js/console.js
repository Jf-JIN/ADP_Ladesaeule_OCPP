const opt_console = document.getElementById('opt_console_contain');

socket.on('update_data', (data) => {
    console.log(data);

    function updateConsole(consoleElement, content) {
        // console.log(consoleElement.scrollHeight - consoleElement.scrollTop);
        // console.log(consoleElement.clientHeight);
        // console.log(Math.abs(consoleElement.scrollHeight - consoleElement.scrollTop - consoleElement.clientHeight) < 1)
        const wasAtBottom = Math.abs(consoleElement.scrollHeight - consoleElement.scrollTop - consoleElement.clientHeight) < 1;
        consoleElement.textContent += `\n${content}\n`;
        if (wasAtBottom) {
            consoleElement.scrollTop = consoleElement.scrollHeight;
        }
    }

    if (data.web_console) {
        updateConsole(opt_console, 'Web Info: ' + data.web_console);
    }

    if (data.opt_console) {
        updateConsole(opt_console, 'Console Info: ' + data.opt_console);
    }
});