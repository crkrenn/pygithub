#!/usr/bin/env python

import sys
import json

import requests
import yaml

# read credentials
with open("github_creds.yaml") as file:
    github_creds = yaml.safe_load(file)
github_user = github_creds["GITHUB_USER"]
github_auth = (github_user, github_creds["GITHUB_CREDS"])
github_api = "https://api.github.com"

# list workflows; find id for "E2E Tests"
owner = "crkrenn"
repo = "polis"    
r = requests.get(f'{github_api}/repos/{owner}/{repo}/actions/workflows', auth=github_auth)
result = r.json()
for item in result["workflows"]:
    print(f'{item["id"]}: {item["name"]}')
    if item["name"] == "E2E Tests":
        workflow_id_e2e = item["id"]

# run E2E workflow
user = "crkrenn"
repo = "polis"
workflow_id = workflow_id_e2e
branch_ref = "dev-for-ci-test"

url = f"{github_api}/repos/{user}/{repo}/actions/workflows/{workflow_id}/dispatches"
payload = {
    'ref': branch_ref,
}

if False:
    r = requests.post(url, data=json.dumps(payload), auth=github_auth)
    print(r.status_code)
    print(r.text)

# show results for workflows    
owner = "crkrenn"
repo = "polis"
workflow_id = workflow_id_e2e
branch_ref = "dev-for-ci-test"

url = f"{github_api}/repos/{owner}/{repo}/actions/runs"
r = requests.get(url, auth=github_auth)
# print(r.text)
json = r.json()
print(json["workflow_runs"][0].keys())
for item in json["workflow_runs"][:5]:
    print(f'{item["id"]}: {item["name"]} {item["status"]} {item["conclusion"]} {item["head_branch"]}')
    if item["name"] == "E2E Tests":
        workflow_id_e2e = item["id"]



