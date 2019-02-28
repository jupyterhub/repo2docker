import os
csp = os.environ.get(
    'CSP_HOSTS', ''
)
c.NotebookApp.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors {} 'self' ".format(csp.replace('"', ''))
    }
}
