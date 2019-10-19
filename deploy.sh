#!/usr/bin/env bash

# lots hardcoded here...
gcloud functions deploy pul-github-reporter  \
  --source "https://source.developers.google.com/projects/pul-github-reporter/repos/pul-github-reporter" \
  --entry-point main \
  --runtime python37  \
  --trigger-topic nightly-run \
  --set-env-vars GITHUB_TOKEN=$PUL_GITHUB_TOKEN,GITHUB_ORGANIZATION=pulibrary
