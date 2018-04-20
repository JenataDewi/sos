#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import shutil
import subprocess
import unittest
from argparse import Namespace

from sos.converter import (extract_workflow, script_to_html,
                           script_to_markdown, script_to_term)
from sos.utils import env


class TestConvert(unittest.TestCase):
    def setUp(self):
        env.reset()
        if not os.path.isdir('temp'):
            os.mkdir('temp')
        with open('temp/script1.sos', 'w') as script:
            script.write('''
[0]
seq = range(3)
input: for_each='seq'
output: "test${_seq}.txt"
print(output)
''')
        with open('temp/script2.sos', 'w') as script:
            # with tab after run:
            script.write('''
[0]
seq = range(3)
input: for_each='seq'
output: "test${_seq}.txt"
run:			concurrent=True
    echo 'this is test script'

[10]
report('this is action report')
''')
        self.scripts = ['temp/script1.sos', 'temp/script2.sos']

    def tearDown(self):
        shutil.rmtree('temp')

    def testScriptToHtml(self):
        '''Test sos show script --html'''
        for script_file in self.scripts:
            script_to_html(script_file, script_file + '.html')
            args = Namespace()
            args.linenos = True
            args.raw = None
            args.view = False
            script_to_html(script_file, script_file + '.html', args=args)
            #
            self.assertEqual(subprocess.call(['sos', 'convert', script_file, '--to', 'html']), 0)

    def testScriptToMarkdown(self):
        '''Test sos show script --markdown'''
        for script_file in self.scripts:
            script_to_markdown(script_file, script_file + '.md', [])

    def testScriptToTerm(self):
        '''Test sos show script --html'''
        args = Namespace()
        for script_file in self.scripts:
            script_to_term(script_file, None, args=args)

    def testExtractWorkflow(self):
        '''Test extract workflow from ipynb file'''
        content = extract_workflow('sample_workflow.ipynb')
        self.assertEqual(content, '''\
#!/usr/bin/env sos-runner
#fileformat=SOS1.0

[global]
a = 1

[default]
print(f'Hello {a}')

''')


if __name__ == '__main__':
    #suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestConvert)
    # unittest.TextTestRunner().run(suite)
    unittest.main()
