 # 1. NSL-KDD Dataset

The NSL-KDD dataset is an improved version of the original KDD Cup 1999 dataset, designed to avoid some of its inherent issues. It is widely used for network intrusion detection research.
Download NSL-KDD Dataset: NSL-KDD Dataset

# 2. CICIDS 2017 Dataset

The CICIDS 2017 dataset contains labeled data for various types of attacks and normal traffic. It is one of the most comprehensive datasets for network intrusion detection.
Download CICIDS 2017 Dataset: CICIDS 2017 Dataset

# 3. UNSW-NB15 Dataset

The UNSW-NB15 dataset is created using an IXIA PerfectStorm tool in the Cyber Range Lab of UNSW Canberra. It contains modern network traffic and attack patterns.
Download UNSW-NB15 Dataset: UNSW-NB15 Dataset

Dataset Structure and Labels

Most of these datasets come with both raw network traffic and labeled data indicating whether the traffic is normal or an attack, and the type of attack.
Example Data Structure for NSL-KDD

The NSL-KDD dataset contains the following features and labels:

    Features:
        Duration
        Protocol type (e.g., TCP, UDP)
        Service (e.g., HTTP, FTP)
        Flag
        Source bytes
        Destination bytes
        Land (1 if the connection is from/to the same host/port; 0 otherwise)
        Wrong fragment
        Urgent
        ... (additional features)
    Label: Indicates the type of attack or normal traffic (e.g., normal, neptune, smurf, teardrop, etc.).

Downloading and Preparing Data
Downloading NSL-KDD Dataset

Download the dataset from the NSL-KDD Dataset page. You will find links to the KDDTrain+.txt and KDDTest+.txt files.
    Upload to S3: Upload the dataset files to your S3 bucket for easy access.

Preparing the Data in SageMaker

  Upload the dataset to your S3 bucket:
        Go to the S3 dashboard.
        Click on "Create bucket" if you haven't already.
        Upload the KDDTrain+.txt and KDDTest+.txt files to your bucket.

  Preprocess the Data in SageMaker:
        Open your SageMaker notebook instance.
        Create a new Jupyter notebook and use the following code to load and preprocess the dataset:

          import pandas as pd
          import boto3
          import sagemaker
          from sklearn.model_selection import train_test_split
          from sklearn.preprocessing import StandardScaler
          
          # Define S3 bucket and file paths
          bucket = 'my-flow-logs-bucket'
          train_file = 'KDDTrain+.txt'
          test_file = 'KDDTest+.txt'
          
          # Load data from S3
          s3 = boto3.client('s3')
          s3.download_file(bucket, train_file, 'KDDTrain+.txt')
          s3.download_file(bucket, test_file, 'KDDTest+.txt')
          
          # Column names based on NSL-KDD dataset documentation
          col_names = [
              "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", 
              "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised", 
              "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells", 
              "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", 
              "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", 
              "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", 
              "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", 
              "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", 
              "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", 
              "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label"
          ]
          
          # Load datasets
          train_df = pd.read_csv('KDDTrain+.txt', names=col_names)
          test_df = pd.read_csv('KDDTest+.txt', names=col_names)
          
          # Encode categorical variables
          train_df = pd.get_dummies(train_df, columns=["protocol_type", "service", "flag"])
          test_df = pd.get_dummies(test_df, columns=["protocol_type", "service", "flag"])
          
          # Ensure train and test data have the same columns
          train_df, test_df = train_df.align(test_df, join='inner', axis=1)
          
          # Separate features and labels
          X_train = train_df.drop(['label'], axis=1)
          y_train = train_df['label']
          X_test = test_df.drop(['label'], axis=1)
          y_test = test_df['label']
          
          # Standardize the features
          scaler = StandardScaler()
          X_train = scaler.fit_transform(X_train)
          X_test = scaler.transform(X_test)
          
          # Save preprocessed data back to S3 for training
          pd.DataFrame(X_train).to_csv('train_features.csv', index=False)
          pd.DataFrame(y_train).to_csv('train_labels.csv', index=False)
          pd.DataFrame(X_test).to_csv('test_features.csv', index=False)
          pd.DataFrame(y_test).to_csv('test_labels.csv', index=False)
          
          s3.upload_file('train_features.csv', bucket, 'processed/train_features.csv')
          s3.upload_file('train_labels.csv', bucket, 'processed/train_labels.csv')
          s3.upload_file('test_features.csv', bucket, 'processed/test_features.csv')
          s3.upload_file('test_labels.csv', bucket, 'processed/test_labels.csv')

Training the Model in SageMaker
Configure and Train:
        Use the preprocessed data from S3 to train your model in SageMaker.


      from sagemaker import get_execution_role
      from sagemaker.inputs import TrainingInput
      from sagemaker.xgboost import XGBoost
      
      # Get execution role
      role = get_execution_role()
      
      # Set S3 paths
      s3_train_features = f's3://{bucket}/processed/train_features.csv'
      s3_train_labels = f's3://{bucket}/processed/train_labels.csv'
      s3_test_features = f's3://{bucket}/processed/test_features.csv'
      s3_test_labels = f's3://{bucket}/processed/test_labels.csv'
      
      # Create XGBoost estimator
      xgb = XGBoost(entry_point='train.py',
                    role=role,
                    instance_count=1,
                    instance_type='ml.m5.xlarge',
                    framework_version='1.3-1')
      
      # Set hyperparameters
      xgb.set_hyperparameters(objective='binary:logistic', num_round=100)
      
      # Define input data
      train_input = TrainingInput(s3_train_features, content_type='csv')
      train_labels_input = TrainingInput(s3_train_labels, content_type='csv')
      
      # Fit the model
      xgb.fit({'train': [train_input, train_labels_input]})

  Deploy the Model:
        Deploy the model as an endpoint in SageMaker.

    # Deploy the model
    predictor = xgb.deploy(initial_instance_count=1, instance_type='ml.m5.xlarge')
    
    # Predict using the deployed model
    result = predictor.predict(test_data)
    print(result)

By following these steps, you can utilize the NSL-KDD dataset, preprocess the data, train a machine learning model using Amazon SageMaker, and deploy it for real-time intrusion detection.
