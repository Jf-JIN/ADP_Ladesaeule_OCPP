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

const test_btn = document.getElementById('test_btn');
test_btn.addEventListener('click', () => {
    socket.emit('input_data', 'home');
})

const submit_btn = document.getElementById('save_settings');
submit_btn.addEventListener('click', () => {
    function collect_data () {
        let res = {
            'charge_mode': document.getElementById('charge_mode').value,
            'charge_power': document.getElementById('charge_power').value,
            'departure_time': document.getElementById('departure_time').value,
        }
        return res
    }
    function check_data (data) {
        let check_res = true;
        for (let [key, value] of Object.entries(data)) {
            let widget = document.getElementById(key);
            console.log(widget)
            if (widget) {
                console.log(widget.id)
                if (value == '') {
                    alert(`Please fill all fields. ${key} is empty.`);
                    widget.style.backgroundColor = 'red';
                    check_res = false;
                    return check_res
                } else {
                    widget.style.backgroundColor = '';
                }
                if (key == 'charge_power') {
                    if (isNaN(parseFloat(value))) {
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
                } else if (key == 'departure_time') {
                    let currentTime = new Date();
                    let selectedTime = new Date(value);
                    console.log(currentTime, selectedTime);
                    if (selectedTime < currentTime) {
                        alert("The selected time cannot be in the past. Please choose a valid time.");
                        value = ''; // 清空输入框值
                        widget.style.backgroundColor = 'red';
                        check_res = false;
                        return check_res;
                    }
                    let isoDate = new Date(value).toISOString().split('.')[0] + 'Z'; // 去掉毫秒部分
                    data[key] = isoDate;
                    console.log(data);
                }
            } else {
                console.error(`Element with id '${key}' not found.`);
            }
        }
        return check_res
    }
    data = collect_data();
    let res = check_data(data);
    console.log(res);
    if (res) {
        socket.emit('input_data', data); // If the key name 'input data' is changed, please also change the corresponding listener part in 'Thread_Server_Web.py'
    }
})