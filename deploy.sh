#!/bin/bash
if [ "$TRAVIS_BRANCH" == "master" ]; then
    echo "TELEGRAM_TOKEN: ${TELEGRAM_TOKEN}" >> serverless.env.yml
    echo "CONTRI_API: ${CONTRI_API}" >> serverless.env.yml
    echo "GH_API: ${GH_API}" >> serverless.env.yml
    serverless config credentials --provider aws --key ${AWS_ACCESS_KEY_ID} --secret ${AWS_SECRET_ACCESS_KEY}
    sls deploy
fi
