#!/usr/bin/env python3
"""
Unit tests for the client.py
"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch


class TestGithubOrgClient(unittest.TestCase):
    """Testing  GithubOrgClient.org"""
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get):
        """Test org methof of GithubOrgClient
        Args:
        org_name: str org name
        """
        test_payload = {"status": 1}
        mock_get.return_value = test_payload
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, test_payload)
        expected_url = GithubOrgClient.ORG_URL.format(org=org_name)
        mock_get.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
