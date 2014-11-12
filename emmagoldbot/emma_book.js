// https://github.com/dariusk/examplebot
// load stuff and things
var Twit = require('twit');
var fs = require('fs');

// config file
var T = new Twit(require('./emma_config.js'));

var data = fs.readFileSync('./pg2162_clean.txt.twit','utf8').toString().split('\n');
var linenum = 0;
var tweet_parts, i=0;
var re = /\(([0-9]+)\/([0-9]+)\)$/;
var quote = data[linenum];

function post_no_next(error, response) {
    if (response) {
	console.log(quote);
	console.log("\n");
	linenum += 1;
	quote = data[linenum];
    }
    if (error) {
	console.log("Twitter Error: ", error);
    }
}

function post_next_if_multi(error, response) {
    var match_array;
    if (response) {
	console.log(quote);
	linenum += 1;
	quote = data[linenum];
	match_array = quote.match(re);
	if (match_array) {
	    if (match_array[1] == match_array[2]) {
		T.post('statuses/update', { status: quote }, post_no_next);
	    } else if (match_array[1] < match_array[2]) {
		readbook();
	    }
	}
    }
    if (error) {
	console.log('Twitter Error: ',error);
    }
}

function readbook() {
    var match_array;
    if (!quote) {
	return;
    }
    match_array = quote.match(re);
    if (match_array) {
	T.post('statuses/update', { status: quote }, post_next_if_multi);
    } else {
	T.post('statuses/update', { status: quote }, post_no_next);
    }
}


readbook();
// DO THE STUFF
// time is in ms!
setInterval(readbook, 1000*60*60);
