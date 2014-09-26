// https://github.com/dariusk/examplebot
// load stuff and things
var Twit = require('twit');
var fs = require('fs');

// config file
var T = new Twit(require('./config.js'));

function randomInt (low, high) {
    return Math.floor(Math.random() * (high - low) + low);
}


// URL search for planet hacking
var HackThePlanet = {q: '"hack the planet" OR "#hacktheplanet" OR "hacktheplanet" -Upworthy -from:sylveonk', count: 100, result_type: "recent"};

// find latest tweet referencing HACK THE PLANET!, retweets it
function retweetLatest() {
    T.get('search/tweets', HackThePlanet, function (error, data){
        //console.log(error);
        // if no errors
        if (!error) {
            // grab ID of tweet to retweet
            var which = randomInt(0,100);
//            var which = 0;
            var retweetId = data.statuses[which].id_str;
//            var retweetId = data.statuses[0].id_str;
            var userId = data.statuses[0].user;
            var textId = data.statuses[0].text;
//            console.log(userId,textId);
//            console.log(data);
            // ... retweet it
            T.post('statuses/retweet/' + retweetId, { }, function (error, response) {
               if (response) {
                   console.log('.\n..\n...\nPLANET HACKED\n...\n..\n.')
               }
              // if error with twitter call
               if (error) {
                   console.log('Error with twitter:',error);
                // I think there are often problems with trying to retweet
                // 'protected' tweets (not sure what that is exactly) so it
                // should probably keep trying until it succeeds...
               }
           })
        }
        // if original search request had error, record here
        else {
            console.log('Error with PLANET HACK search:',error);
        }
    });
}

// DO THE STUFF
retweetLatest();
// time is in ms!
setInterval(retweetLatest, 1000*60*30);
