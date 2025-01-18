
const socket = io();

socket.on('current_time', (data) => {
    displayer = document.getElementById('span_current_time');
    displayer.textContent = data;
});

socket.on('redirect_to_login', () => {
    window.location.href = '/';
});

logout_button = document.getElementById('logout');
logout_button.addEventListener('click', () => {
    socket.emit('logout');
})

test_btn = document.getElementById('test_btn');
test_btn.addEventListener('click', () => {
    socket.emit('input_data', 'home');
})