# transmitter

> Dead simple pub-sub

It's 35 LOC of just subscribe and push.

## API

### subscribe(onChange: function): { dispose: (): void }

Subscribes to change events. Returns an object which contains the method `dispose` which removes the current subscription.

### push(payload: any): void

Emit a change to all the subscribers.

## Example

```js
const bus = transmitter()

bus.subscribe(result => console.log(result))

bus.push({ foo: 'bar' })
```

## License

[MIT](http://josh.mit-license.org)
