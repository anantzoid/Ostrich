'use strict';

function transmitter() {
  var subscriptions = [];
  var pushing = false;
  var toUnsubscribe = [];

  var unsubscribe = function unsubscribe(onChange) {
    if (pushing) {
      toUnsubscribe.push(onChange);
      return;
    }
    var id = subscriptions.indexOf(onChange);
    if (id >= 0) subscriptions.splice(id, 1);
  };

  var subscribe = function subscribe(onChange) {
    subscriptions.push(onChange);
    var dispose = function dispose() {
      return unsubscribe(onChange);
    };
    return { dispose: dispose };
  };

  var push = function push(value) {
    if (pushing) throw new Error('Cannot push while pushing');
    pushing = true;
    try {
      subscriptions.forEach(function (subscription) {
        return subscription(value);
      });
    } finally {
      pushing = false;
      toUnsubscribe = toUnsubscribe.filter(unsubscribe);
    }
  };

  return { subscribe: subscribe, push: push, unsubscribe: unsubscribe, subscriptions: subscriptions };
}

module.exports = transmitter;

