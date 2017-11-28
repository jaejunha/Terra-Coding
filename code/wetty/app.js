var express = require('express');
var http = require('http');
var https = require('https');
var path = require('path');
var server = require('socket.io');
var pty = require('pty.js');
var fs = require('fs');
var wettyPort = '3000'

var opts = require('optimist')
    .options({
        sslkey: {
            demand: false,
            description: 'path to SSL key'
        },
        sslcert: {
            demand: false,
            description: 'path to SSL certificate'
        },
        sshhost: {
            demand: false,
            description: 'ssh server host'
        },
        sshport: {
            demand: false,
            description: 'ssh server port'
        },
        sshuser: {
            demand: false,
            description: 'ssh user'
        },
        sshauth: {
            demand: false,
            description: 'defaults to "password", you can use "publickey,password" instead'
        },
        port: {
            demand: false,
            alias: 'p',
            description: 'wetty listen port'
        },
    }).boolean('allow_discovery').argv;

var runhttps = false;
var sshport = 22;
var sshhost = 'localhost';
var globalsshuser = '';

if (opts.sshport) {
    sshport = opts.sshport;
}

if (opts.sshhost) {
    sshhost = opts.sshhost;
}

if (opts.sshauth) {
	sshauth = opts.sshauth
}

if (opts.sshuser) {
    globalsshuser = opts.sshuser;
}

if (opts.sslkey && opts.sslcert) {
    runhttps = true;
    opts['ssl'] = {};
    opts.ssl['key'] = fs.readFileSync(path.resolve(opts.sslkey));
    opts.ssl['cert'] = fs.readFileSync(path.resolve(opts.sslcert));
}

process.on('uncaughtException', function(e) {
    console.error('Error: ' + e);
});

var httpserv;

var app = express();
app.get('/wetty/ssh/:user', function(req, res) {
    res.sendfile(__dirname + '/public/wetty/index.html');
});

app.use('/', express.static(path.join(__dirname, 'public')));

if (runhttps) {
    httpserv = https.createServer(opts.ssl, app).listen('3000', function() {
        console.log('https on port ' + '3000');
    });
} else {
    httpserv = http.createServer(app).listen('3000', function() {
        console.log('http on port ' + '3000');
    });
}

var io = server(httpserv,{path: '/wetty/socket.io'});
io.on('connection', function(socket){

	var pathFromUser = '';
    var sshuser = '';
    var request = socket.request;
    console.log((new Date()) + ' Connection accepted.');
    //if (match = request.headers.referer.match('/wetty/ssh/.+$')) {
    if( match = request.headers.referer.match('/wetty/ssh/.+$')) {
	pathFromUser = match[0].replace('/wetty/ssh/', '');
    pathFromUser = pathFromUser.replace(/,/gi, '/');
	var tempResult = pathFromUser.split('@');
	var extension = tempResult[0];
	var execute_command = tempResult[1];
	var fileName = tempResult[2];
	console.log('pathFromUser -->' + pathFromUser);
	}
    var term;
    if (process.getuid() == 0) {
		console.log('UID = 0')
		term = pty.spawn('sshpass', ['-p', '1234', 'ssh', '-o', 'StrictHostKeyChecking=no', 'root@localhost'], {
            name: 'xterm-256color',
            cols: 80,
            rows: 30
        });
    } else {
		console.log('UID ELSE')
		term = pty.spawn('sshpass', ['-p', '1234', 'ssh', '-o', 'StrictHostKeyChecking=no', 'root@localhost'], {
            name: 'xterm-256color',
            cols: 80,
            rows: 30
        });
    }

	/* Initial Settings for connected user */
	term.write('cd /root/Desktop/git_t/code/\n');
	term.write('clear\n');

	/* Execute Command */
	if( extension == '.c')
	{
		console.log("This is extension of .c");
		term.write(execute_command + '.main' +' && exit\n');
	}else if( extension == '.java')
	{
		fileName = fileName.replace('.java', '')
		console.log("This is extension of .java");
		term.write('java -cp '+ execute_command + ' ' + fileName + ' && exit\n');
	}else if( extension == '.py')
	{
		term.write('python ' + execute_command + fileName + ' && exit\n');
	}else{
		term.write('exit\n');
	}
	
    term.on('data', function(data) {
		socket.emit('output', data);
    });
    term.on('exit', function(code) {
        console.log((new Date()) + " PID=" + term.pid + " ENDED")
    });
    socket.on('resize', function(data) {
        term.resize(data.col, data.row);
    });

    socket.on('input', function(data) {
		if( data.charCodeAt(0) != 3 && data.charCodeAt(0) != 26) // which means CTRL+C
		{
        	term.write(data);
		}
    });
    socket.on('disconnect', function() {
        term.end();
    });
});
