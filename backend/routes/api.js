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
  var sql = "select username from users where email=? and password=?";
  var params = [email, password];

  console.log( req.body );
  con.query(sql, params, (err, result) => {
    if (err) throw err;
    if (result.length == 0) {
      res.json({ success: false });
    } else {
      res.json({ success: true });
    }
  });
});

router.post('/data', (req, res) => {
  var { token } = req.body;
  var { email } = jwt.verify(token, "Posture-of-Success");
  var sql = "select email from users where email=?";
  var params = [email];
  con.query(sql, params, (err, result) => {
    if (err) throw err;
    if (result.length == 0) {
      res.status(403).send("Rejected!");
    } else {
      res.json({ email: result[0].email, data: result[0].username });
    }
  });
}) ;

router.post('/signin', (req, res) => {
  var valid = false;
  var { email, password } = req.body;
  var sql = "select email from users where email=? and password=?";
  var params = [email, password];
  con.query(sql, params, (err, result) => {
    if (err) throw err;
    if (result.length == 0) {
      res.status(403).send("Rejected!");
    } else {
      let token = jwt.sign({ email: result[0].email }, "Posture-of-Success");
      res.cookie('jwt',token, { httpOnly: true, maxAge: 3600000 })
      res.json(token);
    }
  });
});

router.post('/signup', (req, res) => {
  var { username, email, password } = req.body;
  var sql = "INSERT INTO users (username, email, password) VALUES (?,?,?)";
  var params = [username, email, password];
  con.query(sql, params, (err, result) => {
    if (err) throw err;
  });
});



module.exports = router;
