import json

import boto3
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

try:
    spark = SparkSession.builder.appName("fraud-ips-identification").getOrCreate()
except ValueError:
    print("Spark Session already exist!")

dataTxt = spark.read.text('s3://jmijailovic-item-logs/viewLogs/2020/06/10/14/')
value = str(dataTxt.select("value").collect()[0]).replace("Row(value='", "")[:-2]
jsonData = "[" + value.replace("}", "},", value.count("}") - 1) + "]"
print(jsonData)
df = spark.createDataFrame(json.loads(jsonData))

df.show()
df.createOrReplaceTempView("df")

ips = spark.sql(
    'SELECT DISTINCT x.user_ip FROM df x WHERE (SELECT COUNT(*) FROM df y WHERE x.user_ip=y.user_ip AND x.timestamp=y.timestamp)>5')

table_name = 'FraudulentIps'

dynamodb = boto3.resource('dynamodb')

existing_tables = dynamodb.meta.client.list_tables()['TableNames']
if table_name not in existing_tables:
    print("Creating table %s" % table_name)
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'user_ip', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'user_ip', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    print("Waiting for table to be ready")

    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
ips.show()

ips.write.option("tableName", table_name).option("region", "us-east-2").format("dynamodb").save()

# --packages com.audienceproject:spark-dynamodb_2.11:1.0.3
