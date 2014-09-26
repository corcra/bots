// https://github.com/dariusk/examplebot
// load stuff and things
var Twit = require('twit');
var fs = require('fs');

// config file
var T = new Twit(require('./config.js'));

var data = fs.readFileSync('./hackers_parsed2.txt','utf8').toString().split('\n');
var linenum = 987;
function tweetHackers() {
    linenum = linenum + 1;
    quote = data[linenum];
    console.log(linenum,quote);
    T.post('statuses/update', { status: quote }, function (error, response) {
        if (response) {
            console.log('~\n!!\n###\nMOVIE QUOTED\n###\n!!\n~');
            console.log(linenum);
        }
        // if error with twitter call
        if (error) {
            console.log('Error with twitter:',error);
        }
    });
}

tweetHackers();
// DO THE STUFF
// time is in ms!
setInterval(tweetHackers, 1000*60*15);
