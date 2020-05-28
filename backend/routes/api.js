var express = require('express');
var jwt = require('jsonwebtoken');
var mysql = require('mysql');

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
  let sql = "SELECT users.email as email, COALESCE(SUM(scores.dscore), 0) AS score FROM users LEFT JOIN scores ON users.email = scores.email ";
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
	    console.log({...result[0]});
      res.json({ ...result[0] });
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
