const cfb = require("cfb-data");
const fs = require("fs");
const mongoose = require("mongoose");

const { Game } = require("./database/schema");
const database = require("./database/database");

mongoose.connect(
  database(),
  { useNewUrlParser: true }
);

// get FBS historical scoreboard data
const input = {
  year: 2016,
  week: 10
};

// must change year manually and even then it can crash.  Need to sleep in each loop.
const year = 2017;

var years = [];
for (var i = year; i <= year; i++) {
  years.push(i);
}

var weeks = [];
for (var i = 1; i <= 16; i++) {
  weeks.push(i);
}

var inputs = [];
years.map(year => {
  weeks.map(week => {
    inputs.push({ year: year, week: week, seasontype: 2 });
  });
});

// console.log(inputs);

const getScores = inputs => {
  cfb.scoreboard.getScoreboard(inputs).then((res, err) => {
    if (!res["events"].length) {
      console.log("No games");
    } else {
      res["events"].map(obj => {
        const newGameHome = Game({
          date: obj["date"],
          year: obj["season"]["year"],
          gameID: obj["id"],
          neutralSite: obj["competitions"][0]["neutralSite"],
          conferenceCompetition:
            obj["competitions"][0]["conferenceCompetition"],
          teamID: obj["competitions"][0]["competitors"][0]["id"],
          teamAbbr:
            obj["competitions"][0]["competitors"][0]["team"]["abbreviation"],
          homeAway: obj["competitions"][0]["competitors"][0]["homeAway"],
          pointsFor: obj["competitions"][0]["competitors"][0]["score"],
          pointsAgainst: obj["competitions"][0]["competitors"][1]["score"]
        }).save((err, data) => {
          if (err) return res.send(err);
        });

        const newGameAway = Game({
          date: obj["date"],
          year: obj["season"]["year"],
          gameID: obj["id"],
          neutralSite: obj["competitions"][0]["neutralSite"],
          conferenceCompetition:
            obj["competitions"][0]["conferenceCompetition"],
          teamID: obj["competitions"][0]["competitors"][1]["id"],
          teamAbbr:
            obj["competitions"][0]["competitors"][1]["team"]["abbreviation"],
          homeAway: obj["competitions"][0]["competitors"][1]["homeAway"],
          pointsFor: obj["competitions"][0]["competitors"][1]["score"],
          pointsAgainst: obj["competitions"][0]["competitors"][0]["score"]
        }).save((err, data) => {
          if (err) return res.send(err);
        });
      });
    }
  });
};

inputs.map(input => {
  console.log(input);
  getScores(input);
});

setTimeout(() => {
  mongoose.disconnect();
}, 5 * 1000);
