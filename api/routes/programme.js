const express = require('express');
const router = express.Router();

router.get('/', function(req, res, next) {
  const programmes = ['FEUP-MIEIC', 'FEUP-MIEEC'];
  res.json(programmes);
});

module.exports = router;