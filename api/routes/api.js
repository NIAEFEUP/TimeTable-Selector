var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next) {
  res.json('TTS API Home');
});

router.get('/programme', function(req, res, next) {
  const programmes = ['FEUP-MIEIC', 'FEUP-MIEEC'];
  res.json(programmes);
})

router.get('/schedule-data', function(req, res, next) {
  res.sendfile('./testdata.json');
});

module.exports = router;
