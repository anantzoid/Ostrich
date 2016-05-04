const React = require('react');
const ReactDOM = require('react-dom');
const component = require('./src/components/'+store.component);
ReactDOM.render(React.createFactory(component)(JSON.parse(store.props)), document.getElementById('app-container'));
