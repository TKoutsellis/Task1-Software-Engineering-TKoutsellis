#fetchimages_test.py
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:02:12 2019

@author: Koutsellis Themistoklis

Description
===========

Unit test for fetchimages.fetch_images() function.

All test case scenarios should work flawlessly
regardless of the execution environment e.g. there
might exist directories with no permission rights, depending
on the computer and operating system where the tests run.

Therefore, mock input/output files will be used. To do so,
buffer binary/text stream objects will be used (io.StringIO() & io.BytesIO())
String mock objects for input txt file, img_url_file, and
binary mock object, for the image files saved to output target_path dir.

12 test case scenarios:
-----------------------

    Case 1:
        Assumption:
            A valid input img_url_file txt
            file with 3 image URLs, passed as arg.
        Expected result:
            fetch_images() terminates successfully
            returning number 3 (the number of images).

    Case 2:
        Assumption:
            A valid but empty input img_url_file txt, passed as arg.
        Expected result:
            fetch_images() terminates successfully
            returning number 0 (the number of images).

    Case 3:
        Assumption:
            Invalid input img_url_file txt, passed as arg.
            Contains only one linesep.
        Expected result:
            SystemExit

    Case 4:
        Assumption:
            Invalid input img_url_file txt, passed as arg.
            Contains contains invalid URL.
        Expected result:
            SystemExit

    Case 5:
        Assumption:
            Valid input img_url_file txt, passed as arg, but access denied.
        Expected result:
            SystemExit

    Case 6:
        Assumption:
            Input img_url_file txt, passed as arg, does not exist
        Expected result:
            SystemExit

    Case 7:
        Assumption:
            Output target_path, passed as arg, is invalid.
        Expected result:
            SystemExit

    Case 8:
        Assumption:
            Server, storing the image, denies access. Request cancelled.
        Expected result:
            SystemExit

    Case 9:
        Assumption:
            More than one target_paths, passes as arg.
        Expected result:
            SystemExit

    Case 10:
        Assumption:
            target_path arg equals to None.
        Expected result:
            SystemExit

    Case 11:
        Assumption:
            Passes arg:
                1 valid target_path.
                1 valid input img_url_file txt file with 3 image URLs.
        Expected result:
            fetch_images() terminates successfully,
            returning number 3 (the number of images).

    Case 12:
        Assumption:
            No target_path is given.
            A valid input img_url_file txt file with 3 image URLs.
        Expected result:
            fetch_images() terminates successfully,
            returning number 3 (the number of images).
