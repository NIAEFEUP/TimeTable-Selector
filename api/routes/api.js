var express = require('express');
var router = express.Router();


router.get('/', function(req, res, next) {
  res.json('TTS API Home');
});

module.exports = router;
