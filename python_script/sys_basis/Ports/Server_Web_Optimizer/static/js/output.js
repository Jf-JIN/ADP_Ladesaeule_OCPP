
const socket = io();

submit_button = document.getElementById("submit_Button");
submit_success = document.getElementById("successMessage");

submit_button.addEventListener('click', () => {
    submit_success.style.display = 'none'; // 隐藏成功提示

    let max_grid_power = document.getElementById("MaxGridPower").value.trim();
    let interval = document.getElementById("chargeInterval").value.trim();
    let file_eprices = document.getElementById("eprices").files[0];

    let errors = [];

    // 验证最大电网功率
    if (!max_grid_power) {
        errors.push("■ The maximum power grid power cannot be empty");
    } else {
        let maxPower = parseInt(max_grid_power, 10);
        if (isNaN(maxPower)) {
            errors.push("■ The maximum power grid power must be effective figures");
        } else if (maxPower <= 0) {
            errors.push("■ The maximum power grid power must be greater than 0");
        }
    }

    // 验证充电间隔
    if (!interval) {
        errors.push("■ The charging interval cannot be empty");
    }

    // 验证文件类型
    if (file_eprices) {
        let fileName = file_eprices.name.toLowerCase();
        if (!fileName.endsWith('.csv')) {
            errors.push("■ Only support uploading CSV format files");
        }
    }

    // 如果有错误则弹窗提示
    if (errors.length > 0) {
        alert("Error：\n\n" + errors.join('\n'));
        return; // 阻止继续执行
    }

    // 类型转换
    let maxPower = parseInt(max_grid_power, 10);
    let intervalNum = parseInt(interval, 10);

    // 文件处理逻辑
    if (file_eprices) {
        let reader = new FileReader();
        reader.onload = function(event) {
            let csvData = event.target.result;
            socket.emit('submit', {
                'max_grid_power': maxPower,
                'charging_interval': intervalNum,
                'eprices': csvData
            });
            submit_success.style.display = 'block';
        };
        reader.readAsText(file_eprices);
    } else {
        socket.emit('submit', {
            'max_grid_power': maxPower,
            'charging_interval': intervalNum
        });
        submit_success.style.display = 'block';
    }
});