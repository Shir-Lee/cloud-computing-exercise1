import json
import pulumi
import pulumi_aws as aws
import pulumi_aws_apigateway as apigateway

# execution role to use for the lambda function

assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com",
            },
        }],
    })

policy_db = aws.iam.Policy("policy_db",
    name="policy_db",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": [
		"dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Effect": "Allow",
            "Resource": "*",
        }],
    }))


role = aws.iam.Role("role",
    name="role",
    assume_role_policy= assume_role_policy,
    managed_policy_arns=[
        aws.iam.ManagedPolicy.AWS_LAMBDA_BASIC_EXECUTION_ROLE,
        policy_db.arn,
    ])

# entry lambda function 
entry_fn = aws.lambda_.Function("entry_fn",
    runtime="python3.9",
    handler="entry_handler.lambda_handler",
    role=role.arn,
    code=pulumi.FileArchive("./function"))

entry_api = apigateway.RestAPI("entry_api",
  routes=[
    apigateway.RouteArgs(path="/entry", method=apigateway.Method.POST, event_handler=entry_fn)
  ])

# exit lambda function 
exit_fn = aws.lambda_.Function("exit_fn",
    runtime="python3.9",
    handler="exit_handler.lambda_handler",
    role=role.arn,
    code=pulumi.FileArchive("./function"))

exit_api = apigateway.RestAPI("exit_api",
  routes=[
    apigateway.RouteArgs(path="/exit", method=apigateway.Method.POST, event_handler=exit_fn)
  ])

# DB
table = aws.dynamodb.Table("parking_app_table",
    name="parking_app_table",
    billing_mode="PROVISIONED",
    read_capacity=1,
    write_capacity=1,
    hash_key="id",
    attributes=[
        aws.dynamodb.TableAttributeArgs(name="id", type="S"),
    ])

# URL at which the REST API will be served.
pulumi.export("entry_url", entry_api.url)
pulumi.export("exit_url", exit_api.url)


