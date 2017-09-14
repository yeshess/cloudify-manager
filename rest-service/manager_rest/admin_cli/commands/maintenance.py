import os
import json
import time

from .. import acfy
from manager_rest import config, utils
from manager_rest.maintenance import (
    get_running_executions,
    prepare_maintenance_dict)
from manager_rest.flask_utils import setup_flask_app
from manager_rest.constants import (MAINTENANCE_MODE_ACTIVATED,
                                    MAINTENANCE_MODE_STATUS_FILE,
                                    MAINTENANCE_MODE_ACTIVATING)


@acfy.group(name='maintenance-mode')
def maintenance_mode():
    setup_flask_app()


@maintenance_mode.command(name='status',
                          short_help='Show current maintenance mode status')
@acfy.pass_logger
def status(logger):
    maintenance_file = os.path.join(
        config.instance.maintenance_folder,
        MAINTENANCE_MODE_STATUS_FILE)
    if os.path.isfile(maintenance_file):
        with open(maintenance_file) as f:
            data = json.load(f)
        labels = {
            MAINTENANCE_MODE_ACTIVATING: 'activating',
            MAINTENANCE_MODE_ACTIVATED: 'enabled'
        }
        state = labels.get(data['status'], 'status unknown')
    else:
        state = 'disabled'
    logger.info('Maintenance mode is {0}'.format(state))


@maintenance_mode.command(name='enable', short_help='Enables maintenance mode')
@acfy.pass_logger
def enable(logger):
    maintenance_file = os.path.join(
        config.instance.maintenance_folder,
        MAINTENANCE_MODE_STATUS_FILE)
    execs = get_running_executions()
    requested_timestamp = utils.get_formatted_timestamp()
    while execs:
        logger.info('Waiting for {0} executions to finish...'
                    .format(len(execs)))
        status = prepare_maintenance_dict(
            MAINTENANCE_MODE_ACTIVATING,
            activated_at='',
            remaining_executions=execs,
            requested_by='Admin CLI',
            activation_requested_at=requested_timestamp)
        with open(maintenance_file, 'w') as f:
            json.dump(status, f)
        time.sleep(3)
    status = prepare_maintenance_dict(
        MAINTENANCE_MODE_ACTIVATED,
        activated_at=utils.get_formatted_timestamp(),
        requested_by='Admin CLI',
        activation_requested_at=requested_timestamp)
    with open(maintenance_file, 'w') as f:
        json.dump(status, f)

    # should probably be just owned by cfyuser?
    os.chmod(maintenance_file, 0666)
    logger.info('Maintenance mode enabled')


@maintenance_mode.command(name='disable',
                          short_help='Enables maintenance mode')
@acfy.pass_logger
def disable(logger):
    maintenance_file = os.path.join(
        config.instance.maintenance_folder,
        MAINTENANCE_MODE_STATUS_FILE)
    try:
        os.unlink(maintenance_file)
    except OSError:
        logger.info('Maintenance mode is already disabled')
    else:
        logger.info('Maintenance mode disabled')
