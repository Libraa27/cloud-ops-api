
import unittest
from unittest.mock import patch
from urllib.error import HTTPError,  URLError

from main import monitor_target


class TestMonitorTarget(unittest.TestCase):

    @patch("main.urllib.request.urlopen")
    def test_healthy_target(self, mock_urlopen):
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.status = 200

        result = monitor_target()

        self.assertTrue(result["reachable"])
        self.assertTrue(result["healthy"])
        self.assertEqual(result["status_code"], 200)

    @patch("main.urllib.request.urlopen")
    def test_unreachable_target(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("DNS resolution failed")

        result = monitor_target()

        self.assertFalse(result["reachable"])
        self.assertFalse(result["healthy"])
        self.assertIsNone(result["status_code"])
        self.assertIn("DNS resolution failed", result["error"])

    @patch("main.urllib.request.urlopen")
    def test_unhealthy_target(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            "http://target:80/",
            500,
            "Internal Server Error",
            {},
            None
        )

        result = monitor_target()

        self.assertTrue(result["reachable"])
        self.assertFalse(result["healthy"])
        self.assertEqual(result["status_code"], 500)
