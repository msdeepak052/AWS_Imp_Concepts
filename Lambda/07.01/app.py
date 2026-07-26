import platform

def lambda_handler(event, context):
    name = event.get("name", "World")
    message = f"Hello, {name}! This response came from a CONTAINER IMAGE running Python {platform.python_version()}."
    print(f"Container image invoked for: {name}")   # shows up in CloudWatch Logs, same as any other function

    return {
        "statusCode": 200,
        "body": message
    }