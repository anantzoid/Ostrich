var http = require('http');
var express = require('express');
var bodyParser = require('body-parser');
var reactRender = require('react-render');
// Ensure support for loading files that contain ES6+7 & JSX
require('babel-core/register');
var React = require('react');
var ReactDOM = require('react-dom');

var app = express();
var server = http.Server(app);
app.use(bodyParser.json());

app.get('/', function(req, res) {
    res.end('React render server');
});

app.get('/render', function(req, res) {
   
    var component = React.createFactory(require('/Users/jedi/ostrich/backend/app/static/js/components/searchbar.js'));
    console.log(component);
    res.send(React.renderToString(component()));
    /*
    reactRender(req.body, function(err, markup) {
        if (err) {
            res.json({
                error: {
                    type: err.constructor.name,
                    message: err.message,
                    stack: err.stack
                },
                markup: null
            });
        } else {
            res.json({
                error: null,
                markup: markup
            });
        }
    });
    */
});

var ADDRESS = process.env.PORT || '127.0.0.1';
var PORT = process.env.PORT || 9009;
server.listen(PORT, ADDRESS, function() {
    console.log('React render server listening at http://' + ADDRESS + ':' + PORT);
});
