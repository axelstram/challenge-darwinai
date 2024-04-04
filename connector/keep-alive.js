const http = require('http');

const TARGET_URL = 'http://connector-ubxv3t5y.b4a.run/';
const PORT = process.env.PORT || 80;
const INTERVAL = 5 * 60 * 1000; // 5 minutes in milliseconds

function keepAlive() {
  http.get(`${TARGET_URL}:${PORT}`  , () => {
    console.log('keep alive');
  });
}

keepAlive();
setInterval(keepAlive, INTERVAL);