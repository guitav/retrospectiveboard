from flask import Flask, request, jsonify, abort, Response
import config
import boto3
import json
from botocore.exceptions import ClientError
from flask_cors import CORS
from bisect import bisect_left, bisect_right
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app)
dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
table = dynamodb.Table('SprintRetro')
ACTIVE_STATE = 'alive!'


@app.route('/teams')
def get_teams():
    try:
        response = table.scan()

        list_of_teams = []

        for item in response['Items']:
            if item['team_name'].encode('utf-8') not in list_of_teams:
                list_of_teams.append(item['team_name'].encode('utf-8'))

    except ClientError as e:
        print(e.response['Error']['Message'])

    else:
        # return jsonify(lst)
        return jsonify(list_of_teams)


@app.route('/<team>/sprint')
def get_team_sprints(team):
    try:
        response = table.scan()

        list_of_sprints = [item['sprint_no'].encode('utf-8') for item in response['Items'] if item['team_name'].encode('utf-8') == team]

    except ClientError as e:
        print(e.response['Error']['Message'])

    else:
        return jsonify(list_of_sprints)


@app.route('/<team>/<sprint_no>/well')
def get_sprint_good(team, sprint_no):
    try:
        response = table.scan()

        the_good = [item['well'] for item in response['Items']
                    if item['team_name'].encode('utf-8') == team and
                    item['sprint_no'].encode('utf-8') == sprint_no
                    if 'well' in item]

    except ClientError as e:
        print(e.response['Error']['Message'])

    else:
        return jsonify(the_good)


@app.route('/<team>/<sprint_no>/bad')
def get_sprint_bad(team, sprint_no):
    try:
        response = table.scan()

        the_bad = [item['bad'] for item in response['Items']
                   if item['team_name'].encode('utf-8') == team and item['sprint_no'].encode('utf-8') == sprint_no
                   if 'bad' in item]

    except ClientError as e:
        print(e.response['Error']['Message'])

    else:
        return jsonify(the_bad)


@app.route('/<team>/<sprint_no>/action')
def get_sprint_action(team, sprint_no):
    try:
        response = table.scan()

        the_action = [item['action'] for item in response['Items']
                      if item['team_name'].encode('utf-8') == team and item['sprint_no'].encode('utf-8') == sprint_no
                      if 'action' in item]

    except ClientError as e:
        print(e.response['Error']['Message'])

    else:
        return jsonify(the_action)


def put_well(team, sprint_no, well):
    try:
        table.put_item(
            Item={
                'team_name': team,
                'sprint_no': sprint_no,
                'well': well
            }
        )
    except Exception as e:
        print(e.response['Error']['Message'])


@app.route('/')
def get_pulse():
    return 'hey'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.PORT_NUMBER, debug=True)
