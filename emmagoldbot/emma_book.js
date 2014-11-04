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

function post_next_if_multi(error, response) {
    if (response) {
	console.log('~\n!!\n~anarchy~\n!!\n~');
	console.log(linenum);
	linenum += 1;
	quote = data[linenum];
	if (i < tweet_parts) {
	    i+=1;
	    T.post('statuses/update', { status: quote }, post_next_if_multi);
	} else {
	    i=0;
	}
    }
    if (error) {
	console.log('Error with twitter:',error);
    }
}

function readbook() {
    var match_array;
    if (!quote) {
	return;
    }
    match_array = quote.match(re);
    if (match_array != null) {
	tweet_parts = match_array[2]-1;
        i = 0;
    }
    else {
	tweet_parts = 1;
    }
    T.post('statuses/update', { status: quote }, post_next_if_multi);
}

readbook();
// DO THE STUFF
// time is in ms!
setInterval(readbook, 1000*60*60);
