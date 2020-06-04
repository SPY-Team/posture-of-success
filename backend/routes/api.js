var express = require('express');
var jwt = require('jsonwebtoken');
var mysql = require('mysql');
var moment = require('moment');
var momentDurationFormatSetup = require("moment-duration-format");
momentDurationFormatSetup(moment);

var con = mysql.createConnection({
  host: "localhost",
  user: "admin",
  password: "posture-of-success",
  database: "mydb"
});

con.connect();

var router = express.Router();

router.post('/device/signin', (req, res) => {
  var valid = false;
  var { email, password } = req.body;
  let sql = "SELECT users.email as email, COALESCE(SUM(scores.dscore), 0) AS score, users.sensor_data AS sensor_data FROM users LEFT JOIN scores ON users.email = scores.email ";
  sql += "WHERE users.email = ? AND users.password = ? ";
  sql += "GROUP BY users.email";

  var params = [email, password];

  console.log( req.body );
  con.query(sql, params, (err, result) => {
    if (err) { console.log(err); res.json({ success: false }); }
    else if (result.length == 0) res.json({ success: false });
    else res.json({ success: true, ...result[0] });
  });
});

router.post('/device/update_score', (req, res) => {
  var { email, duration, dscore } = req.body;
  var sql = "insert into scores ( email, duration, dscore ) values ( ?, ?, ? )";
  var params = [email, duration, dscore];

  console.log( req.body );
  con.query(sql, params, (err, result) => {
    if (err) { console.log(err); res.json({ success: false }); }
    else res.json({ success: true });
  });
});

router.post('/device/update_sensor_data', (req, res) => {
  var { email, sensor_data } = req.body;
  var sql = "update users set sensor_data=? where email=?";
  var params = [sensor_data, email];

  console.log( req.body );
  con.query(sql, params, (err, result) => {
    if (err) { console.log(err); res.json({ success: false }); }
    else res.json({ success: true });
  });
});

router.post('/device/init_sensor', (req, res) => {
  var valid = false;
  var { email, sensor_data } = req.body;
  var sql = "update users set sensor_data=? where email=?";
  var params = [sensor_data, email];

  console.log( req.body );
  con.query(sql, params, (err, result) => {
    if (err) { console.log(err); res.json({ success: false }); }
    else if (result.length == 0) res.json({ success: false });
    else res.json({ success: true });
  });
});

router.post('/get_data', (req, res) => {
  var { email } = req.body;
  var sql = "select username, score, duration, week_score, week_duration, score_rank from ranks where email=?";
  var params = [email];
  con.query(sql, params, (err, result) => {
    if (err) { console.log(err); res.json({ success: false }); }
    else if (result.length == 0) res.json({ success: false });
    else {
      result[0].duration = moment.duration(result[0].duration, "seconds").format("h시간 mm분");
      res.json({ ...result[0] });
    }
  });
});

router.post('/get_graph_data', (req, res) => {
  var { email } = req.body;
  var sql = "select receive_time, duration, dscore from scores where email=?";
  var params = [email];
  con.query(sql, params, (err, result) => {
    if (err) { console.log(err); res.json({ success: false }); }
    else {
      let score = 0;
      result.forEach(e => {
	score += e.dscore;
        e.score = Math.floor(score);
	e.receive_time = moment(e.receive_time).format('MM/DD HH:mm');
      })
      let formatted_result = [];
      const N = 50;
      if (result.length <= N)
	    formatted_result = result;
      else {
	for (let i = 0; i<N-1; i++) {
          formatted_result.push(result[Math.floor(i/50*result.length)]);
	}
	formatted_result.push(result[result.length-1]);
      }
      res.json({ graph_data: formatted_result });
    }
  });
});

router.post('/get_leaderboard', (req, res) => {
  var { email } = req.body;
  var sql = "select score_rank, username, score from ranks";
  var params = [email];
  con.query(sql, params, (err, result) => {
    if (err) { console.log(err); res.json({ success: false }); }
    else {
      let score = 0;
      res.json({ leaderboard: result });
    }
  });
});

router.post('/signin', (req, res) => {
  var valid = false;
  var { email, password } = req.body;
  var sql = "select email from users where email=? and password=?";
  var params = [email, password];
  con.query(sql, params, (err, result) => {
    if (err) { console.log(err); res.json({ success: false }); }
    else if (result.length == 0) res.json({ success: false });
    else {
      //let token = jwt.sign({ email: result[0].email }, "Posture-of-Success");
      //res.cookie('jwt',token, { httpOnly: true, maxAge: 3600000 })
      res.json({ email, success: true });
    }
  });
});

router.post('/signup', (req, res) => {
  var { username, email, password } = req.body;
  var sql = "INSERT INTO users (username, email, password) VALUES (?,?,?)";
  var params = [username, email, password];
  con.query(sql, params, (err, result) => {
    if (err) { console.log(err); res.json({ success: false }); }
    res.json({ success: true });
  });
});



module.exports = router;
