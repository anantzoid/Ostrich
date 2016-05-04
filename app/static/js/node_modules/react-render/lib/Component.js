var React = require('react');
var ReactDOMServer = require('react-dom/server');

var Component = function Component(opts) {
  this.opts = opts;
  this.path = null;
  this.component = null;
  this.factory = null;
};

Component.prototype.getPath = function getPath(cb) {
  if (this.path) {
    return cb(null, this.path);
  }
  if (!this.opts.path) {
    return cb(new Error('Component missing `path` property'));
  }
  this.path = this.opts.path;
  cb(null, this.path);
};

Component.prototype.getComponent = function getComponent(cb) {
  if (this.component) {
    return cb(null, this.component);
  }

  if (this.opts.component) {
    this.component = this.opts.component;
    return cb(null, this.component);
  }

  this.getPath(function(err, path) {
    if (err) return cb(err);

    if (!path) {
      return cb(new Error('Component options missing `path` and `component` properties'));
    }

    try {
      this.component = require(this.path);
      if (this.component && typeof this.component === 'object' && this.component.default) {
        this.component = this.component.default
      }
    } catch(err) {
      return cb(err);
    }

    cb(null, this.component);
  }.bind(this));
};

Component.prototype.getFactory = function getFactory(cb) {
  if (this.factory) {
    return cb(null, this.factory);
  }

  this.getComponent(function(err, component) {
    if (err) return cb(err);

    try {
      this.factory = React.createFactory(component);
    } catch(err) {
      cb(err);
    }

    cb(null, this.factory);
  }.bind(this));
};

Component.prototype._render = function _render(props, toStaticMarkup, cb) {
  this.getFactory(function(err, factory) {
    if (err) return cb(err);

    var render = (
      toStaticMarkup
        ? ReactDOMServer.renderToStaticMarkup
        : ReactDOMServer.renderToString
    ).bind(ReactDOMServer);

    try {
      var markup = render(factory(props));
    } catch (err) {
      return cb(err);
    }

    cb(null, markup);
  }.bind(this));
};

Component.prototype.renderToString = function renderToString(props, cb) {
  this._render(props, false, cb);
};

Component.prototype.renderToStaticMarkup = function renderToStaticMarkup(props, cb) {
  this._render(props, true, cb);
};

module.exports = Component;
