var React = require('react');

var Hello = React.createClass({
  render: function() {
    return <div>Hello {this.props.name}</div>;
  }
});

// Trigger a runtime error
foo += 1;

module.exports = Hello;