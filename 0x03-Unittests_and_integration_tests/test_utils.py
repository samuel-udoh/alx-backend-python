#!/usr/bin/env python3
"""
Unit tests for the utils.py
"""

import unittest
from unittest.mock import patch
import utils
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict


class TestAccessNestedMap(unittest.TestCase):
    """
    Test cases for the access_nested_map function.

    This class contains test methods to verify that access_nested_map
    retrieves values from nested dictionaries using a sequence of keys.
    """

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2)
    ])
    def test_access_nested_map(
            self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """
        Test access_nested_map returns the expected value for valid inputs.

        Args:
            nested_map: A nested dictionary to test
            path: Sequence of keys to access the nested value
            expected: The expected value to be returned
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ["a"]),
        ({"a": 1}, ["a", "b"])
    ])
    def test_access_nested_map_exception(
            self, nested_map: Mapping, path: Sequence) -> None:
        """
        Test access_nested_map_ returns KeyError for invalid inputs.

        Args:
            nested_map: A nested dictionary to test
            path: Sequence of keys to access the nested value
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """This is the Test case for get_json
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("utils.requests.get")
    def test_get_json(
            self, test_url: str, test_payload: Dict, mock_get) -> None:
        """
        Test get_json returns json when input is valid.

        Args:
            test_url: str of url path
            test_payload: JSON to be return
        """
        mock_response = mock_get.return_value
        mock_response.json.return_value = test_payload

        response = get_json(test_url)

        self.assertEqual(response, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests the memoize decorator."""
    def test_memoize(self):
        """
        Tests that a memoized property calls its underlying method only once.
        """

        class TestClass:
            """Test Class"""
            def a_method(self):
                """This is the memoized property."""
                return 42

            @memoize
            def a_property(self):
                """This is the memoized property."""
                return self.a_method()
        with patch.object(TestClass, "a_method") as mock_a_method:
            mock_a_method.return_value = 42
            instance = TestClass()
            result1 = instance.a_property
            result2 = instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
