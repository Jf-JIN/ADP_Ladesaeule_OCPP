// This file has not been obfuscated. If it is used officially, it is recommended to obfuscate it.
// This script is mainly used for the common logical parts of the user and administrator interfaces, such as displaying the current time, checking input, etc.

const socket = io();
var isAllowMessageFromServerPopup = true;
var message_in_waiting = null;

console.log('Client connected');

socket.on('current_time', (data) => {
    displayer = document.getElementById('span_current_time');
    displayer.textContent = data;
});

socket.on('redirect_to_login', () => {
    window.location.href = '/';
});

const logout_button = document.getElementById('logout');
// logout_button.addEventListener('click', async () => {
//     // socket.emit('logout');
//     const result = await Swal.fire(lang_dict.question, lang_dict.logout_question, 'question');
//     if (result.isConfirmed) {
//         const result_2 = await Swal.fire(lang_dict.question, lang_dict.logout_question_2, 'question');
//         if (result_2.isConfirmed) {
//             socket.emit('input_data', {'logout': true});
//         }
//     }
// })
logout_button.addEventListener('click', () => {
    isAllowMessageFromServerPopup = false;
    Swal.fire({
        title: lang_dict.system_operation_question_title,
        text: lang_dict.system_operation_question,
        icon: 'question',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: lang_dict.system_operation_reboot_text,
        denyButtonText: lang_dict.system_operation_shutdown_text,
        cancelButtonText: lang_dict.system_operation_cancel_text
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(lang_dict.question, lang_dict.reboot_question, 'question').then((result_root) => {
                if (result_root.isConfirmed) {
                    socket.emit('input_data', { 'logout': false });
                };
                isAllowMessageFromServerPopup = true;
            });
        } else if (result.isDenied) {
            Swal.fire(lang_dict.question, lang_dict.shutdown_question, 'question').then((result_shutdown_1) => {
                if (result_shutdown_1.isConfirmed) {
                    Swal.fire(lang_dict.question, lang_dict.shutdown_question_2, 'question').then((result_shutdown_2) => {
                        if (result_shutdown_2.isConfirmed) {
                            socket.emit('input_data', { 'logout': true });
                            Swal.fire(lang_dict.question, lang_dict.shutdown_message, 'success')
                        }
                    });
                }
            });
        } else if (result.isDismissed) {
            isAllowMessageFromServerPopup = true;
            if (message_in_waiting) {
                Swal.fire(message_in_waiting.title, message_in_waiting.text, message_in_waiting.type);
            };
        };
    });
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
                        Swal.fire(lang_dict.error, window.lang_dict.time_in_past, 'error');
                        value = '';
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
    if (!checkManualInput(target_energy, departure_time)) {
        return;
    }
    let isoDate = new Date(departure_time).toISOString().split('.')[0] + 'Z';
    socket.emit('input_data', { 'manual_input': { 'depart_time' : isoDate, 'target_energy': target_energy }})
})

function checkManualInput (target_energy, depart_time) {
    if (!isValidNumber(target_energy)) {
        Swal.fire(lang_dict.error, window.lang_dict.TE_not_num, 'error');
        return false
    } else if (parseFloat(target_energy) <= 0) {
        Swal.fire(lang_dict.error, window.lang_dict.TE_not_positive, 'error');
        return false;
    }
    let currentTime = new Date();
    let selectedTime = new Date(depart_time);
    if (selectedTime < currentTime) {
        Swal.fire(lang_dict.error, window.lang_dict.time_in_past, 'error');
        return false;
    }
    // if (data.length == 0) {
    //     alert("Text field cannot be empty");
    //     return false;
    // }
    // console.log(data)
    // try {
    //     JSON.parse(data)
    // } catch(e) {
    //     console.log(e)
    //     alert("Text field must be a valid JSON string");
    //     return false;
    // }
    return true;
}

const drop_zone = document.getElementById('drop_zone');
const btn_file_input = document.getElementById('btn_manual_input');
const input_area = document.getElementById('manual_input');
const fileNameSpan = document.getElementById('file_name');

drop_zone.addEventListener('dragover', (e) => {
    e.preventDefault();
    drop_zone.classList.add('dragover');
});

drop_zone.addEventListener('dragleave', () => {
    drop_zone.classList.remove('dragover');
});

drop_zone.addEventListener('drop', (e) => {
    e.preventDefault();
    drop_zone.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

// 选择文件后处理
btn_file_input.addEventListener('change', () => {
    handleFiles(btn_file_input.files);
    if (fileInput.files.length > 0) {
        fileNameSpan.textContent = fileInput.files[0].name;
    } else {
        fileNameSpan.textContent = window.lang_dict.no_file_selected;
    }
});

function handleFiles (files) {
    if (files.length === 0) return;
    const file = files[0];
    if (!file.type.includes('csv')) {
        Swal.fire(lang_dict.error, window.lang_dict.csv_file_error, 'error');
        return;
    }
    const reader = new FileReader();
    reader.onload = function (e) {
        const fileContent = e.target.result;
        // socket.send(fileContent);
        socket.emit('input_data', { 'manual_input_csv': {'data': fileContent } });
    };
    drop_zone.textContent = file.name;
    btn_file_input.textContent = file.name;
    fileNameSpan.textContent = file.name? file.name: window.lang_dict.select_file_hint;
    reader.readAsText(file);
}

const btn_clear_csv = document.getElementById('btn_clear_csv');
btn_clear_csv.addEventListener('click', () => {
    drop_zone.textContent = window.lang_dict.drop_zone;
    fileNameSpan.textContent = window.lang_dict.select_file_hint;
    socket.emit('input_data', { 'manual_input_csv': { 'data': 'clear' } });
})

const btn_create_csv = document.getElementById('btn_create_example_csv')
btn_create_csv.addEventListener('click', function () {
    const data = [
        ['evseId' ,1],
        ['chargingProfileID',1],
        ['stackLevel' ,1],
        ['chargingProfilePurpose' ,'TxProfile' ],
        ['chargingProfileKind' ,'Absolute' ],
        ['ChargingScheduleID',1],
        ['chargingRateUnit','W'],
        [],
        ['startSchedule', '2025-08-08T08:08:08Z'],
        ['startPeriod_in_second','limit'],
        [0,6666],
    ];

    const csvContent = data.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'example.csv';
    a.click();
    URL.revokeObjectURL(url);
})
