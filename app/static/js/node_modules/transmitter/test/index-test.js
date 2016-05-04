import { assert } from 'chai'
import sinon from 'sinon'
import transmitter from '../'

export default {
  'functions exist'() {
    const bus = transmitter()
    assert.isFunction(bus.subscribe)
    assert.isFunction(bus.push)
    assert.isFunction(bus.unsubscribe)
  },

  'can listen and dispose'() {
    const bus = transmitter()
    const result = bus.subscribe(function () { })
    assert.isObject(result)
    assert.isFunction(result.dispose)
    const undef = result.dispose()
    assert.isUndefined(undef)
  },

  'pushing'() {
    const bus = transmitter()
    const spy = sinon.spy()

    const subscription = bus.subscribe(spy)

    bus.push('hello')

    assert.ok(spy.calledOnce)
    assert(spy.firstCall.args[0] === 'hello')

    subscription.dispose()
  },

  'unsub shortcut'() {
    const bus = transmitter()
    const spy = sinon.spy()
    bus.subscribe(spy)
    bus.unsubscribe(spy)

    bus.push(1)

    assert.notOk(spy.calledOnce)
    assert(spy.callCount === 0)
  },

  'unlisten dont exist'() {
    const bus = transmitter()
    bus.unsubscribe(function () { })
  },

  'unsubscribe while pushing'() {
    const bus = transmitter()
    const subscription = bus.subscribe(() => subscription.dispose())
    const spy = sinon.spy()
    bus.subscribe(spy)

    bus.push(1)

    assert(spy.calledOnce, 'spy was called once')
  },

  'unsubscribe and pushing while pushing'() {
    const spy1 = sinon.spy()

    const bus = transmitter()
    const subscription = bus.subscribe(() => {
      spy1()
      subscription.dispose()
    })

    const spy2 = sinon.spy()
    bus.subscribe(spy2)

    bus.subscribe(() => bus.push(2))

    assert.throws(() => bus.push(1), Error)

    assert(spy1.calledOnce, 'spy1 was called once')
    assert(spy2.calledOnce, 'spy2 was called once')
  },

  'errors on subscriptions'() {
    const bus = transmitter()

    const subscription = bus.subscribe(() => {
      subscription.dispose()
    })

    bus.subscribe(() => {
      throw new Error('oops')
    })

    assert(bus.subscriptions.length === 2)

    try {
      bus.push(1)
    } catch (err) {
      // ignore error on purpose
    } finally {
      assert(bus.subscriptions.length === 1)
    }
  },
}
