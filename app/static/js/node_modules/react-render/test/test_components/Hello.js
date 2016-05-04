var React = require('react');

var Hello = React.createClass({
  render: function() {
    return React.createElement("div", null, "Hello ", this.props.name);
  }
});

module.exports = Hello;