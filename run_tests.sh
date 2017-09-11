#!/usr/bin/env bash

# Test with both python 2 and 3

# Assuming you have py.test installed for both python2 and 3

p2dir=$(dirname $(command which python2))
${p2dir}/py.test --cov=list_dict_DB tests.py

p3dir=$(dirname $(command which python3))
${p3dir}/py.test --cov=list_dict_DB tests.py
