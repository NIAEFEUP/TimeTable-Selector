var express = require('express');
var router = express.Router();

var config = require('config');
var dbConfig = config.get('dbConfig');
console.log(dbConfig);

var mysql = require('mysql');
var connection = mysql.createConnection({
  host     : dbConfig.host,
  user     : dbConfig.username,
  password : dbConfig.password,
  database : dbConfig.dbName
});

connection.connect(function(err) {
  if (err) {
    console.error('error connecting: ' + err.stack);
    return;
  }

  console.log('connected as id ' + connection.threadId);
});

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
