from .. import acfy
from manager_rest.storage_manager import get_storage_manager, models
from manager_rest.constants import PROVIDER_CONTEXT_ID


@acfy.group(name='context')
def context():
    pass


@context.command(name='get')
@acfy.pass_logger
def get_context(logger):
    sm = get_storage_manager()
    ctx = sm.get(models.ProviderContext, PROVIDER_CONTEXT_ID)
    logger.info(ctx.context)
