#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:eugene.20041108135942.1:@thin tests/testItem.py
#@@first
#@@first
#@@language python
#@<<testItem declarations>>
#@+node:eugene.20041108140104:<< testItem declarations >>
import sys
sys.path.append('..')

from snakememory import Item
import datetime
from unittest import TestCase, TestSuite, makeSuite
#@nonl
#@-node:eugene.20041108140104:<< testItem declarations >>
#@nl
#@+others
#@+node:eugene.20041108141556:class ItemTestCase
class ItemTestCase(TestCase):
    #@    @+others
    #@+node:eugene.20041108141556.1:testInit
    def testInit(self):
        item = Item('question', 'answer')
        self.assertEqual(item.question, 'question')
        self.assertEqual(item.answer, 'answer')
        
        today = datetime.date.today()
        self.assertEqual(item.creation_date, today)
        item.creation_date = '2004-01-01'
        self.assertEqual(item.creation_date, datetime.date(2004, 1, 1))
        try:
            item.creation_date = ''
        except ValueError:
            pass
        else:
            self.fail("Invalid value wasn't detected")
        try:
            item.creation_date = (2004, 1, 1)
        except ValueError:
            pass
        else:
            self.fail("Invalid value wasn't detected")
        
        self.assertEqual(item.start_date, today)
        item.start_date = '2004-01-01'
        self.assertEqual(item.start_date, datetime.date(2004, 1, 1))
        try:
            item.start_date = ''
        except ValueError:
            pass
        else:
            self.fail("Invalid value wasn't detected")
        try:
            item.start_date = (2004, 1, 1)
        except ValueError:
            pass
        else:
            self.fail("Invalid value wasn't detected")
    
        self.assertEqual(item.efficiency, [2.5])
        item.efficiency = [2.5, 1.3]
        self.assertEqual(item.efficiency, [2.5, 1.3])
        item.efficiency = ' 5,4, 3.1 '
        self.assertEqual(item.efficiency, [5, 4, 3.1])
        item.efficiency = ''
        self.assertEqual(item.efficiency, [2.5])
    
        try:
            item.efficiency = 'invalid'
        except ValueError:
            pass
        else:
            self.fail("Invalid value wasn't detected")
        try:
            item.efficiency = (2, 1)
        except ValueError:
            pass
        else:
            self.fail("Invalid value wasn't detected")
        
    #@nonl
    #@-node:eugene.20041108141556.1:testInit
    #@-others
#@nonl
#@-node:eugene.20041108141556:class ItemTestCase
#@+node:eugene.20041108140415:test_suite
def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(ItemTestCase))
    return suite
#@nonl
#@-node:eugene.20041108140415:test_suite
#@+node:eugene.20041108140326:main
def main():
    import unittest
    unittest.main()
#@nonl
#@-node:eugene.20041108140326:main
#@-others
if __name__ == '__main__':
    main()
#@-node:eugene.20041108135942.1:@thin tests/testItem.py
#@-leo
