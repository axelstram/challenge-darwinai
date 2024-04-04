const http = require('http');

const TARGET_URL1 = 'http://connector-ubxv3t5y.b4a.run/';
const TARGET_URL2 = 'http://darwinai-n3s5o067.b4a.run/';
const PORT1 = process.env.PORT || 80;
const PORT2 = process.env.PORT || 8000;
const INTERVAL = 5 * 60 * 1000; // 5 minutes in milliseconds

function keepAlive() {
  http.get(`${TARGET_URL1}:${PORT1}`  , () => {
    console.log('keep alive 1');
  });

  http.get(`${TARGET_URL2}:${PORT2}`  , () => {
    console.log('keep alive 2');
  });
}

keepAlive();
setInterval(keepAlive, INTERVAL);