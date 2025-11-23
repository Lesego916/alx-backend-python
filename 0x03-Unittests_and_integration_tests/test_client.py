#!/usr/bin/env python3
"""
Unit and integration tests for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class

import client
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that org() returns the expected value and get_json called once."""
        mock_get_json.return_value = {"any": "payload"}
        gh = client.GithubOrgClient(org_name)
        result = gh.org()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/{}".format(org_name))
        self.assertEqual(result, {"any": "payload"})

    def test_public_repos_url(self):
        """Test _public_repos_url uses org payload to return repos_url."""
        gh = client.GithubOrgClient("some_org")
        fake_org = {"repos_url": "https://api.github.com/orgs/some_org/repos"}
        with patch.object(client.GithubOrgClient, "org", return_value=fake_org):
            self.assertEqual(gh._public_repos_url, fake_org["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names using mocked get_json and _public_repos_url."""
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        gh = client.GithubOrgClient("orgname")
        with patch.object(client.GithubOrgClient, "_public_repos_url", "https://api.github.com/orgs/orgname/repos"):
            repos = gh.public_repos()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/orgname/repos")
            self.assertEqual(repos, ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean depending on repo license."""
        gh = client.GithubOrgClient("org")
        self.assertEqual(gh.has_license(repo, license_key), expected)


@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), [
    (org_payload, repos_payload, expected_repos, apache2_repos),
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and set side_effect to return fixture payloads."""
        get_patcher = patch('client.requests.get')
        cls.get_patcher = get_patcher
        cls.mock_get = get_patcher.start()

        # side_effect for .json() depending on call order
        mock_org = Mock()
        mock_org.json.return_value = cls.org_payload
        mock_repos = Mock()
        mock_repos.json.return_value = cls.repos_payload

        cls.mock_get.side_effect = [mock_org, mock_repos]

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos returns expected_repos."""
        gh = client.GithubOrgClient(self.org_payload.get("login"))
        repos = gh.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: filter repos by license (apache-2.0)"""
        gh = client.GithubOrgClient(self.org_payload.get("login"))
        repos = gh.public_repos(license_key="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
