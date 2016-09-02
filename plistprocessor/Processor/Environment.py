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

import os
import re
import pbPlist
from ..Helpers.Switch           import Switch

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

def references(iterable):
    try:
        return iterable.keys()
    except AttributeError:
        return range(len(iterable))

class Processor(object):

    def __init__(self, plist_object):
        self.plist = plist_object

    def convertToWriteable(self, value):
        writeable_type = value
        for case in Switch(self.plist.file_type):
            if case('ascii'):
                type_name = None
                for case in Switch(type(value)):
                    if case(dict):
                        type_name = 'dictionary'
                        value = pbPlist.pbRoot.pbRoot(value)
                        break
                    if case(list):
                        type_name = 'array'
                        break
                    if case():
                        type_name = 'qstring'
                        break
                if type_name is not None:
                    writeable_type = pbPlist.pbItem.pbItemResolver(value, type_name)
                break
            if case('binary'):
                break
            if case('xml'):
                break
            if case():
                break
        return writeable_type

    def process(self):
        native_types_plist = None
        for case in Switch(self.plist.file_type):
            if case('ascii'):
                native_types_plist = self.plist.root.nativeType()
                break
            if case():
                try:
                    self.plist.root.keys()
                    native_types_plist = dict(self.plist.root)
                except AttributeError:
                    native_types_plist = list(self.plist.root)
                break
        root_object_type = type(native_types_plist)
        new_root_object = root_object_type()
        for ref in references(native_types_plist):
            item, value = self.processItemOfObject(ref, native_types_plist)
            for case in Switch(root_object_type):
                if case(dict):
                    new_root_object[item] = value
                    break
                if case(list):
                    new_root_object.append(value)
                    break
                if case():
                    break
        
        self.plist.root = self.convertToWriteable(new_root_object)

    def processItemByType(self, item):
        for case in Switch(type(item)):
            if case(dict):
                item = dict([self.processItemOfObject(ref, item) for ref in references(item)])
                break
            if case(list):
                item = [self.processItemOfObject(ref, item)[1] for ref in references(item)]
                break
            if case():
                item = findAndSubKey(item)
                break
        return item

    def processItemOfObject(self, item, container):
        value = container[item]
        value = self.processItemByType(value)
        
        item = self.convertToWriteable(item)
        value = self.convertToWriteable(value)
        
        return (item, value)

    def write(self, output_path):
        self.plist.write(output_path)