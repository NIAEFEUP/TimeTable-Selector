const express = require('express');
const path = require('path');
const logger = require('morgan');
const bodyParser = require('body-parser');

const apiRouter = require('./routes/api');
var programmeRouter = require('./routes/programme');

const app = express();

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Connect to Date Base
var config = require('config');
var dbConfig = config.get('dbConfig');

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

//Routers
app.use('/api', apiRouter);
app.use('/api/programme', programmeRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.json(err);
});

module.exports = app;
