function transmitter() {
  const subscriptions = []
  let pushing = false
  let toUnsubscribe = []

  const unsubscribe = (onChange) => {
    if (pushing) {
      toUnsubscribe.push(onChange)
      return
    }
    const id = subscriptions.indexOf(onChange)
    if (id >= 0) subscriptions.splice(id, 1)
  }

  const subscribe = (onChange) => {
    subscriptions.push(onChange)
    const dispose = () => unsubscribe(onChange)
    return { dispose }
  }

  const push = (value) => {
    pushing = true
    try {
      subscriptions.forEach(subscription => subscription(value))
    } finally {
      pushing = false
      toUnsubscribe = toUnsubscribe.filter(unsubscribe)
    }
  }

  return { subscribe, push, unsubscribe, subscriptions }
}

module.exports = transmitter
