

// Replace <task_id> with the actual value
var random_id = "test"

// random_id = random_id();

if (random_id) {
    // Create the WebSocket connection
    var socket = new WebSocket('ws://' + window.location.host + '/ws/group/' + random_id + '/');

    // Event handler for successful connection
    socket.onopen = function (event) {
        console.log('WebSocket connection established');

        // You can perform any necessary actions after the connection is established
    };

    // Event handler for receiving messages
    socket.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log(typeof message)
        console.log('Received message:', message);
        if (message.type != "data_converted") {
            window.alert(message.result);
        }

        // Handle the received message as needed
    };

    // Event handler for connection close
    socket.onclose = function (event) {
        console.log('WebSocket connection closed');

        // You can perform any necessary actions after the connection is closed
    };
}



