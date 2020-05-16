var express = require('express');
var router = express.Router();

router.post('/login', function(req, res, next) {
  var valid = false;
  if (req.body.email == "cdltlehf@naver.com") valid = true;
  res.json({...req.body, valid});
});

module.exports = router;
