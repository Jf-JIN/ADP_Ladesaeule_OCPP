

const client_console = document.getElementById('client_console_contain');
const opt_console = document.getElementById('opt_console_contain');
const gui_websocket_console = document.getElementById('gui_websocket_console_contain');

const page_zh = document.getElementById("svg_zh");
const page_en = document.getElementById("svg_en");
const page_de = document.getElementById("svg_de");

socket.on('update_data', (data) => {
    console.log(data);
    console.log(data.main_console);
    function isHTML (content) {
        // 使用正则表达式判断内容是否是HTML
        const htmlRegex = /<\/?[a-z][\s\S]*>/i;
        return htmlRegex.test(content);
    }

    function updateConsole (consoleElement, content) {
        console.log(consoleElement.scrollHeight - consoleElement.scrollTop);
        console.log(consoleElement.clientHeight);
        console.log(Math.abs(consoleElement.scrollHeight - consoleElement.scrollTop - consoleElement.clientHeight) < 1)
        console.log(content);
        const wasAtBottom = Math.abs(consoleElement.scrollHeight - consoleElement.scrollTop - consoleElement.clientHeight) < 1;
        if (content) {
            try { 
                content = content.replace(/--<([^>]+)>/g, '--< $1 >');
            }
            catch (e) {
                console.log(e);
            }
        }
        
        console.log(content);

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
    // socket.emit('input_data', 'home1');
});

title_console.addEventListener('click', () => {
    handleTitleClick(title_console);
    // socket.emit('input_data', 'home');
});

title_image.addEventListener('click', () => {
    handleTitleClick(title_image);
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


function renderImages (data) {
    const parent = document.getElementById("page_image");

    parent.innerHTML = "";

    data.forEach(item => {
        const container = document.createElement("div");
        container.id = item.id; 
        container.className = "image-box";
        parent.appendChild(container);
        displayBase64Image(container, item.base64);
    });
}

function displayBase64Image (container, base64Data) {
    container.innerHTML = ""; // 清空

    const img = document.createElement("img");
    img.src = base64Data.startsWith("data:image/png;base64,")
        ? base64Data
        : `data:image/png;base64,${base64Data}`;

    img.style.width = "100%";
    img.style.height = "100%";
    img.style.objectFit = "cover";
    img.alt = "Image";

    img.onerror = () => {
        container.innerHTML = "<p>图片加载失败</p>";
    };
    container.appendChild(img);
}

// 获取父容器
const pageImageContainer = document.getElementById("page_image");

// 核心渲染函数
function renderImageGroups (groups) {
    // 清空旧内容
    pageImageContainer.innerHTML = "";

    // 遍历每组数据
    groups.forEach(group => {
        // 1. 创建组容器
        const groupDiv = document.createElement("div");
        groupDiv.className = "image-group";

        // 2. 创建左侧客户图片容器
        const clientBox = document.createElement("div");
        clientBox.className = "client-image-box";
        displayBase64Image(clientBox, group.clientImage); // 调用你的现有函数

        // 3. 创建右侧优化器图片容器
        const optimizerBox = document.createElement("div");
        optimizerBox.className = "optimizer-image-box";
        displayBase64Image(optimizerBox, group.optimizerImage);

        // 4. 组装并插入
        groupDiv.appendChild(clientBox);
        groupDiv.appendChild(optimizerBox);
        pageImageContainer.appendChild(groupDiv);
    });
}

// 调用示例
renderImageGroups(imageGroups);

const imagesData = [
    { id: "image_1", base64: "iVBORw0KGgoAAAANSUhEUgAAADkAAAA9CAYAAAAXicGTAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABiSURBVGhD7c8hAQAgEMBA2hCT6I8nwjFxZm5rzh7deoOoSUWTiiYVTSqaVDSpaFLRpKJJRZOKJhVNKppUNKloUtGkoklFk4omFU0qmlQ0qWhS0aSiSUWTiiYVTSqaVHwxeQFYuN+CDEEX7AAAAABJRU5ErkJggg==" },
    { id: "image_2", base64: "iVBORw0KGgoAAAANSUhEUgAAADkAAAA9CAYAAAAXicGTAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABjSURBVGhD7c8hAQAgAMAwspCHsiQET4RxMXP3Mfc6uvEGUZOKJhVNKppUNKloUtGkoklFk4omFU0qmlQ0qWhS0aSiSUWTiiYVTSqaVDSpaFLRpKJJRZOKJhVNKppUNKn4YvICg/TDG4elRY8AAAAASUVORK5CYII=" },
    { id: "image_3", base64: "iVBORw0KGgoAAAANSUhEUgAAADkAAAA9CAYAAAAXicGTAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABiSURBVGhD7c8hAQAgEMBA2hCT6I8nwjFxZm5rzh7deoOoSUWTiiYVTSqaVDSpaFLRpKJJRZOKJhVNKppUNKloUtGkoklFk4omFU0qmlQ0qWhS0aSiSUWTiiYVTSqaVHwxeQFYuN+CDEEX7AAAAABJRU5ErkJggg==" },
    { id: "image_4", base64: "iVBORw0KGgoAAAANSUhEUgAAADkAAAA9CAYAAAAXicGTAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABjSURBVGhD7c8hAQAgAMAwspCHsiQET4RxMXP3Mfc6uvEGUZOKJhVNKppUNKloUtGkoklFk4omFU0qmlQ0qWhS0aSiSUWTiiYVTSqaVDSpaFLRpKJJRZOKJhVNKppUNKn4YvICg/TDG4elRY8AAAAASUVORK5CYII=" }
];

renderImages(imagesData)