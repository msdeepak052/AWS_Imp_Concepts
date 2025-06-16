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

1. **Set up your local environment** (Linux recommended, or use AWS CloudShell):
   ```bash
   mkdir pillow_layer
   cd pillow_layer
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Pillow in a specific directory**:
   ```bash
   mkdir python
   pip install pillow -t python/
   ```

3. **Zip the layer contents**:
   ```bash
   zip -r pillow_layer.zip python
   ```

4. **Create the Lambda Layer**:
   - Go to AWS Lambda Console → **Layers** → **Create layer**
   - Name: `pillow-layer`
   - Upload your `pillow_layer.zip` file
   - Select compatible runtimes (Python 3.8, 3.9, etc.)
   - Click **Create**

5. **Attach the Layer to your Lambda**:
   - Open your `image-processor` Lambda function
   - Scroll to **Layers** section → Click **Add a layer**
   - Choose **Custom layers** → Select `pillow-layer`
   - Click **Add**

---


### **Key Notes:**
1. **Layer vs. Deployment Package**:
   - Layers are reusable across multiple Lambdas.
   - Deployment packages are self-contained but larger.

2. **AWS Limits**:
   - Deployment package (unzipped) must be under **250MB**.
   - Layers (unzipped) can be up to **250MB total** (max 5 layers per Lambda).

3. **ARM vs. x86**:
   - If your Lambda uses **ARM/Graviton**, install Pillow on an ARM machine or use AWS CloudShell (which runs on x86).

4. **Alternative**:
   - Use the **AWS Lambda Powertools** layer if you need additional Python utilities.

Let me know if you'd like me to elaborate on any step!

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
6. Configure S3 trigger in Lambda:
   - In Lambda console, go to "Add trigger"
   - Select S3
   - Choose your bucket
   - Event type: "All object create events"
   - Prefix: "uploads/" (optional)
7. Test by uploading an image to your S3 bucket

**Explanation**: This demonstrates event-driven architecture where Lambda responds to S3 events. The function processes the image and creates a thumbnail version.

## Example 3: API Gateway Integration (REST API)

**Objective**: Create a Lambda-powered REST API with API Gateway

**Steps**:
1. Create a new Lambda function named `api-example` with Node.js runtime
2. Use this code:
```javascript
exports.handler = async (event) => {
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
3. In API Gateway console, create a new REST API
4. Create a resource (e.g., `/hello`)
5. Create a GET method and connect it to your Lambda function
6. Deploy the API to a stage (e.g., "prod")
7. Test the endpoint using the provided URL

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

## Example 6: Serverless File Processing Pipeline

**Objective**: Process CSV files with Lambda and S3

**Steps**:
1. Create two S3 buckets: `input-csv-files` and `processed-csv-files`
2. Create a Lambda function named `csv-processor` with Python runtime
3. Add S3 read/write permissions to the Lambda's execution role
4. Use this code:
```python
import boto3
import csv
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the uploaded CSV file
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download the CSV
    csv_file = s3.get_object(Bucket=bucket, Key=key)
    csv_content = csv_file['Body'].read().decode('utf-8')
    
    # Process CSV
    reader = csv.DictReader(io.StringIO(csv_content))
    
    # Example: Convert all names to uppercase
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
    writer.writeheader()
    
    for row in reader:
        row['name'] = row['name'].upper()  # Assuming there's a 'name' column
        writer.writerow(row)
    
    # Upload processed CSV
    s3.put_object(
        Bucket='processed-csv-files',
        Key=f"processed_{key}",
        Body=output.getvalue()
    )
    
    return {
        'statusCode': 200,
        'body': 'CSV processed successfully!'
    }
```
5. Configure S3 trigger for the input bucket
6. Test by uploading a CSV file to the input bucket
7. Check the processed bucket for the transformed file

**Explanation**: This demonstrates a common ETL (Extract, Transform, Load) pattern using serverless components.

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
