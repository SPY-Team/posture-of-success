var express = require('express');
var jwt = require('jsonwebtoken');

var router = express.Router();

var users = [
  "admin@posture.success",
  "first@posture.success",
  "second@posture.success",
  "guest@posture.success"
];

var data = [
  [ 1, 2, 3, 4 ], 
  [ 4, 3, 2, 1 ],
  [ 9, 8, 7, 6 ],
  [ 0, 0, 0, 0 ],
];

router.post('/data', function(req, res, next) {
  var { token } = req.body;
  var { uid } = jwt.verify(token, "Posture-of-Success");
  if (data[uid]) {
    res.json({ email: users[uid], data: data[uid] });
  } else {
    res.status(403).json({message: "Rejected!"});
  }
}) 

router.post('/login', function(req, res, next) {
  var valid = false;
  var { email, password } = req.body;

  if (users.indexOf(email) != -1) {
    let token = jwt.sign({ uid: users.indexOf(email) }, "Posture-of-Success");
    res.cookie('jwt',token, { httpOnly: true, maxAge: 3600000 })
    res.json(token);
  } else {
    //res.status(403).json({message: "Rejected!"});
    let token = jwt.sign({ uid: 3 }, "Posture-of-Success");
    res.cookie('jwt',token, { httpOnly: true, maxAge: 3600000 })
    res.json(token);
  }
});

module.exports = router;
