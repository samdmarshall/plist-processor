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
import sys
import string
import pbPlist
import unittest
import itertools
import plistprocessor

test_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')

def LoadTestDirectoryAndTestWithName(test, path_subdir, test_file_name):
    test_path = os.path.join(test_directory, path_subdir)
    test_input_path = os.path.join(test_path, test_file_name+'.plist')
    test_generated_output = os.path.join(test_path, test_file_name+'_output.plist')
    test_expected_output = os.path.join(test_path, test_file_name+'_expected.plist')
    args = ['--input', test_input_path, '--output', test_generated_output]
    plistprocessor.main(args)
    generated_output = pbPlist.pbPlist.PBPlist(test_generated_output)
    expected_output = pbPlist.pbPlist.PBPlist(test_expected_output)
    test.assertEqual(len(generated_output.root), len(expected_output.root))

class plistProcessorTestCases(unittest.TestCase):

    def test_xml(self):
        LoadTestDirectoryAndTestWithName(self, 'xml', 'test')

    def test_ascii(self):
        LoadTestDirectoryAndTestWithName(self, 'ascii', 'test')

    def test_binary(self):
        LoadTestDirectoryAndTestWithName(self, 'binary', 'test')

if __name__ == '__main__':
    unittest.main()