# import psycopg2
# import boto3


# class RedshiftManager:

#     def __init__(self):
#         try:
#             self.connection = psycopg2.connect(host=ENV_RS_HOST,
#                             port= ENV_RS_PORT,
#                             dbname= ENV_RS_DATABASE,
#                             user=ENV_RS_USER,
#                             password=ENV_RS_PASSWORD
#                             )
#             self.cursor = self.connection.cursor()
#             self.redshift_role = ENV_RS_ROLE

#         except Exception as e:
#             logger.error("Exception ocurred while connect with RedShift.")
#             raise Exception(str(e))

#     def copy_table_from_avro(self,table,source_key_path):
#         query = '''
#             copy %(tablename)s
#             from %(s3_key)s
#             iam_role %(iam_role)s
#             format as avro 'auto ignorecase';
#         '''
#         try:
#             select_param = {
#                 'table_name': table,
#                 's3_key': f"s3://{ENV_BUCKET_PATH}/{source_key_path}",
#                 'iam_role': self.redshift_role
#             }
#             self.cursor.execute(query, select_param)
#             self.connection.commit()
#         except Exception as e:
#             logger.error("Exception ocurred while COPY to RedShift.")
#             raise Exception(str(e))

#     def read_query_as_pandas(self, query):
#         try:
#             return pd.read_sql(query, self.connection)
#         except Exception as e:
#             logger.error("Exception ocurred while read query to pandas into RedShift.")
#             raise Exception(str(e))

# class S3Manager:

#     def __init__(self):
#         try:
#             self.s3 = None if RUN_LOCALLY else boto3.client('s3', region_name=ENV_AWS_REGION)
#         except Exception as e:
#             logger.error("Exception ocurred while connect with S3.")
#             raise Exception(str(e))

#     def read_from_S3(self, key):
#         try:
#             if RUN_LOCALLY:
#                 filename = os.path.join(PATH_LOCAL, key)
#                 return pd.read_csv(filename)
#             else:
#                 obj = self.s3.get_object(Bucket=ENV_BUCKET_PATH, Key=key)
#                 return pd.read_csv(io.BytesIO(obj['Body'].read()))
#         except Exception as e:
#             print("Exception ocurred while read from S3.")
#             raise Exception(str(e))

#     def load_to_S3(self, key, object):
#         try:
#             if RUN_LOCALLY:
#                 filename = os.path.join(PATH_LOCAL, key)
#                 os.makedirs(os.path.dirname(filename), exist_ok=True)
#                 if isinstance(object, bytes):
#                     with open(filename, 'wb') as file:
#                         file.write(object)
#                 else:
#                     with open(filename, 'w') as file:
#                         file.write(object)
#             else:
#                 self.s3.put_object(Bucket=ENV_BUCKET_PATH, Key=key, Body=object)
#         except Exception as e:
#             print("Exception ocurred while load data to S3.")
#             raise Exception(str(e))
