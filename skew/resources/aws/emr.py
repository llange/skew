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
import datetime

LOG = logging.getLogger(__name__)


class Cluster(AWSResource):

    class Meta(object):
        service = 'emr'
        type = 'cluster'
        enum_spec = None
        # enum_spec = ('list_clusters', 'Clusters[]', {'ClusterStates': ['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING', 'TERMINATING']})
        id = 'Id'
        detail_spec = None
        name = 'Name'
        date = 'Status.Timeline.CreationDate'
        dimension = None
        tags_spec = ('describe_cluster', 'Cluster.Tags[]',
                     'ClusterId', 'id')

    @classmethod
    def enumerate(cls, session_factory, arn, resource_id=None):
        # Let's fetch all TERMINATED cluster - created at max 3 days ago
        cls.Meta.enum_spec = ('list_clusters', 'Clusters[]', {'ClusterStates': ['TERMINATED', 'TERMINATED_WITH_ERRORS'], 'CreatedAfter': (datetime.datetime.now() + datetime.timedelta(-3))})
        resources_inactive = super(Cluster, cls).enumerate(
            session_factory, arn, resource_id)

        # Let's fetch all RUNNING cluster - no time limit
        cls.Meta.enum_spec = ('list_clusters', 'Clusters[]', {'ClusterStates': ['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING', 'TERMINATING']})
        resources_active = super(Cluster, cls).enumerate(
            session_factory, arn, resource_id)

        return resources_active + resources_inactive
