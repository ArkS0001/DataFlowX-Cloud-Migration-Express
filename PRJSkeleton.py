import boto3

# Initialize AWS clients
s3_client = boto3.client('s3')
glue_client = boto3.client('glue')

# 1. Create an S3 bucket
bucket_name = 'your-bucket-name'
s3_client.create_bucket(Bucket=bucket_name)

# 2. Create a Glue crawler
crawler_name = 'your-crawler-name'
database_name = 'your-database-name'
crawler_role = 'arn:aws:iam::your-account-id:role/your-role-name'  # Replace with your IAM role ARN

response = glue_client.create_crawler(
    Name=crawler_name,
    Role=crawler_role,
    DatabaseName=database_name,
    Targets={
        'S3Targets': [
            {
                'Path': f's3://{bucket_name}/your-folder-path'
            },
        ]
    }
)

# 3. Define an ETL job
job_name = 'your-etl-job-name'
script_location = 's3://your-script-location/script.py'  # S3 location of your ETL script
glue_role = 'arn:aws:iam::your-account-id:role/your-role-name'  # Replace with your Glue role ARN

response = glue_client.create_job(
    Name=job_name,
    Role=glue_role,
    Command={
        'Name': 'glueetl',
        'ScriptLocation': script_location
    },
    DefaultArguments={
        '--job-language': 'python',
        '--job-bookmark-option': 'job-bookmark-enable'
    }
)

# 4. Load data into Redshift
redshift_cluster_id = 'your-redshift-cluster-id'
redshift_database_name = 'your-redshift-database-name'
redshift_username = 'your-redshift-username'
redshift_password = 'your-redshift-password'

# Use psycopg2 library to connect and execute SQL commands
import psycopg2

conn = psycopg2.connect(
    dbname=redshift_database_name,
    user=redshift_username,
    password=redshift_password,
    host=f'{redshift_cluster_id}.your-region.redshift.amazonaws.com',
    port='5439'
)

cur = conn.cursor()

# Example: Create a table in Redshift
cur.execute("""
    CREATE TABLE IF NOT EXISTS example_table (
        id INT,
        name VARCHAR(100)
    );
""")

# Example: Load data from S3 into Redshift
cur.execute("""
    COPY example_table
    FROM 's3://your-bucket-name/your-folder-path/'
    IAM_ROLE 'arn:aws:iam::your-account-id:role/your-redshift-role-name'
    CSV;
""")

conn.commit()
conn.close()
