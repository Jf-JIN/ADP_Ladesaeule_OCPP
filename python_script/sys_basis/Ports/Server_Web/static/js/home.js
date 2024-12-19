

const client_console = document.getElementById('client_console_contain');
const opt_console= document.getElementById('opt_console_contain');
const gui_websocket_console = document.getElementById('gui_websocket_console_contain');

socket.on('update_data', (data) => {
    console.log(data);
    console.log(data.main_console);

    function updateConsole (consoleElement, content) {
        console.log(consoleElement.scrollHeight - consoleElement.scrollTop);
        console.log(consoleElement.clientHeight);
        console.log(Math.abs(consoleElement.scrollHeight - consoleElement.scrollTop - consoleElement.clientHeight) < 1)
        const wasAtBottom = Math.abs(consoleElement.scrollHeight - consoleElement.scrollTop - consoleElement.clientHeight) < 1;
        consoleElement.textContent += `\n${content}\n`;
        if (wasAtBottom) {
            consoleElement.scrollTop = consoleElement.scrollHeight;
        }
    }
    if (data.client_console) {
        updateConsole(client_console, data.client_console);
    }
    if (data.opt_console) {
        updateConsole(opt_console, data.opt_console);
    }
    if (data.gui_websocket_console) {
        updateConsole(gui_websocket_console, data.gui_websocket_console);
    }
});

const title_home = document.getElementById('title_home');
const title_console = document.getElementById('title_console');
const title_image = document.getElementById('title_image');

const page_home = document.getElementById('page_home');
const page_console = document.getElementById('page_console');
const page_image = document.getElementById('page_image');

function changePage (pageElement) {
    page_home.style.display = 'none';
    page_console.style.display = 'none';
    page_image.style.display = 'none';
    pageElement.style.display = 'block';
}

function handleTitleClick (selectedElement) {
    title_home.classList.remove('title_selected');
    title_console.classList.remove('title_selected');
    title_image.classList.remove('title_selected');
    selectedElement.classList.add('title_selected');
    if (selectedElement == title_home) {
        changePage(page_home);
    } else if (selectedElement == title_console) {
        changePage(page_console);
    } else if (selectedElement == title_image) {
        changePage(page_image);
    }

}

title_home.addEventListener('click', () => {
    handleTitleClick(title_home);
    socket.emit('input_data', 'home');
});

title_console.addEventListener('click', () => {
    handleTitleClick(title_console);
});

title_image.addEventListener('click', () => {
    handleTitleClick(title_image);
});