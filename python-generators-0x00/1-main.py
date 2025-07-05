#!/usr/bin/env python3

import importlib
module = importlib.import_module('0-stream_users')
stream_users = module.stream_users

# Rest of your code here
for user in stream_users():
    print(user)