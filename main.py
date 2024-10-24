#!/usr/bin/env python
# coding: utf-8

from func import * 

a = os.environ['CONSUMER_KEY']
b = os.environ['CONSUMER_SECRET']
c = os.environ['ACCESS_TOKEN']
d = os.environ['ACCESS_TOKEN_SECRET']

print(
str(a), 
str(b), 
str(c), 
str(d), 
sep = '\n' 
)

if __name__ == "__main__":
   post_date()
