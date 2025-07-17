#!/usr/bin/env python3
"""
Unit tests for the client.py
"""
import unittest
from client import GithubOrgClient
import client
from parameterized import parameterized
from unittest.mock import PropertyMock, patch


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

    def test_public_repos_url(self):
        """Test the GithubOrgClient._public_repos_url"""
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) \
                as mock_repo:
            test_payload = {"repos_url": "https://example.com"}
            mock_repo.return_value = test_payload
            client = GithubOrgClient("org")
            response = client._public_repos_url
            self.assertEqual(response, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get):
        """Testing public repo method"""
        test_load = [{"name": "github"}, {"name": "github2"}]
        mock_get.return_value = test_load
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repo_url:
            mock_public_repo_url.return_value = "https://github.com"
            client = GithubOrgClient("github")
            result = client.public_repos()
            self.assertEqual(["github", "github2"], result)
            mock_get.assert_called_once()
            mock_public_repo_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Testing has_license method"""
        client = GithubOrgClient("url")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
