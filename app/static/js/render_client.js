const React = require('react');
const ReactDOM = require('react-dom');
const component = require('./components/'+store.component);
ReactDOM.render(React.createFactory(component)(store.props), document.getElementById('app-container'));
