#!/usr/bin/env python3
"""
Unit and integration tests for GithubOrgClient class using unittest,
parameterized, and patch.

Includes:
- Task 0-8 unit tests
- Task 9 integration tests for public_repos
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Task 5: Test that GithubOrgClient.org returns expected value"""
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        self.assertEqual(result, {"login": org_name})
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Task 6: Test that _public_repos_url returns correct URL"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        client = GithubOrgClient("test_org")
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Task 6: Test that public_repos returns a list of repository names"""
        test_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_repos_payload

        client = GithubOrgClient("test_org")

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = (
                "https://api.github.com/orgs/test_org/repos"
            )
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url.return_value)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Task 7: Test that has_license returns True if repo has the license"""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


# Task 9: Integration tests
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures and patch requests.get"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url.endswith("/orgs/google"):
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            if url.endswith("/repos"):
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            return unittest.mock.Mock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Task 9: Integration test for public_repos"""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Task 9: Integration test for public_repos filtered by license"""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
