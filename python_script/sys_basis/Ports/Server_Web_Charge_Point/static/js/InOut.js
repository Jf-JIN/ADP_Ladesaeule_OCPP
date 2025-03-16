// This file has not been obfuscated. If it is used officially, it is recommended to obfuscate it.
// This script is mainly used for the common logical parts of the user and administrator interfaces, such as displaying the current time, checking input, etc.

const socket = io();

console.log('Client connected');

socket.on('current_time', (data) => {
    displayer = document.getElementById('span_current_time');
    displayer.textContent = data;
});

socket.on('redirect_to_login', () => {
    window.location.href = '/';
});

const logout_button = document.getElementById('logout');
logout_button.addEventListener('click', () => {
    socket.emit('logout');
})

// const test_btn = document.getElementById('test_btn');
// test_btn.addEventListener('click', () => {
//     socket.emit('input_data', 'home');
// })
function isValidNumber (input) {
    return /^[+-]?\d+(\.\d+)?$/.test(input);
}
const submit_btn = document.getElementById('save_settings');
submit_btn.addEventListener('click', () => {
    function collect_data () {
        let res = {
            'charge_request': {
                'evse_id': document.getElementById('evse_id').value,
                'charge_mode': document.getElementById('charge_mode').value,
                'charge_power': document.getElementById('charge_power').value,
                'depart_time': document.getElementById('depart_time').value,
            }
        }
        return res
    }
    
    function check_data (data) {
        let check_res = true;
        if (!('charge_request' in data)) {
            return false;
        }
        data = data.charge_request
        for (let [key, value] of Object.entries(data)) {
            let widget = document.getElementById(key);
            console.log(widget)
            if (widget) {
                if (key =='charge_mode' && value == -1) {
                    return true
                }
                if (value == '') {
                    alert(`Please fill all fields. ${key} is empty.`);
                    widget.style.backgroundColor = 'red';
                    check_res = false;
                    return check_res
                } else {
                    widget.style.backgroundColor = '';
                }
                if (key == 'charge_power') {
                    if (!isValidNumber(value)) {
                        alert(`Please enter a valid number. ${key} is not a number.`);
                        widget.style.backgroundColor = 'red';
                        check_res = false;
                        return check_res
                    } else if (parseFloat(value) <= 0) {
                        alert(`Please enter a valid number. ${key} is not a positive number.`);
                        widget.style.backgroundColor = 'red';
                        check_res = false;
                    } else {
                        widget.style.backgroundColor = '';
                    }
                } else if (key == 'depart_time') {
                    let currentTime = new Date();
                    let selectedTime = new Date(value);
                    if (selectedTime < currentTime) {
                        alert("The selected time cannot be in the past. Please choose a valid time.");
                        value = ''; // 清空输入框值
                        widget.style.backgroundColor = 'red';
                        check_res = false;
                        return check_res;
                    }
                    let isoDate = new Date(value).toISOString().split('.')[0] + 'Z'; // 去掉毫秒部分
                    data[key] = isoDate;
                }
            } else {
                console.error(`Element with id '${key}' not found.`);
            }
        }
        return check_res
    }
    data = collect_data();
    let res = check_data(data);
    if (res) {
        socket.emit('input_data', data); // If the key name 'input data' is changed, please also change the corresponding listener part in 'Thread_Server_Web.py'
    }
})

const btn_charge_now = document.getElementById('charge_now');
btn_charge_now.addEventListener('click', () => {
    socket.emit('input_data', {
        "charge_now": {
            "evse_id": document.getElementById('evse_id').value,
            "charge_mode": document.getElementById('charge_mode').value,
            }
        }
    ); 
})

const btn_stop = document.getElementById('stop');
btn_stop.addEventListener('click', () => {
    socket.emit('input_data', { "stop": { "evse_id": document.getElementById('evse_id').value }});
})

const btn_implement_page_manual = document.getElementById("implement");
const textEdit = document.getElementById("manual_input");
btn_implement_page_manual.addEventListener("click", () => {
    target_energy = document.getElementById('manual_target_energy').value;
    departure_time = document.getElementById('manual_depart_time').value;
    data = textEdit.value;
    if (!checkManualInput(data, target_energy, departure_time)) {
        return;
    }
    let isoDate = new Date(departure_time).toISOString().split('.')[0] + 'Z'; // 去掉毫秒部分
    socket.emit('input_data', { 'manual_input': { 'depart_time' : isoDate, 'target_energy': target_energy, 'data': data }})
})

function checkManualInput (data, target_energy, depart_time) {
    if (!isValidNumber(target_energy)) {
        alert(`Please enter a valid number. ${key} is not a number.`);
        return false
    } else if (parseFloat(target_energy) <= 0) {
        alert(`Please enter a valid number. ${key} is not a positive number.`);
        return false;
    }
    let currentTime = new Date();
    let selectedTime = new Date(depart_time);
    if (selectedTime < currentTime) {
        alert("The selected time cannot be in the past. Please choose a valid time.");
        return false;
    }
    if (data.length == 0) {
        alert("Text field cannot be empty");
        return false;
    }
    console.log(data)
    try {
        JSON.parse(data)
    } catch(e) {
        console.log(e)
        alert("Text field must be a valid JSON string");
        return false;
    }
    return true;
}