#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:eugene.20041108144653:@thin tests/testall.py
#@@first
#@@first
#@@language python
#@<<testall declarations>>
#@+node:eugene.20041108144653.1:<< testall declarations >>
import unittest

MODULES = ('Item', 'SnakeStore')
#@-node:eugene.20041108144653.1:<< testall declarations >>
#@nl
#@+others
#@+node:eugene.20041108144653.2:suite
def suite():
    alltests = unittest.TestSuite()
    for modname in MODULES:
        mod = __import__('test' + modname)
        alltests.addTest(mod.test_suite())
    return alltests
    
#@-node:eugene.20041108144653.2:suite
#@+node:eugene.20041108144748:main
def main():
    import os, sys
    sys.path.append('..')
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(tests_dir)
    unittest.main(defaultTest='suite')
#@-node:eugene.20041108144748:main
#@-others
if __name__ == '__main__':
    main()
#@-node:eugene.20041108144653:@thin tests/testall.py
#@-leo
