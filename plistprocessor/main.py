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

import sys
import pbPlist
import argparse
from .version             import __version__ as PLIST_PROCESSOR_VERSION
from .Processor           import Environment

# Main
def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='plist-processor is a tool to substitute environment variables into plist files')
    parser.add_argument(
        '--version',
        help='Displays the version information',
        action='version',
        version=PLIST_PROCESSOR_VERSION
    )
    parser.add_argument(
        '-i',
        '--input',
        metavar='<input path>',
        help='specify the path to the pre-processed plist file',
        required=True,
        action='store'
    )
    parser.add_argument(
        '-o',
        '--output',
        metavar='<output path>',
        help='specify the path to write the processed plist file',
        required=True,
        action='store'
    )

    args = parser.parse_args(argv)

    has_input = args.input is not None
    has_output = args.output is not None
    if has_input and has_output:
        plist_obj = pbPlist.pbPlist.PBPlist(args.input)

        pre_processor = Environment.Processor(plist_obj)

        pre_processor.process()

        pre_processor.write(args.output)

if __name__ == "__main__": # pragma: no cover
    main()