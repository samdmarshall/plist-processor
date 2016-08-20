# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/plist-processor
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import re
import os
from ..Helpers.Switch import Switch

def extractKey(value_string):
    return value_string[2:-1]

def findAndSubKey(value_string):
    results = re.finditer(r'\$[\(|\{]\w*[\)|\}]', value_string)
    new_value = ''
    offset = 0
    for item in results:
        key_name = extractKey(item.group())
        if key_name in list(os.environ.keys()):
            value = os.environ.get(key_name, '')
            new_value += value_string[offset:item.start()] + value
        offset = item.end()
    new_value += value_string[offset:]
    return new_value

def processDictionary(dict_object):
    for key in dict_object:
        value = dict_object[key]
        for case in Switch(type(value)):
            if case(str):
                dict_object[key] = findAndSubKey(value)
                break
            if case(list):
                for index in range(0, len(value)):
                    dict_object[key][index] = findAndSubKey(value[index])
                break
            if case(dict):
                dict_object[key] = processDictionary(value)
                break
            if case():
                break
    return dict_object

class Processor(object):
    def __init__(self, obj):
        self.object = obj

    def process(self):
        processDictionary(self.object.root)         

    def write(self, file_path):
        self.object.write(file_path)
