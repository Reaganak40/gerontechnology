#!/usr/bin/env python
#! Run This test from the parent directory or module (data wrangling) to avoid relative import errors. 
# python -m unittest -v tests.test_utils

""" Test the efficacy of the Utils class (unit tests)
"""

# * Modules
import unittest
import pandas as pd
import os
from src.data_wrangling import Utils

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class TestUtilsClass(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
    
    # Tests the the distinct filter will provide a df with only distinct entries.
    def test_distinct_filter(self):
        pre_filter = pd.read_excel(os.path.dirname(os.path.realpath(__file__)) + R"\test data\input\test_distinct_filter.xlsx")
        correct_filter = pd.read_excel(os.path.dirname(os.path.realpath(__file__)) + R"\test data\output\test_distinct_filter - after (correct).xlsx")
        post_filter = Utils.filter_to_distinct_interactions(pre_filter)
        
        post_filter = post_filter.sort_values(by=['interactionId'])
        correct_filter = correct_filter.sort_values(by=['interactionId'])

        self.assertEqual(len(post_filter), len(correct_filter))
        for index in range(len(post_filter)):
            self.assertTrue(post_filter.iloc[index].equals(correct_filter.iloc[index]))


