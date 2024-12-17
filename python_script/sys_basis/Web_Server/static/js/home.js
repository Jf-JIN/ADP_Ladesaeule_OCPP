

const main_console = document.getElementById('main_console_contain');
const opt_console= document.getElementById('opt_console_contain');
const client_console = document.getElementById('client_console_contain');

socket.on('update_data', (data) => {
    const json_data = JSON.stringify(data, null, 2);

    function updateConsole (console, logKey) {
        const wasAtBottom = console.scrollHeight - console.scrollTop === console.clientHeight;
        console.textContent += `\n${json_data[logKey]}\n`;
        if (wasAtBottom) {
            console.scrollTop = console.scrollHeight;
        }
    }

    updateConsole(main_console, 'main_console');
    updateConsole(opt_console, 'opt_console');
    updateConsole(client_console, 'client_console');
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
});

title_console.addEventListener('click', () => {
    handleTitleClick(title_console);
});

title_image.addEventListener('click', () => {
    handleTitleClick(title_image);
});