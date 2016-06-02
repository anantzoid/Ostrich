const React = require('react');
const ReactDOM = require('react-dom');
window.renderApp = function(props) {
    const component = require('./src/components/'+store.component);
    const domContainerNode = document.getElementById('app-container');
    ReactDOM.unmountComponentAtNode(domContainerNode);
    ReactDOM.render(React.createFactory(component)(props), domContainerNode);
}
renderApp(store.props);
