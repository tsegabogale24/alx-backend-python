#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class using unittest, parameterized, and patch.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected value"""
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        self.assertEqual(result, {"login": org_name})
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org payload"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}

        client = GithubOrgClient("test_org")
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = test_payload
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
