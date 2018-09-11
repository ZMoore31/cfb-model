const cfb = require("cfb-data");
const fs = require("fs");
const mongoose = require("mongoose");

const { Recruiting } = require("./database/schema");
const database = require("./database/database");

mongoose.connect(
  database(),
  { useNewUrlParser: true }
);

var years = [];
for (var i = 2001; i <= 2018; i++) {
  years.push(i);
}

years.forEach(year => {
  for (i = 1; i <= 6; i++) {
    cfb.recruiting.getSchoolRankings(year, i).then(result => {
      result.map(obj => {
        const newRecruiting = Recruiting({
          year: year,
          rank: obj.rank === "N/A" ? "" : obj.rank,
          school: obj.school,
          totalCommits: obj.totalCommits,
          fiveStars: obj.fiveStars,
          fourStars: obj.fourStars,
          threeStars: obj.threeStars,
          averageRating: obj.averageRating,
          points: obj.points
        }).save((err, data) => {
          if (err) return res.send(err);
          console.log("Success");
        });
      });
    });
  }
});