"""

import io
import os
import unittest
import urllib.error
from unittest.mock import patch
from unittest.mock import Mock

import fetchimages

class TestFetchImages(unittest.TestCase):
    '''
    TestCase class to test fetchimages.fetch_images() function.
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Class level setup function.Execution
        once before all test case scenarios.
        '''
        cls.three_valid_img_urls_file = \
        ('https://i.ytimg.com/vi/Fyt6QmLtUJA/maxresdefault.jpg\n' +
         'https://i.pinimg.com/originals/56/50/e2/5650e280b7d3814bf43bed91630d1d3e.jpg\n' +
         'https://i.pinimg.com/originals/17/f6/0d/17f60d5c3de5a3ff40828efc2c267dd9.jpg\n' \
         )
        cls.empty_img_urls_file = ''
        cls.empty_img_urls_file_with_linesep = '\n'
        cls.invalid_url_txt_file = ')*$%&*'


    @classmethod
    def tearDownClass(cls):
        '''
        Class level setup function.
        Execution once after all test case scenarios.
        '''
        pass

    def setUp(self):
        '''
        Execution before every test case scenario.
        '''
        self.input_buffer = io.StringIO()
        self.output_buffer = io.BytesIO()

        self.input_buffer.seek(0)
        self.output_buffer.seek(0)

    def tearDown(self):
        '''
        Execution after every test case scenario.
        '''
        self.input_buffer.close()
        self.output_buffer.close()

    # Case 1:
    @patch('fetchimages.open', )
    def test_correct_img_url_file(self, mock_open):
        '''
        Tests fetchimages.fetch_images
        response if img_url_file is valid containing 3 image URLs.
        No target path is given.
        '''
        print('Test case 1:')
        self.input_buffer.write(TestFetchImages.three_valid_img_urls_file)
        self.input_buffer.seek(0)

        mock_file = Mock()

#        Every time fetchimages._download_image() is called,
#        the mock io.BytesIO() object is closed due to try statement.
#        Therefore, the closed io.BytesIO() cannot be reused
#        for the next iteration. For every new iteration
#        a brand new io.BytesIO() is needed. In these test case,
#        the fetchimages._download_image() is called 3 times.#
#        Therefore, below, the side_effect list contains 3 io.BytesIO() objects.
#        Similar logic, in the next case scenarios implimentation.
        mock_open.side_effect = [self.input_buffer, io.BytesIO(), io.BytesIO(), io.BytesIO()]
        self.assertEqual(fetchimages.fetch_images(mock_file), 3)

    # Case 2:
    @patch('fetchimages.open', )
    def test_empty_img_url_file(self, mock_open):
        '''
        Tests fetchimages.fetch_images
        response if img_url_file is empty.
        '''
        print('Test case 2:')
        self.input_buffer.write(TestFetchImages.empty_img_urls_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_open.side_effect = [self.input_buffer, io.BytesIO()]
        self.assertEqual(fetchimages.fetch_images(mock_file), 0)

    # Case 3:
    @patch('fetchimages.open', )
    def test_empty_img_url_file_with_linesep(self, mock_open):
        '''
        Tests fetchimages.fetch_images response
        if img_url_file only contains a linesep.
        '''
        print('Test case 3:')
        self.input_buffer.write(TestFetchImages.empty_img_urls_file_with_linesep)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_open.side_effect = [self.input_buffer, io.BytesIO()]
        with self.assertRaises(SystemExit) as ex:
            fetchimages.fetch_images(mock_file)
        self.assertEqual(ex.exception.code, 1)

    # Case 4:
    @patch('fetchimages.open', )
    def test_img_url_file_with_invalid_url(self, mock_open):
        '''
        Tests fetchimages.fetch_images response
        if img_url_file contains invalid URLs.
        '''
        print('Test case 4:')
        self.input_buffer.write(TestFetchImages.invalid_url_txt_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_open.side_effect = [self.input_buffer, io.BytesIO()]
        with self.assertRaises(SystemExit) as ex:
            fetchimages.fetch_images(mock_file)
            self.assertEqual(ex.exception.code, 1)

    # Case 5:
    @patch('fetchimages.open', )
    def test_img_url_file_with_access_denied(self, mock_open):
        '''
        Tests fetchimages.fetch_images response
        if access to img_url_file is denied.
        '''
        print('Test case 5:')
        self.input_buffer.write(TestFetchImages.invalid_url_txt_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_open.side_effect = [WindowsError]
        with self.assertRaises(SystemExit) as ex:
            fetchimages.fetch_images(mock_file)
            self.assertEqual(ex.exception.code, 1)

    # Case 6:
    @patch('fetchimages.open', )
    def test_img_url_file_does_not_exist(self, mock_open):
        '''
        Tests fetchimages.fetch_images response
        if img_url_file does not exist.
        '''
        print('Test case 6:')
        self.input_buffer.write(TestFetchImages.invalid_url_txt_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_open.side_effect = [IOError]
        with self.assertRaises(SystemExit) as ex:
            fetchimages.fetch_images(mock_file)
            self.assertEqual(ex.exception.code, 1)

    # Case 7:
    @patch('fetchimages.open', )
    def test_target_path_invalid(self, mock_open):
        '''
        Tests fetchimages.fetch_images response
        if target_path is invalid.
        '''
        print('Test case 7:')
        self.input_buffer.write(TestFetchImages.invalid_url_txt_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_open.side_effect = [self.input_buffer, io.BytesIO()]
        with self.assertRaises(SystemExit) as ex:
            fetchimages.fetch_images(mock_file, ')%%^')
            self.assertEqual(ex.exception.code, 1)

    # Case 8:
    @patch('fetchimages.urllib.request.urlopen', )
    @patch('fetchimages.open', )
    def test_url_server_access_denied(self, mock_open, mock_response):
        '''
        Tests fetchimages.fetch_images response
        if access to server denied.
        '''
        print('Test case 8:')
        self.input_buffer.write(TestFetchImages.invalid_url_txt_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_target_path = Mock()
        mock_open.side_effect = [self.input_buffer, io.BytesIO()]
        mock_response.side_effect = [urllib.error.URLError]
        with self.assertRaises(SystemExit) as ex:
            fetchimages.fetch_images(mock_file, mock_target_path)
            self.assertEqual(ex.exception.code, 1)

    # Case 9:
    @patch('fetchimages.open', )
    def test_more_than_one_target_paths(self, mock_open):
        '''
        Tests fetchimages.fetch_images response
        if more than one target_paths given.
        '''
        print('Test case 9:')
        self.input_buffer.write(TestFetchImages.invalid_url_txt_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_target_path1 = Mock()
        mock_target_path2 = Mock()
        mock_open.side_effect = [self.input_buffer, io.BytesIO()]
        with self.assertRaises(SystemExit) as ex:
            fetchimages.fetch_images(mock_file, mock_target_path1, mock_target_path2)
            self.assertEqual(ex.exception.code, 1)

    # Case 10:
    @patch('fetchimages.open', )
    def test_target_path_is_none(self, mock_open):
        '''
        Tests fetchimages.fetch_images response
        if None is passed instead of valid target_path.
        '''
        print('Test case 10:')
        self.input_buffer.write(TestFetchImages.invalid_url_txt_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_open.side_effect = [self.input_buffer, io.BytesIO()]
        with self.assertRaises(SystemExit) as ex:
            fetchimages.fetch_images(mock_file, None)
            self.assertEqual(ex.exception.code, 1)

    # Case 11:
    @patch('fetchimages.open', )
    def test_target_path_is_valid(self, mock_open):
        '''
        Tests fetchimages.fetch_images response
        if 1 valid target_path is given.
        '''
        self.input_buffer.write(TestFetchImages.three_valid_img_urls_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        test_dir = os.path.dirname(__file__)
        mock_open.side_effect = [self.input_buffer, io.BytesIO(), io.BytesIO(), io.BytesIO()]
        self.assertEqual(fetchimages.fetch_images(mock_file, test_dir), 3)

    # Case 12:
    @patch('fetchimages.open', )
    def test_target_path_not_given(self, mock_open):
        '''
        Tests fetchimages.fetch_images response
        if no target_path is given.
        '''
        print('Test case 12:')
        self.input_buffer.write(TestFetchImages.three_valid_img_urls_file)
        self.input_buffer.seek(0)

        mock_file = Mock()
        mock_open.side_effect = [self.input_buffer, io.BytesIO(), io.BytesIO(), io.BytesIO()]
        self.assertEqual(fetchimages.fetch_images(mock_file), 3)

if __name__ == '__main__':
    unittest.main()
