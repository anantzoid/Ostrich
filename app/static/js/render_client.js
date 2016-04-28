var React = require('react');
import ReactDOM from 'react-dom';
//import Component from './components/'+component;
//var homepage = React.createFactory(require('./components/home.jsx'));
import homepage from './components/home.jsx'; 
ReactDOM.render(<homepage user={window.props.user} collections={window.props.collections} />, 
        document.getElementById('app-container'));
