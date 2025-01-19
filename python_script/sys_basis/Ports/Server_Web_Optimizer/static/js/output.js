
const socket = io();

submit_button = document.getElementById("submit_Button");
submit_button.addEventListener('click', () => {
    const max_grid_power = document.getElementById("MaxGridPower").value;
    const interval = document.getElementById("chargeInterval").value;
    const file_eprices = document.getElementById("eprices").files[0];
    if (file_eprices) {
        const reader = new FileReader();

        reader.onload = function(event) {
            const csvData = event.target.result;
            const dataToSubmit = {
                'max_grid_power': max_grid_power,
                'charging_interval': interval,
                'eprices': csvData,
            };
            socket.emit('submit', dataToSubmit);
        };

        reader.readAsText(file_eprices);
    } else {
        socket.emit('submit', {
            'max_grid_power': max_grid_power,
            'charging_interval': interval,
        });
    }
})