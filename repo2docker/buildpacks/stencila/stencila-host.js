const stencila = require("stencila-node");

// Get the port passed here from the `nbserverproxy.hanglers.SuperviseAndProxyHandler`
const port = parseInt(process.env.STENCILA_HOST_PORT || '2000')

// Run the Stencila execution host without
// any authentication (handled by Jupyter)
process.env.STENCILA_AUTH = 'false'

stencila.run({ port })
