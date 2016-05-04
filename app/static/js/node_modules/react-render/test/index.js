var path = require('path');
var assert = require('chai').assert;
var reactRender = require('..');
var Component = require('../lib/Component');

var Hello = path.join(__dirname, 'test_components', 'Hello.js');
var ErrorThrowingComponent = path.join(__dirname, 'test_components', 'ErrorThrowingComponent.js');

describe('reactRender', function() {
  beforeEach(function() {
    reactRender._components.clear();
  });
  it('is a function', function() {
    assert.isFunction(reactRender);
  });
  it('can render a component to static markup', function(done) {
    reactRender({
      path: Hello,
      toStaticMarkup: true,
      props: {
        name: 'World'
      }
    }, function(err, output) {
      assert.isNull(err);
      assert.equal(output, '<div>Hello World</div>');
      done();
    });
  });
  it('can render a component to a string', function(done) {
    reactRender({
      path: Hello,
      props: {
        name: 'World'
      }
    }, function(err, output) {
      assert.isNull(err);
      assert.include(output, '<div');
      assert.include(output, '><span');
      assert.include(output, '>Hello </span><span');
      assert.include(output, '>World</span>');
      assert.include(output, '</div>');
      done();
    });
  });
  it('can render a component without props', function(done) {
    reactRender({
      path: Hello,
      toStaticMarkup: true
    }, function(err, output) {
      assert.isNull(err);
      assert.equal(output, '<div>Hello </div>');
      done();
    });
  });
  it('can parse props which are provided in a JSON serialized form', function(done) {
    reactRender({
      path: Hello,
      toStaticMarkup: true,
      serializedProps: '{"name": "World"}'
    }, function(err, output) {
      assert.isNull(err);
      assert.equal(output, '<div>Hello World</div>');
      done();
    });
  });
  it('can require a component specified by a path and render it', function(done) {
    reactRender({
      path: path.join(__dirname, 'test_components', 'Hello'),
      toStaticMarkup: true,
      props: {
        name: 'World'
      }
    }, function(err, output) {
      assert.isNull(err);
      assert.equal(output, '<div>Hello World</div>');
      done();
    });
  });
  it('should return an error if neither `component` and `path` have been defined', function(done) {
    reactRender({
      toStaticMarkup: true,
      props: {
        name: 'World'
      }
    }, function(err, output) {
      assert.instanceOf(err, Error);
      assert.include(err.stack, 'Component missing `path` property');
      assert.isUndefined(output);
      done();
    });
  });
  it('should create `Component` instances when called', function(done) {
    assert.isArray(reactRender._components._cache);
    assert.equal(reactRender._components._cache.length, 0);

    reactRender({
      path: Hello
    }, function() {
      assert.equal(reactRender._components._cache.length, 1);
      assert.instanceOf(reactRender._components._cache[0], Component);
      assert.equal(reactRender._components._cache[0].component, require(Hello));
      done();
    });
  });
  it('should reuse Component instances when called', function() {
    assert.isArray(reactRender._components._cache);
    assert.equal(reactRender._components._cache.length, 0);

    reactRender({component: Hello}, function() {});
    assert.equal(reactRender._components._cache.length, 1);
    assert.instanceOf(reactRender._components._cache[0], Component);
    assert.equal(reactRender._components._cache[0].component, Hello);


    reactRender({path: 'foo'}, function() {});
    assert.equal(reactRender._components._cache.length, 2);
    assert.instanceOf(reactRender._components._cache[1], Component);
    assert.equal(reactRender._components._cache[1].opts.path, 'foo');

    reactRender({path: 'foo'}, function() {});
    assert.equal(reactRender._components._cache.length, 2);
    assert.instanceOf(reactRender._components._cache[1], Component);
    assert.equal(reactRender._components._cache[1].opts.path, 'foo');

    reactRender({path: 'foo', props: {bar: 1}}, function() {});
    assert.equal(reactRender._components._cache.length, 2);
    assert.instanceOf(reactRender._components._cache[1], Component);
    assert.equal(reactRender._components._cache[1].opts.path, 'foo');

    reactRender({path: 'bar', serializedProps: {bar: 1}}, function() {});
    assert.equal(reactRender._components._cache.length, 3);
    assert.instanceOf(reactRender._components._cache[2], Component);
    assert.equal(reactRender._components._cache[2].opts.path, 'bar');

    reactRender({path: 'foo', serializedProps: '{"bar": 1}'}, function() {});
    assert.equal(reactRender._components._cache.length, 3);
    assert.instanceOf(reactRender._components._cache[1], Component);
    assert.equal(reactRender._components._cache[1].opts.path, 'foo');

    reactRender({path: 'bar', serializedProps: '{"bar": 1}'}, function() {});
    assert.equal(reactRender._components._cache.length, 3);
    assert.instanceOf(reactRender._components._cache[2], Component);
    assert.equal(reactRender._components._cache[2].opts.path, 'bar');
  });
  it('passes up errors thrown during a component\'s rendering', function(done) {
    reactRender({
      path: ErrorThrowingComponent
    }, function(err, output) {
      assert.instanceOf(err, Error);
      assert.include(err.stack, 'Error from inside ErrorThrowingComponent');
      assert.include(err.stack, path.join(__dirname, 'test_components', 'ErrorThrowingComponent.js'));
      assert.isUndefined(output);
      done();
    });
  });
});