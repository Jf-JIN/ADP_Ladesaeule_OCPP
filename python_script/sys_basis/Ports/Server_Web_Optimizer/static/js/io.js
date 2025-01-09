
const socket = io();

update_button = document.getElementById("update_Button");
update_button.addEventListener('click', () => {
    const max_grid_power = document.getElementById("max_grid_power").value;
    socket.emit('update', {'max_grid_power':max_grid_power});
})