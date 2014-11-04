// https://github.com/dariusk/examplebot
// load stuff and things
var Twit = require('twit');
var fs = require('fs');

// config file
var T = new Twit(require('./emma_config.js'));

var data = fs.readFileSync('./pg2162_clean.txt.twit','utf8').toString().split('\n');
var linenum = 0;
function readbook() {
    quote = data[linenum];
    linenum = linenum + 1;
    console.log(linenum,quote);
    T.post('statuses/update', { status: quote }, function (error, response) {
        if (response) {
            console.log('~\n!!\n~anarchy~\n!!\n~');
            console.log(linenum);
        }
        // if error with twitter call
        if (error) {
            console.log('Error with twitter:',error);
        }
    });
}

readbook();
// DO THE STUFF
// time is in ms!
setInterval(readbook, 1000*60*5);
