# Copyright (c) 2018 Ludovic LANGE
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import jmespath
import logging

from skew.resources.aws import AWSResource

LOG = logging.getLogger(__name__)


class Vault(AWSResource):

    class Meta(object):
        service = 'glacier'
        type = 'vault'
        enum_spec = ('list_vaults', 'VaultList[]', None)
        id = 'VaultName'
        filter_name = 'marker'
        filter_type = 'string'
        detail_spec = None
        name = 'VaultName'
        date = 'CreationDate'
        dimension = None
        tags_spec = ('list_tags_for_vault', 'Tags',
                     'vaultName', 'id')

    @property
    def arn(self):
        return self._data['VaultARN']