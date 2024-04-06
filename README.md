# Automated Data Analytics on AWS

The Automated Data Analytics on AWS solution provides an end-to-end data platform for ingesting, transforming, managing and querying datasets. This helps analysts and business users manage and gain insights from data without deep technical experience using Amazon Web Services (AWS). It has an open-sourced architecture with connectors to commonly used AWS services, along with third-party data sources and services. This solution also provides an user interface (UI) to search, share, manage, and query datasets using standard SQL commands.

## Architecture overview

The following diagram represents the solution's architecture design.

![solution_architecture_diagram](https://github.com/ArkS0001/DataFlowX-Cloud-Service/assets/113760964/d1c3cd34-884b-40d0-a3b8-cb61bea9021d)


The Automated Data Analytics on AWS solution automates the building of data pipelines that are optimized for the size, frequency of update, and type of data. These data pipelines handle the data ingestion, transformations, and queries.

The Automated Data Analytics on AWS solution creates and integrates a combination of AWS services required to perform these tasks, abstracted through a user interface. These services include AWS Glue crawlers, jobs, workflows and triggers, along with S3 buckets, IAM integration, and other services. Additionally, the solution automatically detects and redacts personally identifiable information (PII) with granular security and governance controls.

For more information on the solution’s architecture, refer to the [implementation guide](https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/architecture-overview.html).

---

## Prerequisites

### Build environment specifications

- To build and deploy this solution, we recommend using Ubuntu with minimum 4 cores CPU, 16GB RAM. Mac(Intel) or other Linux distributions are also supported.
- The computer used to build the solution must be able to access the internet.

### AWS Account

- A CDK bootstrapped AWS account.

  - https://docs.aws.amazon.com/cdk/latest/guide/bootstrapping.html

- Sufficient AWS Lambda Concurrent executions limit
  - Please use AWS Service Quotas to verify AWS Lambda Concurrent exeuctions `Applied quota value` in your account is greater or equal to the `AWS default quota value` (which is 1000). Click this [link](https://console.aws.amazon.com/servicequotas/home/services/lambda/quotas/L-B99A9384) to check it in your AWS Console. If `Applied quota value` is less than 1000, please use `Request quota increase` button to make a request to increase it to at least 1000 before deploying the solution. For more details, please refer to [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html).

### Tools

- The latest version of the AWS CLI, installed and configured.
  - https://aws.amazon.com/cli/ .
- node.js version 16.
  - https://docs.npmjs.com/getting-started
  - Below are the example commands for installing nvm and node 16, please make sure those commands fit your build environment before using them.
    ```
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash
    exec $SHELL -l
    nvm install 16
    ```
- install yarn
  ```
  npm install --global yarn
  ```
- Python 3.9

  - We recommend creating a python virtual env using `pipenv` to avoid version conflicts
  - Below are the example commands for installing python 3.9 on Amazon Linux 2 and configure the virtual env, please make sure those commands fit your build environment before using them.

    ```
    pip3 install --user pipenv
    export PATH="/home/<YOUR_USERNAME>/.local/bin:$PATH"
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    export PATH="/home/<YOUR_USERNAME>/.pyenv/bin:$PATH"
    sudo yum-builddep python3
    pipenv --python 3.9

    # after clone the Ada repository, navigate to the Ada directory and run the following commands
    cd <Ada directory>
    pyenv local 3.9
    eval "$(pyenv init -)"
    ```

- Docker Desktop (>= v20.10)
  - https://www.docker.com/get-started/

> **Note regarding AWS CDK version:** We recommend running all `cdk <cmd>` related tasks via `yarn cdk <cmd>` to ensure exact version parity. If you choose to run globally installed `cdk` command, ensure you have a compatible version of [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html) installed globally.

---

## Build and run the unit tests

1. Clone the solution source code from its GitHub repository. `git clone https://github.com/aws-solutions/automated-data-analytics-on-aws`
2. Open the terminal and navigate to the source folder created in step 1. `cd automated-data-analytics-on-aws/source`
3. Run the following command.

   ```
   chmod +x ./run-all-tests.sh
   ./run-all-tests.sh
   ```

The `/source/run-all-tests.sh` script is the centralized script to install all dependencies, build the solution from source code and execute all unit tests.

**The build process including downloading dependencies takes about 60 minutes the first time.**

---

## File structure

After you have successfully cloned the repository into your local development environment, you will see the following file structure in your editor.

```
|- .github/ ...                       - resources for open-source contributions.
|- source/                            - solution's source code
  |- @types                           - type utilities
  |- cypress                          - cypress tests
  |- images                           - images files for the documentation
  |- packages                         - multiple packages of solution source code, including unit tests
  |- scripts                          - helper scripts
  |- header.txt                       - license header
  |- lerna.json                       - configuration file for lerna
  |- packages.json                    - package file for solution root package
  |- run-all-tests.sh                 - runs all tests within the /source folder
  |- yarn-audit.js                    - helper script for yarn audit
  |- yarn.lock                        - yarn lockfile
|- .gitignore
|- CHANGELOG.md                       - changelog file to track changes between versions
|- CODE_OF_CONDUCT.md                 - code of conduct for open source contribution
|- CONTRIBUTING.md                    - detailed information about open source contribution
|- LICENSE.txt                        - Apache 2.0 license.
|- NOTICE.txt                         - Copyrights for Automated Data Analytics on AWS solution
|- THIRDPARTY_LICENSE.txt             - Copyrights licenses for third party software that was used in this solution
|- README.md                          - this file
```

---

## Deploying the solution

Before you begin, ensure that:

- The solution has been built and all unit tests have passed as described in the [Build and run unit tests](#build-and-run-the-unit-tests) section.
- You have configured the computer used to deploy the solution with the correct AWS credentials to access the AWS account that Automated Data Analytics on AWS solution will be deployed to.

1. Set the deployment region `export AWS_REGION=<region-id>`. For a list of supported AWS region, refer to https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/design-considerations.html
2. Make sure the current directory is in `automated-data-analytics-on-aws/source`
3. Deploy the Automated Data Analytics on AWS solution:
   - To deploy the Automated Data Analytics on AWS solution with its default security settings, use the command below:
     `yarn deploy-solution --parameters adminEmail="<Your email address>" --parameters adminPhoneNumber="<Your mobile number for MFA>"`
   - If the deployment is for evaluation purposes and does not contain any sensitive data, the default Multi-factor Authentication(MFA) feature can be set to `optional` to simplify the process. If this is preferred, use the following command for deployment:
     `yarn deploy-solution --parameters adminEmail="<Your email address>" --parameters adminMFA='OPTIONAL' --parameters advancedSecurityMode='OFF'`

The deployment may take up to 60 minutes to complete. During deployment the temporary password for the root administrator will be sent via email to the specified _adminEmail_. The email address and temporary password received in email can be used to log into the Automated Data Analytics on AWS solution for the initial setup.

After the solution has been deployed, the CDK returns the following information. Using this information, follow the steps to access the Automated Data Analytics on AWS solution.

> **Note**: To view the information returned by CDK from the AWS CloudFormation Console, navigate to the **Ada** stack and select the **Outputs** section.

```
Outputs:
Ada.AthenaProxyApiUrl = example.cloudfront.net:443
Ada.BaseApiUrl = https://example.execute-api.ap-southeast-2.amazonaws.com/prod/
Ada.CognitoUserPoolId = ap-southeast-2_Example
Ada.ExportNamespaceGlobalUUID = example
Ada.RetainedResourcesExport = ["arn:aws:kms:ap-southeast-2:123456789012:key/5dad9516-0007-4993-a613-example","arn:aws:kms:ap-southeast-2:123456789012:key/21d45985-6c92-41e9-a762-example","arn:aws:s3:::ada-dataproductservicestack752cb9-databucket-hash","arn:aws:s3:::ada-dataproductservicestack752-scriptsbucket-hash","arn:aws:s3:::ada-dataproductservicestack-fileuploadbucket-hash"]
Ada.UserPoolClientId = example
Ada.WebsiteUrl = https://example1234.cloudfront.net/
```

- `AthenaProxyApiUrl`: The URL for connecting Automated Data Analytics on AWS with Tableau / PowerBI via JDBC/ODBC.
- `BasedApiUrl`: Rest API URL.
- `CognitoUserPoolId`: Cognito User Pool id.
- `ExportNamespaceGlobalUUID`: A global unique identifier specific to this deployment.
- `RetainedResourcesExport`: A list of AWS Resources ARNs for which the resources will be retained if this solution is uninstalled (tore down) from the web console with retaining data or tore down from AWS CloudFormation Console.
- `UserPoolClientId`: Cognito user pool app client id
- `WebsiteUrl`: Automated Data Analytics on AWS web UI URL

## Accessing the solution web UI

1. Open `WebsiteUrl` in your browser. We recommend using Chrome. You will be redirected to the sign in page that requires username and password.
2. Sign in with the email address specified during deployment as username and use the temporary password received via email after deployment. Note that the sender of the temporary password email is `no-reply@verificationemail.com`.
3. During the sign in, you are required to set a new password when signing in for the first time. If the solution is deployed with MFA enabled, the MFA code is sent to the mobile number specified as _AdminPhone_ as a text message and you will need the MFA code for signing in.
4. After signing in, you can view the Automated Data Analytics on AWS web UI. The current user is the _root administrator_ user who has the highest level of permission for Automated Data Analytics on AWS. We recommend you keep these credentials secure.

We recommend using an external OpenID Connect or SAML 2.0 compatible identity provider to manage your users who need access to Automated Data Analytics on AWS. If there is an existing enterprise Identity Provider, you can integrate it with Automated Data Analytics on AWS. The root administrator user can set it up by accessing `Admin -> Identity Provider` in the Automated Data Analytics on AWS Web UI.

For more information on how to set up your Identity Provider, refer to the [implementation guide](https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/using-the-automated-data-analytics-on-aws-solution.html#identity-providers)

---

## Uninstalling the solution

You can uninstall the solution either from the Automated Data Analytics on AWS web UI or by directly deleting the stacks from the AWS CloudFormation console.

To uninstall the solution from the Automated Data Analytics on AWS web UI:

1. Open Automated Data Analytics on AWS web UI and login with the root administrator user details.
2. On the left navigation panel, click `Admin -> TearDown`
   > **Note**: Using the Teardown page, you can permanently remove the Automated Data Analytics on AWS solution from your account. The Teardown option is only available for users with <i>root_admin</i> access.
3. From the Teardown page, choose one of these following actions:
   - **Delete solution** – This will uninstall all the resources associated with the solution but retain the imported data.
   - **Delete solution and data** – This will uninstall all the resources associated with the solution and destroy the imported data.
4. Follow the link displayed on the web UI to AWS CloudFormation Console to monitor all Automated Data Analytics on AWS stacks to be deleted.

**Note**: If you chose to retain data, the data buckets and KMS keys for the data buckets will be retained.

To uninstall the solution from AWS CloudFormation console:

1. Go to the AWS CloudFormation console, and on the **Stacks** page, filter by stack name _ada-dp-_ to get list of dynamic infrastructure created for each Data Product.
2. Navigate to your `Ada` stack, and check its Output section, note down the value of the key `RetainedResourcesExport` and copy it to a text file to keep. These resources are retained after the main Automated Data Analytics on AWS stack is deleted.
3. In AWS CloudFormation console page, select the **Ada** stack and select **Delete**. Wait until all Automated Data Analytics on AWS nested stacks and main stack are deleted completely.
4. The data buckets and the KMS keys to encrypted data in them are retained (as listed out in `RetainedResourcesExport`). You can migrate data out of these buckets.
5. After the migration is completed, navigate to the AWS S3 console, choose each bucket, empty it and delete it for all the buckets that were listed in the `RetainedResourcesExport` file.
6. After deleting the buckets, navigate to AWS KMS Console and delete the two KMS keys that were listed in the `RetainedResourcesExport` file.

---

## Collection of operational metrics

This solution collects anonymized operational metrics to help AWS improve the quality of features of the solution. For more information, including how to disable this capability, refer to the [implementation guide](https://docs.aws.amazon.com/solutions/latest/automated-data-analytics-on-aws/collection-of-operational-metrics.html).

---

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://www.apache.org/licenses/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and limitations under the License.



![WhatsApp Image 2024-04-01 at 4 02 28 PM](https://github.com/ArkS0001/DataFlowX-Cloud-Service/assets/113760964/65e3eb0e-2e8f-4ae6-92ce-a73c6d0b9b20)


![The-microbiome-data-analysis-pipeline-using-AWS-AWS-Amazon-Web-Services-S3-Simple](https://github.com/ArkS0001/DataFlowX-Cloud-Migration-Express/assets/113760964/e4fab5f7-9013-4ebb-adfa-ab9692f9ab86)

Setting up an AWS pipeline for data analytics involves several steps, typically utilizing AWS services like S3, Glue, Athena, Redshift, and others. Here's a basic outline of how you might set up such a pipeline:

    Data Collection: Begin by collecting your data from various sources. This might include databases, log files, APIs, etc. You can store this raw data in Amazon S3 buckets.

    Data Ingestion: Once the data is collected, you need to ingest it into your AWS environment. AWS Glue is a fully managed extract, transform, and load (ETL) service that can help you with this task. Glue crawlers can automatically discover your data and create metadata tables in the AWS Glue Data Catalog.

    Data Transformation: After ingestion, you may need to transform your data to make it suitable for analysis. AWS Glue provides a serverless environment for running ETL jobs. You can use Glue jobs to transform your data using Spark ETL scripts written in Python or Scala.

    Data Storage: Once transformed, you may want to store your data in a structured format for efficient querying. Amazon Redshift is a fully managed data warehouse service that you can use for this purpose. You can load your transformed data into Redshift tables for analysis.

    Data Analysis: With your data stored in Redshift, you can perform various types of analytics using SQL queries. You can use Amazon Athena, an interactive query service, to run SQL queries directly against data stored in S3 without needing to load it into Redshift.

    Data Visualization: Finally, you can visualize your analytics results using tools like Amazon QuickSight, a fully managed business intelligence service. QuickSight allows you to create interactive dashboards and reports to gain insights from your data.

    Monitoring and Optimization: Continuously monitor the performance of your pipeline and optimize it for cost and efficiency. AWS CloudWatch provides monitoring and logging capabilities that you can use to track the performance of your pipeline and identify areas for improvement.

Remember, the specific services and configurations you choose will depend on your specific requirements, such as the volume and type of data you're dealing with, your budget, and your performance requirements. AWS offers a wide range of services that can be combined and customized to meet your needs.

    Set Up AWS Account: If you haven't already, sign up for an AWS account and log in to the AWS Management Console.

    Create an S3 Bucket: Navigate to the Amazon S3 console and create a new S3 bucket to store your raw data. Configure the bucket permissions as needed to allow access from other AWS services.

    Set Up AWS Glue: Go to the AWS Glue console and create a new Glue crawler. Point the crawler to your S3 bucket and configure it to discover the schema of your data. This will create metadata tables in the Glue Data Catalog.

    Define ETL Jobs: Create one or more Glue ETL jobs to transform your data. You can write custom ETL scripts using Python or Scala, or use the built-in visual ETL editor. Configure the jobs to read data from the source tables created by the crawler and write the transformed data to new destination tables.

    Set Up Amazon Redshift: Go to the Amazon Redshift console and create a new Redshift cluster. Configure the cluster settings, such as node type and number of nodes, and set up the necessary security groups and VPC settings.

    Load Data into Redshift: Once your Redshift cluster is up and running, use Glue or another ETL tool to load the transformed data from your Glue tables into Redshift tables. You can use Redshift's COPY command to efficiently load large amounts of data from S3 into Redshift.

    Perform Analytics with Amazon Athena: Navigate to the Amazon Athena console and create a new database. Define tables in Athena that point to your data stored in S3. You can then run SQL queries against these tables using the Athena query editor or any SQL client that supports JDBC/ODBC connections.

    Visualize Data with Amazon QuickSight: Go to the Amazon QuickSight console and create a new analysis. Connect QuickSight to your Redshift database or Athena database and import the necessary data. You can then create interactive dashboards and visualizations to explore your data and gain insights.

    Monitor and Optimize: Regularly monitor the performance of your pipeline using AWS CloudWatch metrics and logs. Look for opportunities to optimize your pipeline for cost and performance, such as adjusting Redshift cluster configurations or optimizing ETL job scripts.

    Automation and Maintenance: Consider automating your pipeline using AWS Step Functions, AWS Lambda, or AWS Glue workflows. This can help streamline your data processing tasks and reduce manual intervention. Also, ensure that you regularly update your pipeline as your data and business requirements evolve.

AWS pipeline for data analytics using Python and the AWS SDK (Boto3). This example will cover setting up an S3 bucket, creating a Glue crawler, defining an ETL job, and loading data into Redshift. Please note that you'll need to install the boto3 library if you haven't already (pip install boto3).

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

This code provides a basic outline of how you can interact with AWS services using Python and Boto3. Remember to replace placeholders like 'your-bucket-name', 'your-folder-path', 'your-account-id', 'your-role-name', 'your-script-location', 'your-redshift-cluster-id', 'your-redshift-database-name', 'your-redshift-username', 'your-redshift-password', and 'your-redshift-role-name' with your actual AWS resource names and configurations. Additionally, make sure you have the necessary IAM permissions to perform these actions.

1. Amazon Athena:

Amazon Athena allows you to run SQL queries directly against data stored in Amazon S3 without the need for any infrastructure setup. Here's how you can perform data analytics with Athena:

    Create Database and Tables: Define databases and tables in Athena that point to your data stored in S3. You can use the Glue Data Catalog to simplify this process.

    Run SQL Queries: Once your tables are defined, you can run SQL queries against them using the Athena query editor or any SQL client that supports JDBC/ODBC connections.

    Analyze Data: Use SQL to perform various types of analytics such as aggregations, filtering, joins, and window functions to gain insights from your data.

2. Amazon Redshift:

Amazon Redshift is a fully managed data warehouse service that allows you to analyze large volumes of data using standard SQL. Here's how you can perform data analytics with Redshift:

    Create Cluster and Database: Set up a Redshift cluster and create a database within it where you can load and analyze your data.

    Load Data: Load your data into Redshift tables either directly from S3 or using ETL tools like AWS Glue.

    Run SQL Queries: Use SQL to query your data stored in Redshift tables. Redshift supports a wide range of SQL functions and analytical capabilities.

    Optimize Performance: Tune your Redshift cluster configuration and optimize your SQL queries for performance to ensure fast query execution times.

3. Direct Querying of Data in S3:

If your data is stored in structured formats like CSV, JSON, or Parquet directly in S3, you can also query it using tools like AWS Glue or even by using libraries like Apache Spark or Presto running on Amazon EMR (Elastic MapReduce).

    Define Schema: Use tools like AWS Glue to define the schema of your data stored in S3 and create metadata tables.

    Run Queries: Once the schema is defined, you can run SQL queries against your data using services like AWS Glue or directly using SQL-on-Hadoop engines like Presto.

    Perform Analytics: Use SQL to perform various analytics tasks such as data aggregations, transformations, and joins to derive insights from your data.

Choose the approach that best fits your requirements in terms of performance, scalability, and ease of use. Additionally, consider factors like cost and data security when selecting the appropriate service for your data analytics needs.

![](https://github.com/aws-samples/aws-cdk-pipelines-datalake-infrastructure/blob/main/resources/Aws-cdk-pipelines-blog-datalake-data_lake.png)
