#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function in the utils module.
This module contains test cases to verify the correct behavior of
nested dictionary access functionality.
"""

import unittest
from utils import access_nested_map
from parameterized import parameterized
from typing import Mapping, Sequence, Any


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


if __name__ == "__main__":
    unittest.main()
