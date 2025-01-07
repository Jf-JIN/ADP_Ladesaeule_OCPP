
const socket = io();

test_button = document.getElementById("test_Button");
test_button.addEventListener('click', () => {
    console.log('testfdsafsadfsdfsadfasdfasfdsafasdfsafdsafsdfsadfdsafdsf');
    socket.emit('test', 'test');
})