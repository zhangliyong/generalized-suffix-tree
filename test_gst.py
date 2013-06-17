#!/usr/bin/env python

from gst import GST
import unittest


class GSTTest(unittest.TestCase):

    def test_normal(self):
        text = 'abcabcd'
        gst_obj = GST()
        gst_obj.add_text(text, 0)
        gst_obj.traverse(text)

        self.assertEqual(list(gst_obj.search('c')), [0])
        self.assertEqual(list(gst_obj.search('abcd')), [0])
        self.assertEqual(list(gst_obj.search('abcc')), [])

    #@unittest.skip("")
    def test_two_text(self):
        text = "abc_ccc"
        gst_obj = GST()
        for index, t in enumerate(text.split('_')):
            gst_obj.add_text(t, index)
        gst_obj.traverse(text)

        self.assertEqual(list(gst_obj.search('c')), [0, 1])
        self.assertEqual(list(gst_obj.search('cc')), [1])
        self.assertEqual(list(gst_obj.search('bc')), [0])
        self.assertEqual(list(gst_obj.search('d')), [])

    def test_explicit_end(self):
        text = "ababa"
        gst_obj = GST()
        gst_obj.add_text(text, 0)
        gst_obj.traverse(text)

        self.assertEqual(list(gst_obj.search('c')), [])
        self.assertEqual(list(gst_obj.search('aba')), [0])

    def test_implicit_end(self):
        text = "c_aa"
        gst_obj = GST()
        for index, t in enumerate(text.split('_')):
            gst_obj.add_text(t, index)
        gst_obj.traverse(text)

        self.assertEqual(list(gst_obj.search('c')), [0])
        self.assertEqual(list(gst_obj.search('ca')), [])
        self.assertEqual(list(gst_obj.search('aa')), [1])
        self.assertEqual(list(gst_obj.search('d')), [])
