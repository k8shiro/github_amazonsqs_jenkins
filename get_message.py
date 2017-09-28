# -*- coding: utf-8 -*-

import boto3
import json
import ast
import requests
import os
import sys
import ConfigParser


def get_sqs_message(sqs, url, max_num):
    try:
        response = sqs.receive_message(QueueUrl=url, MaxNumberOfMessages=max_num)
    except Exception as e:
        print "=====Error====="
        print "get_sqs_message"
        print "ERROR:" + str(e)
        print "==============="
        return None

    return response


def delete_sqs_message(sqs, url, msg):
    try:
        response = sqs.delete_message(QueueUrl=url, ReceiptHandle=msg)
    except Exception as e:
        print "=====Error====="
        print "delete_sqs_message"
        print "ERROR:" + str(e)
        print "==============="
        return None

    return response


def get_github_message(response):
    body = response["Messages"][0]["Body"]
    body = json.loads(body)

    github_message={
        "repository": body["repository"]["ssh_url"],
        "brach": body["ref"].replace("refs/heads/", ""),
        "push_user": body["pusher"]["name"]
    }
    
    return github_message


def run_jenkins(url, user, token, github_message):
    response = requests.post(url, data=github_message, auth=(user,token))
    return response


if __name__ == '__main__':
    print "=======start========="

    config = ConfigParser.SafeConfigParser()
    config.read("conf.txt")

    os.environ["HTTP_PROXY"] = config.get("env", "http_proxy")
    os.environ["HTTPS_PROXY"] = config.get("env", "https_proxy")
    os.environ["no_proxy"] = config.get("env", "no_proxy")


    sqs = boto3.client('sqs')
    sqs_url = config.get("amazon_sqs", "url")
    get_msg_response = get_sqs_message(sqs, sqs_url, 1)
    print get_msg_response
    if "Messages" not in get_msg_response:
        print "No Messages"
        sys.exit()
    
    github_message = get_github_message(get_msg_response)
    print github_message

    
    jenkins_url = config.get("jenkins", "url")
    jenkins_api_token = config.get("jenkins", "api_token")
    jenkins_user = config.get("jenkins", "user")
    jenkins_response = run_jenkins(jenkins_url,
                                   jenkins_user,
                                   jenkins_api_token,
                                   github_message)
    print jenkins_response.text
    

    receipt_handle = get_msg_response["Messages"][0]["ReceiptHandle"]
    del_sqs_response = delete_sqs_message(sqs, sqs_url, receipt_handle)
    print del_sqs_response

    print "==========end============="
