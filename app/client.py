html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Real-time shit</h1>

        <script>
            var ws = new WebSocket("ws://localhost:5000/getEvents/payment?user_id=1&organization_id=1");
            ws.onmessage = function(event) {
                console.log(event.data);
            };
            var ws1 = new WebSocket("ws://localhost:5000/getEvents/guest?user_id=1&organization_id=1");
            ws1.onmessage = function(event) {
                console.log(event.data);
            };
            var ws2 = new WebSocket("ws://localhost:5000/getEvents/reservation?user_id=1&organization_id=1");
            ws2.onmessage = function(event) {
                console.log(event.data);
            };
        </script>
    </body>
</html>
"""