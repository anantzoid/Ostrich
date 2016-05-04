var React = require('react');

var ErrorThrowingComponent = React.createClass({
  render: function() {
    throw Error('Error from inside ErrorThrowingComponent');
  }
});

module.exports = ErrorThrowingComponent;