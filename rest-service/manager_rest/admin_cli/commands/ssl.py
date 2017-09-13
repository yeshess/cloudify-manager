from .. import acfy
from manager_rest.rest.resources_v3_1.manager import (
    SSLConfig,
    DEFAULT_CONF_PATH,
    HTTP_PATH,
    HTTPS_PATH)


@acfy.group(name='ssl')
def ssl():
    pass


@ssl.command(name='status')
@acfy.pass_logger
def ssl_status(logger):
    return 'SSL {0}'.format(
        'enabled' if SSLConfig._is_enabled() else 'disabled')
