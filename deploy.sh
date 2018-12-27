#!/bin/bash
if [ "$TRAVIS_BRANCH" == "master" ]; then
    echo $'TELEGRAM_TOKEN: ${TELEGRAM_TOKEN}\nCONTRI_API: ${CONTRI_API}' > serverless.env.yml
    serverless config credentials --provider aws --key ${aws_access_key_id} --secret ${aws_secret_access_key} --profile iam-aws
    sls deploy
fi
