#!/bin/sh

# Fail script if any command fails
set -e

# Push code coverage to gh-pages
./tools/coverage_to_gh_pages.sh

# Decrypt secrets
./tools/secure_data.py decrypt -k $SALT_SECRET

# Configure SSH keys for travis-ci user
python -c "import yaml; fh = open('pillar/secure/init.sls'); d = yaml.load(fh); print d['TRAVIS_SSH_PRIVATE_KEY']" > ~/.ssh/id_rsa

# Run provisioning on server and deploy code and static assets to server
fab provision deploy -H travis-ci@koosli.org:21890
