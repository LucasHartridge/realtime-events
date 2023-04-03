import ws from 'k6/ws';
import { check } from 'k6';

export default function () {
    const user_id = 1
    const channels = ["payment", "guest", "reservation"]
    const channel = channels[Math.floor(Math.random() * channels.length)];

    const organization_ids = ["99999"]
    const organization_id = organization_ids[Math.floor(Math.random() * organization_ids.length)];

    const url = `ws://localhost:5000/getEvents/${channel}?organization_id=${organization_id}&user_id=${user_id}`;

    const res = ws.connect(url, null, function (socket) {
        socket.on('open', () => console.log('connected'));
        socket.on('message', (data) => console.log('Message received: ', data));
        socket.on('close', () => console.log('disconnected'));
    });

    check(res, { 'status is 101': (r) => r && r.status === 101 });
}