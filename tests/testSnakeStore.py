#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:eugene.20041108152153:@thin tests/testSnakeStore.py
#@@first
#@@first
#@@language python
#@<<testSnakeStore declarations>>
#@+node:eugene.20041108152221:<< testSnakeStore declarations >>
import sys
sys.path.append('..')

from snakememory import SnakeStore
import datetime
from unittest import TestCase, TestSuite, makeSuite
#@nonl
#@-node:eugene.20041108152221:<< testSnakeStore declarations >>
#@nl
#@+others
#@+node:eugene.20041108152444:class SnakeStoreTestCase
class SnakeStoreTestCase(TestCase):
    #@    @+others
    #@+node:eugene.20041108152918:testInit
    def testInit(self):
        store = SnakeStore('cards.xml')
        store.load()
        items = store.get_items_store()
        
        iter = items.get_iter((0,))
        question = items.get_value(iter, 0)
        self.assertEquals(question, 'question 1')
        item = items.get_value(iter, 1)
        self.assertEquals(item.question, 'question 1')
        self.assertEquals(item.answer, 'answer 1')
        self.assertEquals(item.creation_date, datetime.date(1999, 1, 1))
        self.assertEquals(item.efficiency, [1.0, 1.1])
        
        iter = items.get_iter((1, 0, 0))
        question = items.get_value(iter, 0)
        self.assertEquals(question, 'child of child of question 2')
        item = items.get_value(iter, 1)
        self.assertEquals(item.question, question)
        self.assertEquals(item.answer, 'haizi')
        self.assertEquals(item.creation_date, datetime.date(2004, 11, 7))
        self.assertEquals(item.efficiency, [2.5])
        try:
            # scheuled_date is never loaded -- it is computed
            print item.scheduled_date
        except AttributeError:
            pass
        else:
            self.fail("Missing attribute wasn't detected")
    
    #@-node:eugene.20041108152918:testInit
    #@-others
#@nonl
#@-node:eugene.20041108152444:class SnakeStoreTestCase
#@+node:eugene.20041108152411:test_suite
def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(SnakeStoreTestCase))
    return suite
#@nonl
#@-node:eugene.20041108152411:test_suite
#@+node:eugene.20041108152353:main
def main():
    import unittest
    unittest.main()
#@nonl
#@-node:eugene.20041108152353:main
#@-others
if __name__ == '__main__':
    main()
#@-node:eugene.20041108152153:@thin tests/testSnakeStore.py
#@-leo
