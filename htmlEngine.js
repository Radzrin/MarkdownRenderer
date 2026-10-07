let http = require('http');
let port = 8080;

if(process.argv.length === 2){
  console.error("try 2 arguments")
  process.exit(1);
}


http.createServer(function (req, res) {
  console.log("server created on http://127.0.0.1:" + port)
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.end('Hello World!');
}).listen(port);