//
// begin setup CLI
//
var setupCLI = () => {
	cli.on('table_subscribe', (params) => {
		if(typeof(params.tables) === 'undefined') {
			console.log('command error: "tables" parameter is missing.');
		} else {
			table_subscribe(params.tables);
		}
	});
	cli.on('table_unsubscribe', (params) => {
		if(typeof(params.tables) === 'undefined') {
			console.log('command error: "tables" parameter is missing.');
		} else {
			table_unsubscribe(params.tables);
		}
	});
}
//
// end setup CLI
//

//
// begin main functions
//
var tableUpdate = (update) => {
	try {
		var jsonData = JSON.parse(update);
		console.log(`Table update: ${JSON.stringify(jsonData)}`);
	} catch (e) {
		console.log('table update JSON parse error: ', e);
		return;
	}
}

var table_subscribe = (models) => {
	for (var i in models) {
		socket.on(models[i], tableUpdate);
	}
	cli.emit('send',{ "method":"POST", "resource":"/trading/subscribe", "params": { "models":models } })
}

var table_unsubscribe = (models) => {
	for (var i in models) {
		socket.removeListener(models[i], tableUpdate);
	}
	cli.emit('send',{ "method":"POST", "resource":"/trading/unsubscribe", "params": { "models":models } })
}
//
// end main functions
//

//
// begin module boilerplate
//
var cli;
var socket;
var initdone = false;

// called when the module is being loaded
exports.init = (c, s) => {
	if (!initdone) {
		cli = c;
		socket = s;
		setupCLI();
	}
	initdone = true;
}
//
// end module boilerplate
//