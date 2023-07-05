//
// begin setup CLI
//
var setupCLI = () => {
	cli.on('price_subscribe', (params) => {
		if(typeof(params.pairs) === 'undefined') {
			console.log('command error: "pairs" parameter is missing.');
		} else {
			subscribe(params.pairs);
		}
	});
	cli.on('price_unsubscribe', (params) => {
		if(typeof(params.pairs) === 'undefined') {
			console.log('command error: "pairs" parameter is missing.');
		} else {
			unsubscribe(params.pairs);
		}
	});
}
//
// end setup CLI
//

//
// begin main functions
//
var priceUpdate = (update) => {
	try {
		var jsonData = JSON.parse(update);
		// JavaScript floating point arithmetic is not accurate, so we need to round rates to 5 digits
		// Be aware that .toFixed returns a String
		jsonData.Rates = jsonData.Rates.map(function(element){
			return element.toFixed(5);
		});
		console.log(`@${jsonData.Updated} Price update of [${jsonData.Symbol}]: ${jsonData.Rates}`);
	} catch (e) {
		console.log('price update JSON parse error: ', e);
		return;
	}
}

var subscribe = (pairs) => {
	var callback = (statusCode, requestID, data) => {
		if (statusCode === 200) {
			try {
				var jsonData = JSON.parse(data);
			} catch (e) {
				console.log('subscribe request #', requestID, ' JSON parse error: ', e);
				return;
			}
			if(jsonData.response.executed) {
				try {
					for(var i in jsonData.pairs) {
						socket.on(jsonData.pairs[i].Symbol, priceUpdate);
					}
				} catch (e) {
					console.log('subscribe request #', requestID, ' "pairs" JSON parse error: ', e);
					return;
				}
			} else {
				console.log('subscribe request #', requestID, ' not executed: ', jsonData);
			}
		} else {
			console.log('subscribe request #', requestID, ' execution error: ', statusCode, ' : ', data);
		}
	}
	cli.emit('send',{ "method":"POST", "resource":"/subscribe", "params": { "pairs":pairs }, "callback":callback })
}

var unsubscribe = (pairs) => {
	var callback = (statusCode, requestID, data) => {
		if (statusCode === 200) {
			try {
				var jsonData = JSON.parse(data);
			} catch (e) {
				console.log('unsubscribe request #', requestID, ' JSON parse error: ', e);
				return;
			}
			if(jsonData.response.executed) {
				try {
					for(var i in jsonData.pairs) {
						socket.removeListener(jsonData.pairs[i], priceUpdate);
					}
				} catch (e) {
					console.log('unsubscribe request #', requestID, ' "pairs" JSON parse error: ', e);
					return;
				}
			} else {
				console.log('unsubscribe request #', requestID, ' not executed: ', jsonData);
			}
		} else {
			console.log('unsubscribe request #', requestID, ' execution error: ', statusCode, ' : ', data);
		}
	}
	cli.emit('send',{ "method":"POST", "resource":"/unsubscribe", "params": { "pairs":pairs }, "callback":callback })
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