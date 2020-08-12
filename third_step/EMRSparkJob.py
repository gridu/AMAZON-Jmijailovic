import boto3

connection = boto3.client(
    'emr',
    region_name='us-east-2',
    aws_access_key_id='',
    aws_secret_access_key=''
)

cluster_id = connection.run_job_flow(
    Name='spark-fraudulent-ips',
    LogUri='s3://jmijailovic-item-logs/logs',
    ReleaseLabel='emr-5.30.0',
    Applications=[
        {
            'Name': 'Spark'
        },
    ],
    Instances={
        'InstanceGroups': [
            {
                'Name': "Master nodes",
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 1,
            },
            {
                'Name': "Slave nodes",
                'Market': 'ON_DEMAND',
                'InstanceRole': 'CORE',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 2,
            }
        ],
        'Ec2KeyName': 'mijailovicBigData',
        'KeepJobFlowAliveWhenNoSteps': True,
        'TerminationProtected': False,
        'Ec2SubnetId': 'subnet-5bc54c17',
    },
    Steps=[
        {
            'Name': 'pip-step',
            'ActionOnFailure': 'CANCEL_AND_WAIT',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['sudo', 'pip3', 'install', 'boto3']
            }
        },
        {
            'Name': 'fraudulent-ip-step',
            'ActionOnFailure': 'CANCEL_AND_WAIT',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['spark-submit', '--packages com.audienceproject:spark-dynamodb_2.11:1.0.3',
                         's3://jmijailovic-item-logs/IdentifyFraudIpsSpark.py']
            }
        }
    ],
    VisibleToAllUsers=True,
    JobFlowRole='EMR_EC2_DefaultRole',
    ServiceRole='EMR_DefaultRole'
)

print('cluster created with the step...', cluster_id['JobFlowId'])
