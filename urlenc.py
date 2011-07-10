# -*- coding: utf-8 -*-

import base64

def encode(s):
    return base64.b64encode(s).replace('+','-').replace('/','_')

def decode(s):
    m = s.replace('-','+').replace('_','/')
    return base64.b64decode(m)
