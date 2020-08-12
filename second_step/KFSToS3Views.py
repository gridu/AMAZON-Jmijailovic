import boto3
import datetime
import json

session = boto3.Session(profile_name='default')
logViewsClient = session.client('firehose', region_name='us-east-2', aws_access_key_id='', aws_secret_access_key='')

try:
    s3 = boto3.client("s3", region_name='us-east-2', aws_access_key_id='', aws_secret_access_key='')
    s3.create_bucket(Bucket="jmijailovic-item-logs", CreateBucketConfiguration={
        'LocationConstraint': 'us-east-2'})
except:
    print("Bucket already exists!!")
try:
    logViewsClient.create_delivery_stream(
            DeliveryStreamName="jmijailovicLogsViewsStream",
            DeliveryStreamType="DirectPut",
            S3DestinationConfiguration={
                "RoleARN": "arn:aws:iam::{}:role/mijailovic_firehose_delivery_role".format("571632058847"),
                "BucketARN": "arn:aws:s3:::jmijailovic-item-logs",
                "Prefix": "viewLogs/",
                "ErrorOutputPrefix": "errorLogs/",
                "CompressionFormat": "UNCOMPRESSED"
            },
        )
except:
    print("Delivery stream already exists!!")

records = []

with open("LogViews.json") as json_file:
    lines = json.load(json_file)
    # count = 1
    date_time = datetime.datetime.now()
    hour_to_compare = '{}-{}-{} {}'.format(date_time.year, date_time.month, date_time.day, date_time.hour)

    for line in lines:
        # if count % 500 == 0:
        line_timestamp = datetime.datetime.strptime(line['timestamp'], '%Y-%m-%d %H:%M:%S')
        batch_hour = '{}-{}-{} {}'.format(line_timestamp.year, line_timestamp.month, line_timestamp.day, line_timestamp.hour)

        if batch_hour == hour_to_compare:
            response = logViewsClient.put_record_batch(
                DeliveryStreamName='jmijailovicLogsViewsStream',
                Records=records
            )
            print(response)
            print(len(records))
            records.clear()
        record = {
            "Data": json.dumps(line)
        }
        records.append(record)
        # count = count + 1
        hour_to_compare = batch_hour

    if len(records) > 0:
        print(len(records))
        response = logViewsClient.put_record_batch(
            DeliveryStreamName='jmijailovicLogsViewsStream',
            Records=records
        )
        print(response)