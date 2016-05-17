const React = require('react');
const ReactDOM = require('react-dom');
window.renderApp = function(props) {
    const component = require('./src/components/'+store.component);
    ReactDOM.render(React.createFactory(component)(props), document.getElementById('app-container'));
}
renderApp(JSON.parse(store.props));
