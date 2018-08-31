# Copyright (c) 2014 Scopely, Inc.
# Copyright (c) 2015 Mitch Garnaat
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

from skew.resources.aws import AWSResource

import logging

LOG = logging.getLogger(__name__)

class LoadBalancer(AWSResource):

    class Meta(object):
        service = 'elb'
        type = 'loadbalancer'
        enum_spec = ('describe_load_balancers',
                     'LoadBalancerDescriptions', None)
        detail_spec = None
        id = 'LoadBalancerName'
        filter_name = 'LoadBalancerNames'
        filter_type = 'list'
        name = 'DNSName'
        date = 'CreatedTime'
        dimension = 'LoadBalancerName'
        tags_spec = ('describe_tags', 'TagDescriptions[].Tags[]',
                     'LoadBalancerNames', 'id')

class LoadBalancerV2(AWSResource):

    class Meta(object):
        service = 'elbv2'
        type = 'loadbalancer'
        enum_spec = ('describe_load_balancers',
                     'LoadBalancers', None)
        detail_spec = None
        id = 'LoadBalancerArn'
        filter_name = 'LoadBalancerArns'
        filter_type = 'list'
        name = 'DNSName'
        date = 'CreatedTime'
        dimension = 'LoadBalancerArn'
        tags_spec = ('describe_tags', 'TagDescriptions[].Tags[]',
                     'ResourceArns', 'id')

    # @classmethod
    # def enumerate(cls, session_factory, arn, resource_id=None):
    #     LOG.warn('enumerate arn=%r, resource_id=%r' % (arn, resource_id))

    #     resources = super(LoadBalancerV2, cls).enumerate(
    #         session_factory, arn, resource_id)

    #     return resources

    @property
    def arn(self):
        # LOG.warn('arn: id=%r' % (self.id))
        return '%s' % (self.id)