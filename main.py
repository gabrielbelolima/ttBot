#!/usr/bin/env python
# coding: utf-8

from func import * 

print(
os.environ['CONSUMER_KEY'],
os.environ['CONSUMER_SECRET'],
os.environ['ACCESS_TOKEN'],
os.environ['ACCESS_TOKEN_SECRET'],
sep = '\n' 
)

if __name__ == "__main__":
   post_date()
