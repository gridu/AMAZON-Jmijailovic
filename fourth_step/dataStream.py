import json

#
import boto3

kinesis = boto3.client("kinesis", region_name='us-east-2', aws_access_key_id='',
                       aws_secret_access_key='')

# kinesis.create_stream(
#     StreamName='mijailovic-stream',
#     ShardCount=1
# )

import mysql.connector
import boto3
import os

ENDPOINT = "jmijailoviccatalog.cnz7flo1slhx.us-east-2.rds.amazonaws.com"
PORT = "3306"
USR = "jmijailovic"
PASSWD = "ZUMMopz1u7ztrBcWr9ml"
REGION = "us-east-2"
DBNAME = "jmijailovicCatalog"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

# gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = boto3.client('rds')

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)

try:
    conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PASSWD, port=PORT, database=DBNAME)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM catalog""")
    query_results = cur.fetchall()

    e = ()
    data = []

    for element in query_results:
        response = kinesis.put_record(
            Data=json.dumps({
                'item_id': str(element[0]),
                'title': str(element[1]),
                'description': str(element[2]),
                'category': str(element[3])
            }),
            PartitionKey='default',
            StreamName='mijailovic-stream'
        )

except Exception as e:
    print(e)

# aws sns create-topic --name mail-top-categories-alert --output text
# aws sns subscribe --topic-arn arn:aws:sns:us-east-2:571632058847:mail-top-categories-alert --protocol email --notification-endpoint jmijailovic@griddynamics.com
