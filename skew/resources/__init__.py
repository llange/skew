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

import importlib

# Maps resources names as they appear in ARN's to the path name
# of the Python class representing that resource.
# Cf http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces
ResourceTypes = {
    # Alexa for Business  a4b
    'aws.apigateway.restapis': 'aws.apigateway.RestAPI',
    # - execute-api
    # AWS Application Discovery Service   discovery
    #appstream
    # AWS AppSync     appsync
    #artifact
    # Amazon Athena   athena
    'aws.autoscaling.autoScalingGroup': 'aws.autoscaling.AutoScalingGroup',
    'aws.autoscaling.launchConfigurationName': 'aws.autoscaling.LaunchConfiguration',
    # AWS Batch   batch
    # AWS Billing and Cost Management     aws-portal
    # AWS Budgets     budgets
    # AWS Certificate Manager (ACM)   acm
    # Amazon Chime    chime
    # AWS Cloud9  cloud9
    # Amazon Cloud Directory  clouddirectory
    'aws.cloudformation.stack': 'aws.cloudformation.Stack',
    'aws.cloudfront.distribution': 'aws.cloudfront.Distribution',
    #cloudhsm
    #cloudsearch # TODO - used
    # TODO - used : cloudsearch domain
    #cloudtrail
    'aws.cloudwatch.alarm': 'aws.cloudwatch.Alarm',
    #events
    #logs # TODO - used
    # TODO - used : logs log-group
    #codebuild
    #codecommit
    #codedeploy
    #codepipeline
    #codestar
    #cognito-idp
    #cognito-identity
    #cognito-sync
    # Amazon Comprehend   comprehend
    #config
    # Amazon Connect  connect
    #datapipeline # TODO - used
    # TODO - used : datapipeline pipeline
    #dms # TODO - used
    # TODO - used : dms rep
    #devicefarm
    #directconnect
    #ds # TODO - used
    # TODO - used : ds directory
    'aws.dynamodb.table': 'aws.dynamodb.Table', # TODO - used
    'aws.ec2.address': 'aws.ec2.Address',
    'aws.ec2.customer-gateway': 'aws.ec2.CustomerGateway',
    'aws.ec2.key-pair': 'aws.ec2.KeyPair',
    'aws.ec2.image': 'aws.ec2.Image',
    'aws.ec2.instance': 'aws.ec2.Instance',
    'aws.ec2.natgateway': 'aws.ec2.NatGateway',
    'aws.ec2.network-acl': 'aws.ec2.NetworkAcl',
    'aws.ec2.route-table': 'aws.ec2.RouteTable',
    'aws.ec2.security-group': 'aws.ec2.SecurityGroup',
    'aws.ec2.snapshot': 'aws.ec2.Snapshot',
    'aws.ec2.volume': 'aws.ec2.Volume',
    'aws.ec2.vpc': 'aws.ec2.Vpc',
    'aws.ec2.vpc-peering-connection': 'aws.ec2.VpcPeeringConnection',
    'aws.ec2.subnet': 'aws.ec2.Subnet',
    #ecr # TODO - used
    # TODO - used : ecr repository
    #ecs
    # Amazon Elastic Container Service for Kubernetes (Amazon EKS)    eks
    #ssm
    'aws.elasticbeanstalk.application': 'aws.elasticbeanstalk.Application',
    'aws.elasticbeanstalk.environment': 'aws.elasticbeanstalk.Environment',
    #elasticfilesystem # TODO - used
    # TODO - used : elasticfilesystem file-system
    #elasticloadbalancing != elb ??? # TODO - used
    # TODO - used : elasticloadbalancing loadbalancer
    # Ex: (ALB) arn:aws:elasticloadbalancing:eu-west-1:130536754160:loadbalancer/app/reportv3alb/920cc2fd6817052a
    'aws.elb.loadbalancer': 'aws.elb.LoadBalancer',
    #elasticmapreduce
    #elastictranscoder
    'aws.elasticache.cluster': 'aws.elasticache.Cluster',
    'aws.elasticache.subnet-group': 'aws.elasticache.SubnetGroup',
    'aws.elasticache.snapshot': 'aws.elasticache.Snapshot',
    'aws.es.domain': 'aws.es.ElasticsearchDomain', # TODO - used
    # AWS Firewall Manager    fms
    # Amazon FreeRTOS     freertos
    #gamelift
    #glacier
    # AWS Glue    glue
    # AWS Greengrass  greengrass
    # Amazon GuardDuty    guardduty
    #health
    'aws.iam.group': 'aws.iam.Group',
    'aws.iam.instance-profile': 'aws.iam.InstanceProfile',
    'aws.iam.role': 'aws.iam.Role',
    'aws.iam.policy': 'aws.iam.Policy',
    'aws.iam.user': 'aws.iam.User',
    'aws.iam.server-certificate': 'aws.iam.ServerCertificate',
    #importexport
    #inspector
    #iot
    #kms # TODO - used
    # TODO - used : kms key
    #kinesisanalytics
    'aws.firehose.deliverystream': 'aws.firehose.DeliveryStream',
    'aws.kinesis.stream': 'aws.kinesis.Stream', # TODO - used
    # Amazon Kinesis Video Streams    kinesisvideo
    'aws.lambda.function': 'aws.lambda.Function', # TODO - used
    # Amazon Lex  lex
    #lightsail
    # Amazon Macie    macie
    #machinelearning
    #aws-marketplace
    #aws-marketplace-management
    # AWS Elemental MediaConvert  mediaconvert
    # AWS Elemental MediaLive     medialive
    # AWS Elemental MediaPackage  mediapackage
    # AWS Elemental MediaStore    mediastore
    # AWS Elemental MediaTailor   mediatailor
    # AWS Migration Hub   mgh
    #mobileanalytics
    #mobilehub
    # Amazon MQ   mq
    #opsworks
    #opsworks-cm
    #organizations
    # Amazon Pinpoint     mobiletargeting
    #polly
    # Amazon QuickSight   quicksight
    'aws.redshift.cluster': 'aws.redshift.Cluster',
    # Amazon Rekognition  rekognition
    'aws.rds.db': 'aws.rds.DBInstance', # TODO - used
    # TODO - used : rds cluster
    'aws.rds.secgrp': 'aws.rds.DBSecurityGroup',
    # AWS Resource Groups     resource-groups
    'aws.route53.hostedzone': 'aws.route53.HostedZone', # TODO - used
    'aws.route53.healthcheck': 'aws.route53.HealthCheck',
    # Amazon Route 53 Auto Naming     servicediscovery
    # Amazon Route 53 Domains     route53domains
    # Amazon SageMaker    sagemaker
    # AWS Secrets Manager     secretsmanager
    #sts
    # AWS Serverless Application Repository   serverlessrepo
    #servicecatalog
    # AWS Shield  shield
    # AWS Shield Advanced     DDoSProtection
    #ses
    'aws.sns.subscription': 'aws.sns.Subscription',
    'aws.sns.topic': 'aws.sns.Topic',
    'aws.sqs.queue': 'aws.sqs.Queue',
    'aws.s3.bucket': 'aws.s3.Bucket'
    #swf
    #sdb
    #states
    #storagegateway
    # Amazon Sumerian     sumerian
    #support
    # Amazon Transcribe   transcribe
    # Amazon Translate    translate
    #trustedadvisor
    #waf # TODO - used
    # - waf-regional
    # TODO - used : waf-regional rule
    # TODO - used : waf-regional webacl
    # TODO - used : waf rule
    # TODO - used : waf webacl
    #workdocs
    #workmail
    #workspaces
    # AWS X-Ray   xray
}


def all_providers():
    providers = set()
    for resource_type in ResourceTypes:
        providers.add(resource_type.split('.')[0])
    return list(providers)


def all_services(provider_name):
    services = set()
    for resource_type in ResourceTypes:
        t = resource_type.split('.')
        if t[0] == provider_name:
            services.add(t[1])
    return list(services)


def all_types(provider_name, service_name):
    types = set()
    for resource_type in ResourceTypes:
        t = resource_type.split('.')
        if t[0] == provider_name and t[1] == service_name:
            types.add(t[2])
    return list(types)


def find_resource_class(resource_path):
    """
    dynamically load a class from a string
    """
    class_path = ResourceTypes[resource_path]
    # First prepend our __name__ to the resource string passed in.
    full_path = '.'.join([__name__, class_path])
    class_data = full_path.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]
    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)
