import pipes
import sys

from nbserverproxy.handlers import SuperviseAndProxyHandler

# define our proxy handler for proxying the application

class StencilaProxyHandler(SuperviseAndProxyHandler):

    name = 'stencila'

    def get_env(self):
        return {
            'STENCILA_PORT': str(self.port),
            'STENCILA_ARCHIVE_DIR': self.state['notebook_dir'],
            'BASE_URL': self.state['base_url'],
        }

    def get_cmd(self):
        return [
            'sh', '-c', 'cd "$STENCILA_DIR"; node stencila.js',
        ]


class StencilaHostProxyHandler(SuperviseAndProxyHandler):

    name = 'stencila-host'

    def get_env(self):
        return {
            'STENCILA_HOST_PORT': str(self.port)
        }

    def get_cmd(self):
        return [
            'sh', '-c', 'cd "$STENCILA_DIR"; node stencila-host.js',
        ]


def add_handlers(app):
    """Register the stencila proxy directory"""
    app.log.info("serving stencila at %s", app.base_url + 'stencila')
    app.web_app.add_handlers('.*', [
        (
            app.base_url + 'stencila/(.*)',
            StencilaProxyHandler,
            dict(state=dict(
                base_url=app.base_url,
                notebook_dir=app.notebook_dir,
            )),

        ), (
            app.base_url + 'stencila-host/(.*)',
            StencilaHostProxyHandler,
            dict(state=dict(
                base_url=app.base_url,
                notebook_dir=app.notebook_dir,
            )),
        ),
    ])


# fake a module to load the proxy handler as an extension
module_name = '_stencilaproxy'
import types
mod = types.ModuleType(module_name)
sys.modules[module_name] = mod
mod.load_jupyter_server_extension = add_handlers
c.NotebookApp.nbserver_extensions.update({
    module_name: True,
})
