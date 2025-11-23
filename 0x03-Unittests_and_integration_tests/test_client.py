#!/usr/bin/env python3
"""
Unit and integration tests for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
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


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration tests using fixtures """

    @classmethod
    def setUpClass(cls):
        """ Start patcher for requests.get """
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Configure side effects for all GET requests
        mock_get.side_effect = [
            cls.org_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        """ Stop patcher """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Test that public_repos returns expected fixture results """
        client = GithubOrgClient("google")
        result = client.public_repos()

        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that public_repos(license="apache-2.0")
        filters repos correctly using the fixtures
        """
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")

        self.assertEqual(result, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
