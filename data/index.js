const cfb = require('cfb-data');
const year = 2010

const result = cfb.recruiting.getSchoolRankings(year,1);

console.log(JSON.stringify(result));