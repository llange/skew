# Copyright 2015 Mitch Garnaat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import time

import datetime
import jmespath
import boto3
import warnings
from botocore.exceptions import ClientError

from skew.config import get_config

LOG = logging.getLogger(__name__)


def json_encoder(obj):
    """JSON encoder that formats datetimes as ISO8601 format."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj


class AWSClient(object):

    _cached_credentials = {}
    _cached_identity = {}
    _cached_alias = {}

    @property
    def cached_credentials(self):
        return self._cached_credentials

    @cached_credentials.setter
    def cached_credentials(self, val):
        self._cached_credentials = val

    @property
    def cached_identity(self):
        return self._cached_identity

    @cached_identity.setter
    def cached_identity(self, val):
        self._cached_identity = val

    @property
    def cached_alias(self):
        return self._cached_alias

    @cached_alias.setter
    def cached_alias(self, val):
        self._cached_alias = val

    @property
    def account_name(self):
        return self._cached_alias.get(self._account_id)

    def __init__(self, service_name, region_name, account_id, **kwargs):
        self._config = get_config()
        self._service_name = service_name
        self._region_name = region_name
        self._account_id = account_id
        self._has_credentials = False
        self.aws_creds = kwargs.get('aws_creds')
        if self.aws_creds is None:
            # no aws_creds, need profile to get creds from ~/.aws/credentials
            self._profile = self._config['accounts'][account_id]['profile']
        self.placebo = kwargs.get('placebo')
        self.placebo_dir = kwargs.get('placebo_dir')
        self.placebo_mode = kwargs.get('placebo_mode', 'record')
        self._client = self._create_client()

    @property
    def service_name(self):
        return self._service_name

    @property
    def region_name(self):
        return self._region_name

    @property
    def account_id(self):
        return self._account_id

    @property
    def profile(self):
        return self._profile

    def _create_client(self):
        if self.aws_creds:
            session = boto3.Session(**self.aws_creds)
        else:
            session = boto3.Session(
                profile_name=self.profile)
        if self.placebo and self.placebo_dir:
            pill = self.placebo.attach(session, self.placebo_dir)
            if self.placebo_mode == 'record':
                pill.record()
            elif self.placebo_mode == 'playback':
                pill.playback()

        if (self.account_id not in self.cached_identity):
            sts_client = session.client('sts')
            LOG.debug("sts_client:%s" % (sts_client))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                identity = sts_client.get_caller_identity()
            LOG.debug("identity:%s" % (identity))
            self.cached_identity[self.account_id] = {}
            self.cached_identity[self.account_id]['UserId'] = identity.get('UserId')
            self.cached_identity[self.account_id]['Account'] = identity.get('Account')
            self.cached_identity[self.account_id]['Arn'] = identity.get('Arn')
            LOG.debug("Region:%s Account:%s Identity:%s" % (self._region_name, self.account_id, self.cached_identity[self.account_id]))
        else:
            LOG.debug("Region:%s Account:%s Identity from cache:%s" % (self._region_name, self.account_id, self.cached_identity[self.account_id]))
        # self._identity_userid = self.cached_identity.get('UserId')
        # self._identity_account = self.cached_identity.get('Account')
        # self._identity_arn = self.cached_identity.get('Arn')

        if (self.account_id not in self.cached_alias):
            iam_client = session.client('iam')
            LOG.debug("iam_client:%s" % (iam_client))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                accountaliases = iam_client.list_account_aliases()
            LOG.debug("Aliases:%s" % (accountaliases))
            if len(accountaliases.get('AccountAliases', [])) > 0:
                accountalias = "%s (%s)" % (self.cached_identity.get(self.account_id, {}).get('Account'), accountaliases.get('AccountAliases')[0])
            else:
                accountalias = "%s" % (self.cached_identity.get(self.account_id, {}).get('Account'))
            self.cached_alias[self.account_id] = accountalias
            LOG.debug("Region:%s Account:%s Stored account alias:%s" % (self._region_name, self.account_id, self.cached_alias[self.account_id]))
        else:
            LOG.debug("Region:%s Account:%s Cached account alias:%s" % (self._region_name, self.account_id, self.cached_alias[self.account_id]))

        return session.client(
            self.service_name,
            region_name=self.region_name if self.region_name else None)

    def call(self, op_name, query=None, **kwargs):
        """
        Make a request to a method in this client.  The response data is
        returned from this call as native Python data structures.

        This method differs from just calling the client method directly
        in the following ways:

          * It automatically handles the pagination rather than
            relying on a separate pagination method call.
          * You can pass an optional jmespath query and this query
            will be applied to the data returned from the low-level
            call.  This allows you to tailor the returned data to be
            exactly what you want.

        :type op_name: str
        :param op_name: The name of the request you wish to make.

        :type query: str
        :param query: A jmespath query that will be applied to the
            data returned by the operation prior to returning
            it to the user.

        :type kwargs: keyword arguments
        :param kwargs: Additional keyword arguments you want to pass
            to the method when making the request.
        """
        LOG.debug(kwargs)
        if query:
            query = jmespath.compile(query)
        if self._client.can_paginate(op_name):
            paginator = self._client.get_paginator(op_name)
            results = paginator.paginate(**kwargs)
            data = results.build_full_result()
        else:
            op = getattr(self._client, op_name)
            done = False
            data = {}
            while not done:
                try:
                    data = op(**kwargs)
                    done = True
                except ClientError as e:
                    LOG.debug(e, kwargs)
                    if 'Throttling' in str(e):
                        time.sleep(1)
                    elif 'AccessDenied' in str(e):
                        done = True
                    elif 'NoSuchTagSet' in str(e):
                        done = True
                except Exception:
                    done = True
        if query:
            data = query.search(data)
        return data


def get_awsclient(service_name, region_name, account_id, **kwargs):
    if region_name == '':
        region_name = None
    return AWSClient(service_name, region_name, account_id, **kwargs)


class SkewSessionFactory(object):

    def __init__(self, region, account, **kwargs):
        self.region_name = region
        self.account = account
        self.kwargs = kwargs

    def get_client(self, service_name):
        return AWSClient(service_name, self.region_name, self.account, **self.kwargs)
