const http = require('http');

const TARGET_URL = 'https://connector-ubxv3t5y.b4a.run/';
const INTERVAL = 25 * 60 * 1000; // 25 minutes in milliseconds

function keepAlive() {
  http.get(TARGET_URL, () => {
    // Do nothing 
  });
}

keepAlive();
setInterval(keepAlive, INTERVAL);