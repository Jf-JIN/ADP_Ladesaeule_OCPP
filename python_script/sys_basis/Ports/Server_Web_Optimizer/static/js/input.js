
// update condole
const opt_console = document.getElementById('console_contain');

socket.on('update_data', (data) => {
    console.log(data);

    function isHTML (content) {
        // 使用正则表达式判断内容是否是HTML
        const htmlRegex = /<\/?[a-z][\s\S]*>/i;
        return htmlRegex.test(content);
    }

    function updateConsole (consoleElement, content) {
        console.log(consoleElement.scrollHeight - consoleElement.scrollTop);
        console.log(consoleElement.clientHeight);
        console.log(Math.abs(consoleElement.scrollHeight - consoleElement.scrollTop - consoleElement.clientHeight) < 1)
        const wasAtBottom = Math.abs(consoleElement.scrollHeight - consoleElement.scrollTop - consoleElement.clientHeight) < 1;
        content = content.replace(/--<([^>]+)>:/g, '--< $1 >: ');
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

    if (data.web_console) {
        updateConsole(opt_console, 'Web Info: \n' + data.web_console);
    }

    if (data.opt_console) {
        updateConsole(opt_console, 'OCPP Info: \n' + data.opt_console);
    }
});

// update charging needs
const evseId = document.getElementById('evseId');
const departureTime = document.getElementById('departureTime');
const energyAmount = document.getElementById('energyAmount');
const evMaxVoltage = document.getElementById('evMaxVoltage');
const evMaxCurrent = document.getElementById('evMaxCurrent');
const evMinCurrent = document.getElementById('evMinCurrent');
const mod = document.getElementById('mod');
socket.on('update_charging_needs', (data) => {
    evseId.textContent = data.evseId;
    departureTime.textContent = data.departureTime;
    energyAmount.textContent = data.energyAmount + "Wh";
    evMaxVoltage.textContent = data.evMaxVoltage + "V";
    evMaxCurrent.textContent = data.evMaxCurrent + "A";
    evMinCurrent.textContent = data.evMinCurrent + "A";
    if (data.mod === 0) {
        mod.textContent = "Adaptive";
    } else if (data.mod === 1) {
        mod.textContent = "Minimum charging time";
    } else if (data.mod === 2) {
        mod.textContent = "Minimum charging cost";
    }
});

// update connection status
const connectionStatus = document.getElementById('connectionStatus');

socket.on('update_connection_status', (data) => {
    if (data.connection_status) {
        connectionStatus.innerText = '✅ Connected to ip: ' + data.ip;
        connectionStatus.classList.remove('disconnected');
        connectionStatus.classList.add('connected');
    } else {
        connectionStatus.innerText = '❌ No Connection ';
        connectionStatus.classList.remove('connected');
        connectionStatus.classList.add('disconnected');
    }
});

// update results
const optimizationResults = document.getElementById('optimizationResults');
const chargingImg = document.getElementById('chargingImg');
const comparisonImg = document.getElementById('comparisonImg');

socket.on('update_results', (data) => {
    if (data.results) {
        optimizationResults.innerText = '✅ Optimize Success ';
        optimizationResults.classList.remove('failed');
        optimizationResults.classList.add('success');
        chargingImg.src = `data:image/png;base64,${data.img_charging}`;
        comparisonImg.src = `data:image/png;base64,${data.img_comparison}`;
    } else {
        optimizationResults.innerText = '❌ Optimization failed ';
        optimizationResults.classList.remove('success');
        optimizationResults.classList.add('failed');
        chargingImg.src = `https://via.placeholder.com/500x200?text=充电随时间变化图`;
        comparisonImg.src = `https://via.placeholder.com/500x200?text=充电随时间变化图`;
    }
});
