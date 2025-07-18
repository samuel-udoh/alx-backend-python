#!/usr/bin/env python3
"""
Unit tests for the client.py
"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import PropertyMock, patch, MagicMock
from fixtures import TEST_PAYLOAD


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


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class,
    mocking only external requests.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the class by patching requests.get.
        This runs ONCE before all tests in the class start.
        """
        def mock_side_effect(url: str) -> MagicMock:
            """
            Checks the URL and returns the appropriate
            mock response based on our fixtures.
            """

            magic_response = MagicMock()

            repos_url = cls.org_payload.get("repos_url")

            if url == repos_url:
                magic_response.json.return_value = cls.repos_payload
            else:
                magic_response.json.return_value = cls.org_payload

            return magic_response
        cls.get_patcher = patch("utils.requests.get")
        mock_request_get = cls.get_patcher.start()
        mock_request_get.side_effect = mock_side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patcher after all tests in the class have run.
        """
        if cls.get_patcher:
            cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test that public_repos returns the correct list of repository names.
        """
        client = GithubOrgClient("google")
        response = client.public_repos()
        self.assertEqual(response, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that public_repos correctly filters by license.
        """
        client = GithubOrgClient("google")
        response = client.public_repos(license="apache-2.0")
        self.assertEqual(response, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
