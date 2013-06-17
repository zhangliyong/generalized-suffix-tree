#!/usr/bin/env python

from gst import GST
import unittest


class GSTTest(unittest.TestCase):

    def test_normal(self):
        text = 'abcabcd'
        gst_obj = GST()
        gst_obj.add_text(text, 0)
        gst_obj.traverse(text)

    #@unittest.skip("")
    def test_two_text(self):
        text = "abc_ccc"
        gst_obj = GST()
        for index, t in enumerate(text.split('_')):
            gst_obj.add_text(t, index)
        gst_obj.traverse(text)

    def test_explicit_end(self):
        text = "ababa"
        gst_obj = GST()
        gst_obj.add_text(text, 0)
        gst_obj.traverse(text)

    def test_implicit_end(self):
        text = "c_aa"
        gst_obj = GST()
        for index, t in enumerate(text.split('_')):
            gst_obj.add_text(t, index)
        gst_obj.traverse(text)
