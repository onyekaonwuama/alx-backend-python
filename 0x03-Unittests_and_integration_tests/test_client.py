#!/usr/bin/env python3
"""
Unit tests for client module
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
import client
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        test_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = test_payload

        github_client = client.GithubOrgClient(org_name)
        result = github_client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }

            github_client = client.GithubOrgClient("google")
            result = github_client._public_repos_url

            self.assertEqual(result,
                           "https://api.github.com/orgs/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = \
                "https://api.github.com/orgs/google/repos"

            github_client = client.GithubOrgClient("google")
            result = github_client.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license method"""
        github_client = client.GithubOrgClient("google")
        result = github_client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test cases for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests"""
        def side_effect(url):
            """Side effect function for mocking requests.get"""
            mock_response = Mock()
            if url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = cls.org_payload
            return mock_response

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """Test public_repos method in integration test"""
        github_client = client.GithubOrgClient("google")
        self.assertEqual(github_client.org, self.org_payload)
        self.assertEqual(github_client.repos_payload, self.repos_payload)
        self.assertEqual(github_client.public_repos(), self.expected_repos)
        self.assertEqual(github_client.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        github_client = client.GithubOrgClient("google")
        self.assertEqual(github_client.public_repos(), self.expected_repos)
        self.assertEqual(github_client.public_repos("apache-2.0"),
                         self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """Tear down class fixtures after running tests"""
        cls.get_patcher.stop()


if __name__ == '__main__':
    unittest.main()