const mongoose = require("mongoose");
const database = require("./database");

const recruitingSchema = new mongoose.Schema({
  date: { type: Date, default: Date.now },
  year: { type: Number },
  rank: { type: Number },
  school: { type: String },
  totalCommits: { type: Number },
  fiveStars: { type: Number },
  fourStars: { type: Number },
  threeStars: { type: Number },
  averageRating: { type: Number },
  points: { type: Number }
});

module.exports.Recruiting = mongoose.model("Recruiting", recruitingSchema);

const gameSchema = new mongoose.Schema({
  date: { type: Date },
  year: { type: Number },
  gameID: { type: String },
  neutralSite: { type: Boolean },
  conferenceCompetition: { type: Boolean },
  teamID: { type: String },
  teamAbbr: { type: String },
  homeAway: { type: String },
  pointsFor: { type: Number },
  pointsAgainst: { type: Number }
});

module.exports.Game = mongoose.model("Game", gameSchema);
