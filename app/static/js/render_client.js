import React from 'react';

window.RenderClient = function(component, props) {
    //import Component from './components/'+component;
    const Component = require('./components/'+component);
    props = JSON.parse(props);
    console.log("herer");
    React.renderComponent(Component(props), 
            document.getElementById('app-container'));
}
