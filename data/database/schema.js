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
