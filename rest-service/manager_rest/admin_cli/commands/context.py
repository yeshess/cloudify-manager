import yaml

from manager_rest.storage import get_storage_manager, models
from manager_rest.flask_utils import setup_flask_app
from manager_rest.constants import PROVIDER_CONTEXT_ID

from .. import acfy


@acfy.group(name='context')
def context():
    setup_flask_app()


@context.command(name='get')
@acfy.options.with_manager_deployment
@acfy.pass_logger
def get_context(with_manager_deployment, logger):
    sm = get_storage_manager()
    ctx = sm.get(models.ProviderContext, PROVIDER_CONTEXT_ID)
    context = ctx.context
    if not with_manager_deployment:
        context['cloudify']['manager_deployment'] = '[omitted]'
    logger.info(yaml.dump(ctx.context))
