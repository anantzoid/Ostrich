var React = require('react');
var Hello = require('./Hello.jsx');

var HelloWrapper = React.createClass({
  render: function () {
    var numbers = this.props.numbers.map(function (number) {
      return number * 10;
    }).join(', ');
    return (
      <div>
        <Hello name={this.props.name} />
        <span>{numbers}</span>
      </div>
    );
  }
});

module.exports = HelloWrapper;