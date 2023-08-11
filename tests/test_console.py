#!/usr/bin/python3
"""
test_console module
"""
import unittest
from unittest.mock import patch
from io import StringIO
from unittest import TestCase
import pycodestyle
from console import HBNBCommand
from models import storage


class TestHBNBCommand(TestCase):
    """
    TestHBNBCommand class
    """

    def test_pep(self):
        """test pep"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['console.py',
                                    'tests/test_console.py'])
        self.assertEqual(result.total_errors, 14,
                         "Found code style errors (and warnings).")

    def test_module_doc(self):
        """test module documentation"""
        doc = __import__('console').__doc__
        self.assertGreater(len(doc), 1)

    def test_class_doc(self):
        """test class documentation"""
        doc = HBNBCommand.__doc__
        self.assertGreater(len(doc), 1)

    def setUp(self):
        self.console = HBNBCommand()
        self.mock_stdout = StringIO()

    def tearDown(self):
        self.console = None

    def test_quit(self):
        with patch('sys.stdout', new=self.mock_stdout):
            self.assertTrue(HBNBCommand().onecmd("quit"))
            self.assertEqual("", self.mock_stdout.getvalue().strip())

    def test_EOF(self):
        with patch('sys.stdout', new=self.mock_stdout):
            self.assertTrue(HBNBCommand().onecmd("EOF"))
            self.assertEqual("", self.mock_stdout.getvalue().strip())

    def test_create(self):
        with patch('sys.stdout', new=self.mock_stdout):
            self.console.onecmd("create BaseModel")
            obj_id = self.mock_stdout.getvalue().strip()
            self.assertIsNotNone(storage.all().get("BaseModel." + obj_id))

    def test_show(self):
        with patch('sys.stdout', new=self.mock_stdout):
            self.console.onecmd("create BaseModel")
            obj_id = self.mock_stdout.getvalue().strip()
            self.mock_stdout = StringIO()
            self.console.onecmd("show BaseModel " + obj_id)

    def test_destroy(self):
        with patch('sys.stdout', new=self.mock_stdout):
            self.console.onecmd("create BaseModel")
            obj_id = self.mock_stdout.getvalue().strip()
            self.mock_stdout = StringIO()
            self.console.onecmd("destroy BaseModel " + obj_id)
            self.assertEqual("", self.mock_stdout.getvalue().strip())
            self.assertIsNone(storage.all().get("BaseModel." + obj_id))


if __name__ == '__main__':
    unittest.main()
