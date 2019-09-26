#!/usr/bin/env bash

cd $(dirname $0)
echo "Generating help page"

aeroframe -h > user_guide/_help_page.txt
