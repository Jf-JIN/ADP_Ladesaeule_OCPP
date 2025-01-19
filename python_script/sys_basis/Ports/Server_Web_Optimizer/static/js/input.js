
// update condole
const opt_console = document.getElementById('console_contain');

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
    }
});
