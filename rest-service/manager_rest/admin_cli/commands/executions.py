from .. import acfy
from manager_rest.flask_utils import setup_flask_app
from manager_rest.storage import get_storage_manager, models


@acfy.group(name='executions')
def executions():
    setup_flask_app()


@executions.command(name='force-remove')
@acfy.options.execution_id
@acfy.pass_logger
def force_remove(execution_id, logger):
    sm = get_storage_manager()
    execution = models.Execution.query\
        .filter(models.Execution.id == execution_id).one()
    sm.delete(execution)
    logger.info('Execution {0} removed'.format(execution_id))
