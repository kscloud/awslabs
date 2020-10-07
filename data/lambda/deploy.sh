#!/bin/bash

rm lambda_mysql_loader.zip || true
cd package
zip -r9 ${OLDPWD}/lambda_mysql_loader.zip .
cd ..
zip -g lambda_mysql_loader.zip lambda_mysql_loader.py
