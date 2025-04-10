var shell = require('shelljs');

shell.exec(`tsc-watch --onSuccess \"node ./build/main.js ${process.argv.slice(2).join(" ")}\"`)