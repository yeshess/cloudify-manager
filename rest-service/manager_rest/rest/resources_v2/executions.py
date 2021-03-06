#########
# Copyright (c) 2017 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#

from flask import request
from flask_restful_swagger import swagger

from manager_rest import manager_exceptions
from manager_rest.resource_manager import get_resource_manager
from manager_rest.rest import (
    resources_v1,
    rest_decorators,
    rest_utils,
)
from manager_rest.storage import (
    get_storage_manager,
    models,
)
from manager_rest.security.authorization import authorize
from manager_rest.utils import create_filter_params_list_description


class Executions(resources_v1.Executions):
    @swagger.operation(
        responseClass='List[{0}]'.format(models.Execution.__name__),
        nickname="list",
        notes='Returns a list of executions for the optionally provided filter'
              ' parameters: {0}'.format(models.Execution),
        parameters=create_filter_params_list_description(
            models.Execution.response_fields, 'executions') + [
            {'name': '_include_system_workflows',
             'description': 'Include executions of system workflows',
             'required': False,
             'allowMultiple': True,
             'dataType': 'bool',
             'defaultValue': False,
             'paramType': 'query'}
        ]
    )
    @rest_decorators.exceptions_handled
    @authorize('execution_list', allow_all_tenants=True)
    @rest_decorators.marshal_with(models.Execution)
    @rest_decorators.create_filters(models.Execution)
    @rest_decorators.paginate
    @rest_decorators.sortable(models.Execution)
    @rest_decorators.all_tenants
    def get(self, _include=None, filters=None, pagination=None,
            sort=None, all_tenants=None, **kwargs):
        """
        List executions
        """
        deployment_id = request.args.get('deployment_id')
        if deployment_id:
            self._check_if_deployment_exists(deployment_id, all_tenants)
        is_include_system_workflows = rest_utils.verify_and_convert_bool(
            '_include_system_workflows',
            request.args.get('_include_system_workflows', 'false'))

        return get_resource_manager().list_executions(
            filters=filters,
            pagination=pagination,
            sort=sort,
            is_include_system_workflows=is_include_system_workflows,
            include=_include,
            all_tenants=all_tenants
        )

    def _check_if_deployment_exists(self, deployment_id, all_tenants):
        deployments_list = get_storage_manager().list(
            models.Deployment,
            include=['id'],
            filters={'id': deployment_id},
            all_tenants=all_tenants
        )
        if not deployments_list:
            raise manager_exceptions.NotFoundError(
                'Requested `Deployment` with ID `{0}` was not found'
                .format(deployment_id)
            )
