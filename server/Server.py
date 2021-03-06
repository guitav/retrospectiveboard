from flask import Flask, request, jsonify, abort, Response
import boto3
import json
from botocore.exceptions import ClientError
from flask_cors import CORS
from bisect import bisect_left, bisect_right
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import decimal
import os

app = Flask(__name__)
CORS(app)
# Or via the Session
session = boto3.Session(
    aws_access_key_id=os.environ['AWSAccessKeyId'],
    aws_secret_access_key=os.environ['AWSSecretKey']
)
dynamodb = session.resource("dynamodb", region_name='us-east-1')
table = dynamodb.Table('SprintRetro')
ACTIVE_STATE = 'alive!'


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


@app.route('/teams')
def get_teams():
    try:
        response = table.scan()
        list_of_teams = []
        for item in response['Items']:
            if item['team_name'] not in list_of_teams:
                list_of_teams.append(item['team_name'])
    except ClientError as e:
        return(e.response['Error']['Message'])
    else:
        return ({"teams": list_of_teams})


@app.route('/<team>/sprint')
def get_team_sprints(team):
    try:
        response = table.scan()
        list_of_sprints = [item['sprint_no'] for item in response['Items'] if item['team_name'] == team]
    except ClientError as e:
        return(e.response['Error']['Message'])
    else:
        return jsonify(list_of_sprints)


@app.route('/<team>/<sprint_no>')
def get_all_values(team, sprint_no):
    try:
        response = table.get_item(
            Key={
                'team_name': team,
                'sprint_no': sprint_no
            }
        )
        all_values = response['Item']['category']
    except ClientError as e:
        return(e.response['Error']['Message'])
    else:
        return (json.dumps(all_values, indent=4, cls=DecimalEncoder))


@app.route('/<team>/<sprint_no>/<retro_type>/<description>')
def upvote(team, sprint_no, retro_type, description):
    print("SET category." + retro_type + ".#description = " + retro_type + ".#description + :i")
    try:
        table.update_item(
            Key={
                'team_name': team,
                'sprint_no': sprint_no
            },
            UpdateExpression="SET category." + retro_type + ".#description = category." + retro_type + ".#description + :i",
            ExpressionAttributeNames={
                '#description': description,
            },
            ExpressionAttributeValues={':i': decimal.Decimal(1)}
        )
    except ClientError as e:
        return (e.response['Error']['Message'])
    else:
        return "Increase vote"


@app.route('/post/<team>/<sprint_no>/<retro_type>/<description>')
def insert_description(team, sprint_no, retro_type, description):
    try:
        table.update_item(
            Key={
                'team_name': team,
                'sprint_no': sprint_no
            },
            UpdateExpression="SET category." + retro_type + ".#description =:i",
            ExpressionAttributeNames={
                '#description': description,
            },
            ExpressionAttributeValues={':i': decimal.Decimal(0)}
        )
    except ClientError as e:
        return (e.response['Error']['Message'])
    else:
        return "Inserted Description"


@app.route('/post/<team>/<sprint_no>')
def insert_team(team, sprint_no):
    try:
        response = table.put_item(
            Item={
                'team_name': team,
                'sprint_no': sprint_no,
                'category': {'well': {}, 'bad': {}, 'todo': {}}
            }
        )
    except ClientError as e:
        return (e.response['Error']['Message'])
    else:
        return "Inserted Team"


@app.route('/')
def get_pulse():
    return 'alive'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
