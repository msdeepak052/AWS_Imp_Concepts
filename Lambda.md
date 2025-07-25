# AWS Lambda Hands-on Examples with Detailed Steps

## Example 1: Simple Hello World Lambda (Python)

**Objective**: Create a basic Lambda function that returns "Hello, World!"

**Steps**:
1. Go to AWS Lambda console
2. Click "Create function"
3. Select "Author from scratch"
4. Enter function name: `hello-world`
5. Select runtime: Python 3.x
6. Click "Create function"
7. In the code editor, replace the default code with:
```python
import json

def lambda_handler(event, context):
    # TODO implement
    print("hello world")
    print(event)
    print(context)
    print("hello world 2")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

```
![image](https://github.com/user-attachments/assets/22f3d8b8-f442-4466-a9b6-d846ce13915a)

8. Click "Deploy"
9. Click "Test" and create a new test event (use default template)
10. Click "Test" again to see the output

![image](https://github.com/user-attachments/assets/5f432fb3-14d4-4908-afea-cc2bce5d6c2a)

#### CloudWatch Logs

![image](https://github.com/user-attachments/assets/7f6b2303-5a30-4294-adb7-7f2cea976adb)

![image](https://github.com/user-attachments/assets/37fce163-3973-465b-84a9-7c7b82e7913f)


**Explanation**: This is the simplest Lambda function that demonstrates the basic structure. The `lambda_handler` is the entry point that AWS calls when your function is invoked.

## Example 2: S3 Trigger for Image Processing

**Objective**: Create a Lambda that processes images when uploaded to S3

**Steps**:
1. Create an S3 bucket

![image](https://github.com/user-attachments/assets/7dcdd597-e968-4d36-9ef5-b7da52242e9b)

2. Create a new Lambda function named `image-processor` with Python runtime

![image](https://github.com/user-attachments/assets/e01eb1d0-7be8-47e3-a20d-63b75aa69b77)

3. Add the following permissions to the Lambda's execution role:
   - `s3:GetObject`
   - `s3:PutObject`

![image](https://github.com/user-attachments/assets/8c5d0bfe-c52c-41f2-a217-721fe4c3ef43)

4. Install the Pillow library (for image processing):
   - Create a deployment package or use Lambda Layers

#### Here's a detailed step-by-step guide for installing the Pillow library for your S3-triggered image processing Lambda function:

---

#### **Steps to Create a Pillow Lambda Layer:**

#### 1. Create the directory structure
```bash
mkdir -p pillow_layer/python
cd pillow_layer
```

#### 2. Run the correct Docker command (using AWS's official build image)
```bash
docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.10" /bin/sh -c "pip install pillow -t python/ && chmod -R 755 python; exit"
```

#### 3. Verify the contents
```bash
ls -la python/
```

#### 4. Create the zip file
```bash
zip -r pillow_layer.zip python
```

#### Download the file from the cloudshell using the 3 dots and provide the zip file complete path
![image](https://github.com/user-attachments/assets/cfd9c9e7-9a9e-4361-bf82-06e7e5fb13da)

![image](https://github.com/user-attachments/assets/3ed5c1a6-9aa3-4bd1-a4ce-ac522dc66fee)


4. **Create the Lambda Layer**:
   - Go to AWS Lambda Console → **Layers** → **Create layer**
   - Name: `pillow-layer`
   - Upload your `pillow_layer.zip` file
   - Select compatible runtimes (Python 3.8, 3.9, etc.)
   - Click **Create**

![image](https://github.com/user-attachments/assets/ba22a366-bbbb-493b-a863-a8725173defd)

![image](https://github.com/user-attachments/assets/806a7a62-dc61-4190-875a-1f93521d40f5)


5. **Attach the Layer to your Lambda**:
   - Open your `image-processor` Lambda function
   - Scroll to **Layers** section → Click **Add a layer**
    ![image](https://github.com/user-attachments/assets/3be2905d-8f67-47de-9c90-1eefb0026262)

   - Choose **Custom layers** → Select `pillow-layer`
   - Click **Add**

    ![image](https://github.com/user-attachments/assets/8cdc62d2-d2e4-4f17-ba21-a61173746ddd)


---

5. Use this code:
```python
import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the uploaded file
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download the image
    file_byte_string = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    image = Image.open(io.BytesIO(file_byte_string))
    
    # Create thumbnail
    image.thumbnail((100, 100))
    
    # Save thumbnail to S3
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)
    
    s3.put_object(
        Bucket=bucket,
        Key=f"thumbnails/{key}",
        Body=buffer
    )
    
    return {
        'statusCode': 200,
        'body': 'Thumbnail created successfully!'
    }
```
![image](https://github.com/user-attachments/assets/9d81e272-abc0-4165-a956-99a2441bc900)


6. Configure S3 trigger in Lambda:
   - In Lambda console, go to "Add trigger"
   - Select S3
   - Choose your bucket
   - Event type: "All object create events"
   - Prefix: "uploads/" (optional)

![image](https://github.com/user-attachments/assets/bca17e1c-6cf0-421a-91d6-53ae805e52a3)

![image](https://github.com/user-attachments/assets/5c091e30-4d76-4d09-b196-1daa3f188ee8)

![image](https://github.com/user-attachments/assets/54c0b673-5f40-4923-b083-003c1a62bf6e)

![image](https://github.com/user-attachments/assets/df0eda75-9a44-4a09-bf26-ac9d81cf8e8c)

7. Test by uploading an image to your S3 bucket

![image](https://github.com/user-attachments/assets/fe087ec1-cd45-49f6-9072-ea5b66fdc4a3)

![image](https://github.com/user-attachments/assets/7a70b7a9-6cc7-4ee6-b659-2b8139fc90b2)

![image](https://github.com/user-attachments/assets/62585862-bc7c-4e8d-881f-2476d7145548)

![image](https://github.com/user-attachments/assets/df12ef27-c7db-4dbd-80e2-dcebd197f273)



**Explanation**: This demonstrates event-driven architecture where Lambda responds to S3 events. The function processes the image and creates a thumbnail version.

## Example 3: API Gateway Integration (REST API)

**Objective**: Create a Lambda-powered REST API with API Gateway

**Steps**:
1. Create a new Lambda function named `api-example` with Node.js runtime
2. Use this code:
```javascript
export const handler = async (event) => {
    const response = {
        statusCode: 200,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: "Hello from Lambda!",
            input: event
        })
    };
    return response;
};
```
![image](https://github.com/user-attachments/assets/21ec65f9-c64c-4628-b4ce-dee22b46666e)

3. In API Gateway console, create a new REST API

![image](https://github.com/user-attachments/assets/bbc4ed96-9ab6-4e26-b50b-0931ae83ef0b)

4. Create a resource (e.g., `/hello`)

![image](https://github.com/user-attachments/assets/834ce3a9-0713-4c92-a62b-1c984dd92a13)

5. Create a GET method and connect it to your Lambda function
![image](https://github.com/user-attachments/assets/3a146d74-e8b8-4d4e-a471-21a25ba7f7a6)

6. Deploy the API to a stage (e.g., "prod")
![image](https://github.com/user-attachments/assets/df70b8c2-b8d7-4af3-a8a6-a14f7c859e2b)

7. Test the endpoint using the provided URL

![image](https://github.com/user-attachments/assets/10d27fa6-3085-44aa-8d8b-419eb643c894)

![image](https://github.com/user-attachments/assets/eaf41b45-9829-4fd6-83b8-5acf140a6381)




**Explanation**: This shows how to expose Lambda functions as HTTP endpoints. API Gateway handles the HTTP protocol while Lambda processes the business logic.

## Example 4: Scheduled Lambda with CloudWatch Events

**Objective**: Create a Lambda that runs on a schedule

**Steps**:
1. Create a new Lambda function named `scheduled-task` with Python runtime
2. Use this code:
```python
import datetime

def lambda_handler(event, context):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Current time:", current_time)
    
    # Add your scheduled task logic here
    # For example: database cleanup, report generation, etc.
    
    return {
        'statusCode': 200,
        'body': f'Task executed at {current_time}'
    }
```
3. In Lambda console, go to "Add trigger"
4. Select "EventBridge (CloudWatch Events)"
5. Create a new rule:
   - Rule type: "Schedule expression"
   - Schedule expression: `rate(5 minutes)` (runs every 5 minutes)
6. Click "Add"
7. Wait for the schedule to trigger and check CloudWatch logs

**Explanation**: This demonstrates how to run Lambda functions on a schedule, useful for cron-like jobs.

## Example 5: DynamoDB Stream Processor

**Objective**: Process DynamoDB changes in real-time

**Steps**:
1. Create a DynamoDB table with "id" as primary key
2. Enable DynamoDB Streams on the table
3. Create a new Lambda function named `dynamodb-stream-processor` with Node.js runtime
4. Add DynamoDB stream read permissions to the Lambda's execution role
5. Use this code:
```javascript
exports.handler = async (event) => {
    console.log("Received event:", JSON.stringify(event, null, 2));
    
    event.Records.forEach((record) => {
        console.log("Record:", JSON.stringify(record, null, 2));
        
        if (record.eventName === 'INSERT') {
            console.log("New item created:", record.dynamodb.NewImage);
        } else if (record.eventName === 'MODIFY') {
            console.log("Item modified - old:", record.dynamodb.OldImage);
            console.log("Item modified - new:", record.dynamodb.NewImage);
        } else if (record.eventName === 'REMOVE') {
            console.log("Item deleted:", record.dynamodb.OldImage);
        }
    });
    
    return `Successfully processed ${event.Records.length} records.`;
};
```
6. Configure DynamoDB stream as trigger for the Lambda
7. Test by creating, updating, and deleting items in DynamoDB
8. Check CloudWatch logs for the output

**Explanation**: This shows how to build real-time applications that react to database changes.

---

## **Example 6: Serverless File Processing Pipeline**  
### **Objective**: Process CSV files automatically when uploaded to S3 using Lambda  

---

### **Step 1: Create S3 Buckets**  
1. Go to **AWS S3 Console** → **Create Bucket**.  
   - **Bucket 1**: `input-csv-files` (stores raw CSV uploads)  
   - **Bucket 2**: `processed-csv-files` (stores processed CSVs)  
   - *Leave default settings (Region: Your preferred region, e.g., `ap-south-1`)*.  
![image](https://github.com/user-attachments/assets/4305609e-06cc-467b-a6ae-0babbed502df)
![image](https://github.com/user-attachments/assets/c91b742b-e2f9-4204-ad33-01db8c846761)
![image](https://github.com/user-attachments/assets/b893e6f2-b668-467c-9a08-80341b9e12fa)

---

### **Step 2: Create Lambda Function**  
1. Go to **AWS Lambda Console** → **Create Function**.  
   - **Name**: `csv-processor`  
   - **Runtime**: `Python 3.12` (or latest supported)  
   - **Permissions**:  
     - Choose *"Create a new role with basic Lambda permissions"*.  
     - After creation, attach **S3 read/write policies** (see **Step 3**).  
![image](https://github.com/user-attachments/assets/1757fd5d-8d5a-4e90-b2e9-4260225fd372)

---

### **Step 3: Add S3 Permissions to Lambda Role**  
1. Open the **IAM Console** → **Roles**.  
2. Find the role created for `csv-processor` (e.g., `csv-processor-role-xyz`).  
3. Click **Add Permissions** → **Attach Policies**.  
   - Add:  
     - `AmazonS3FullAccess` (for testing)  
     - *Or create a custom policy* with:  
       ```json
       {
           "Version": "2012-10-17",
           "Statement": [
               {
                   "Effect": "Allow",
                   "Action": [
                       "s3:GetObject",
                       "s3:PutObject"
                   ],
                   "Resource": [
                       "arn:aws:s3:::input-csv-files/*",
                       "arn:aws:s3:::processed-csv-files/*"
                   ]
               }
           ]
       }
       ```
![image](https://github.com/user-attachments/assets/5dc104d7-cfd6-408c-af60-a19599a89f5a)

---

### **Step 4: Paste Lambda Code**  
Replace the default code with:  
```python
import boto3
import csv
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the uploaded CSV file details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download the CSV
    csv_file = s3.get_object(Bucket=bucket, Key=key)
    csv_content = csv_file['Body'].read().decode('utf-8')
    
    # Process CSV (convert "name" column to uppercase)
    reader = csv.DictReader(io.StringIO(csv_content))
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
    writer.writeheader()
    
    for row in reader:
        if 'name' in row:  # Check if 'name' column exists
            row['name'] = row['name'].upper()
        writer.writerow(row)
    
    # Upload processed CSV to the "processed-csv-files" bucket
    processed_key = f"processed_{key}"
    s3.put_object(
        Bucket='processed-csv-files',
        Key=processed_key,
        Body=output.getvalue()
    )
    
    return {
        'statusCode': 200,
        'body': f'CSV processed! Saved to processed-csv-files/{processed_key}'
    }
```
**Click "Deploy"** to save.
![image](https://github.com/user-attachments/assets/e46c8f73-16d9-4374-9719-d841ff339b38)

---

### **Step 5: Configure S3 Trigger**  
1. In the Lambda function, go to **Configuration** → **Triggers** → **Add Trigger**.  
2. Select **S3**.  
   - **Bucket**: `input-csv-files`  
   - **Event Type**: `All object create events` (or `Put`)  
   - **Prefix**: Optional (e.g., `raw/` to only process files in `raw/` folder).  
3. Click **Add**.  

![image](https://github.com/user-attachments/assets/bfa2bd58-6173-43ca-8eb4-c3328b30379b)

---

### **Step 6: Test with a Sample CSV**  
#### **Sample CSV (`employees.csv`)**  
```csv
id,name,department
1,john doe,IT
2,jane smith,HR
3,alex brown,Finance
```
**Upload to S3**:  
1. Go to `input-csv-files` bucket → **Upload** → Select `employees.csv`.  
2. Lambda will trigger automatically.  

![image](https://github.com/user-attachments/assets/311099e4-b223-4a67-9200-1dbc7e59502a)


#### **Expected Processed Output**  
Check `processed-csv-files` bucket for `processed_employees.csv`:  
```csv
id,name,department
1,JOHN DOE,IT
2,JANE SMITH,HR
3,ALEX BROWN,Finance
``` 
![image](https://github.com/user-attachments/assets/cb6c11ea-9025-40f5-aaf3-df4a5da92dc7)
![image](https://github.com/user-attachments/assets/09efd48f-7dd2-45ce-ae75-ef035aafc1cb)
![image](https://github.com/user-attachments/assets/b9d4658f-3135-4afc-a191-ee150d1374bc)

---

## Same configuration with EC2 , SQS and S3 without involvement of Lambda

**complete step-by-step guide** to implement the same CSV processing pipeline using **EC2** instead of Lambda, along with key differences and explanations:

---

## **Example 6: File Processing Pipeline using EC2 (Instead of Lambda)**  
### **Objective**: Process CSV files automatically when uploaded to S3 using an EC2 instance  

---

### **Key Differences: EC2 vs. Lambda**  
| Feature               | Lambda (Serverless) | EC2 (Server-based) |
|-----------------------|---------------------|--------------------|
| **Infrastructure**    | No servers to manage | Manual setup (VM) |
| **Scaling**           | Automatic           | Manual (or Auto Scaling) |
| **Cost**              | Pay per execution   | Pay per hour (always-on) |
| **Trigger**           | S3 Event Notification | S3 Event + SQS or Polling |
| **Maintenance**       | Zero                | OS updates, security patches |

---

## **Step-by-Step EC2 Implementation**  

### **Step 1: Create S3 Buckets**  
1. Go to **AWS S3 Console** → **Create Bucket**.  
   - **Bucket 1**: `input-csv-files-ec2` (for uploads)  
   - **Bucket 2**: `processed-csv-files-ec2` (for processed files)  

---

### **Step 2: Launch an EC2 Instance**  
1. Go to **EC2 Console** → **Launch Instance**.  
   - **AMI**: Amazon Linux 2023 (or Ubuntu)  
   - **Instance Type**: `t2.micro` (free tier eligible)  
   - **Key Pair**: Create/download a `.pem` key for SSH access.  
   - **Security Group**: Allow **SSH (22)** and **HTTP (80)** inbound.  
   - **IAM Role**: Attach a role with **S3 full access** (or custom policy from Lambda example).  

---

### **Step 3: Connect to EC2 and Install Dependencies**  
1. **SSH into the EC2 instance**:  
   ```bash
   ssh -i "your-key.pem" ec2-user@<EC2_PUBLIC_IP>
   ```
2. **Install Python and AWS CLI**:  
   ```bash
   sudo yum update -y
   sudo yum install python3 -y
   pip3 install boto3 awscli
   ```

---

### **Step 4: Set Up S3 Event Notifications (Using SQS)**  
Since EC2 cannot be triggered directly by S3, we use **SQS** as middleware:  

1. **Create an SQS Queue**:  
   - Go to **SQS Console** → **Create Queue** → **Standard Queue** (e.g., `csv-upload-notifications`).  
2. **Configure S3 Bucket to Send Events to SQS**:  
   - Go to **S3 Bucket** → `input-csv-files-ec2` → **Properties** → **Event Notifications**.  
   - Add a new notification:  
     - **Event Type**: `All object create events`  
     - **Destination**: `SQS Queue` → Select your queue.  

---

### **Step 5: Write the EC2 Processing Script**  
On the EC2 instance, create a Python script (`/home/ec2-user/csv_processor.py`):  
```python
import boto3
import csv
import io
import time

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
queue_url = 'YOUR_SQS_QUEUE_URL'

def process_csv(bucket, key):
    # Download CSV
    csv_file = s3.get_object(Bucket=bucket, Key=key)
    csv_content = csv_file['Body'].read().decode('utf-8')
    
    # Process CSV (uppercase 'name' column)
    reader = csv.DictReader(io.StringIO(csv_content))
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
    writer.writeheader()
    
    for row in reader:
        if 'name' in row:
            row['name'] = row['name'].upper()
        writer.writerow(row)
    
    # Upload processed file
    processed_key = f"processed_{key}"
    s3.put_object(
        Bucket='processed-csv-files-ec2',
        Key=processed_key,
        Body=output.getvalue()
    )
    print(f"Processed {key} -> saved to processed-csv-files-ec2/{processed_key}")

def poll_sqs():
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        if 'Messages' in response:
            for message in response['Messages']:
                # Parse S3 event from SQS
                s3_event = eval(message['Body'])
                bucket = s3_event['Records'][0]['s3']['bucket']['name']
                key = s3_event['Records'][0]['s3']['object']['key']
                process_csv(bucket, key)
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        time.sleep(5)

if __name__ == '__main__':
    poll_sqs()
```

---

### **Step 6: Run the Script Continuously**  
1. **Make the script executable**:  
   ```bash
   chmod +x /home/ec2-user/csv_processor.py
   ```
2. **Run it in the background** (e.g., using `tmux` or `nohup`):  
   ```bash
   tmux new -s csv-processor
   python3 /home/ec2-user/csv_processor.py
   ```
   (Press `Ctrl+B`, then `D` to detach the session.)  

---

### **Step 7: Test the Pipeline**  
1. Upload a CSV to `input-csv-files-ec2`:  
   ```bash
   aws s3 cp employees.csv s3://input-csv-files-ec2/
   ```
2. Check the processed file in `processed-csv-files-ec2`:  
   ```bash
   aws s3 ls s3://processed-csv-files-ec2/
   ```

---

### **EC2-Specific Considerations**  
1. **Always-On Cost**: EC2 runs 24/7 (unlike Lambda’s pay-per-use).  
2. **Scalability**:  
   - Use **Auto Scaling Groups** if workload increases.  
   - For high throughput, switch to **Spot Instances** or larger instance types.  
3. **Fault Tolerance**:  
   - Add **CloudWatch Alerts** to restart the script if it crashes.  
   - Use **SQS Dead-Letter Queues (DLQ)** for failed processing.  

---

### **When to Use EC2 Over Lambda**  
- **Long-running jobs** (>15 minutes, Lambda’s timeout).  
- **Custom software** (e.g., legacy apps not supported in Lambda).  
- **Persistent storage** (EC2 has local disks; Lambda has ephemeral storage).  

---

### **Final Architecture**  
```
S3 Upload → S3 Event → SQS → EC2 (Polling) → Process CSV → S3
```



## Example 7: Lambda with External API Integration

**Objective**: Call an external API from Lambda and process the response

**Steps**:
1. Create a new Lambda function named `api-caller` with Node.js runtime
2. Use this code (example with weather API):
```javascript
const https = require('https');

exports.handler = async (event) => {
    // Example: Get weather data from OpenWeatherMap API
    const apiKey = 'your-api-key'; // Replace with actual API key
    const city = event.queryStringParameters?.city || 'London';
    
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
    
    return new Promise((resolve, reject) => {
        https.get(url, (response) => {
            let data = '';
            
            response.on('data', (chunk) => {
                data += chunk;
            });
            
            response.on('end', () => {
                const weatherData = JSON.parse(data);
                
                const result = {
                    city: weatherData.name,
                    temperature: weatherData.main.temp,
                    description: weatherData.weather[0].description
                };
                
                resolve({
                    statusCode: 200,
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(result)
                });
            });
        }).on('error', (error) => {
            reject({
                statusCode: 500,
                body: JSON.stringify({ error: error.message })
            });
        });
    });
};
```
3. Create an API Gateway trigger (as in Example 3)
4. Deploy and test with query parameter: `?city=NewYork`
5. Examine the weather data in the response

**Explanation**: This shows how Lambda can integrate with external services, a common pattern for serverless applications.

## Additional Tips:
1. Always check CloudWatch logs for debugging
2. Monitor your Lambda metrics (invocations, duration, errors)
3. Consider using environment variables for configuration
4. Implement proper error handling
5. For production, use Infrastructure as Code (AWS SAM or Terraform)

These examples cover a range of common Lambda use cases from basic to more advanced integrations with other AWS services.
