import unittest
from unittest.mock import patch, Mock
from api_client import make_api_request, process_response, APIResponse
import requests

class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.test_url = "https://api.example.com/test"
        self.test_api_key = "test_api_key"
        self.test_data = {"key": "value"}
        self.test_headers = {"Content-Type": "application/json"}

    @patch('requests.request')
    def test_successful_get_request(self, mock_request):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Make request
        result = make_api_request(
            url=self.test_url,
            method='GET',
            api_key=self.test_api_key
        )

        # Verify results
        self.assertIsInstance(result, APIResponse)
        self.assertEqual(result.data, {"status": "success"})
        self.assertEqual(result.status_code, 200)
        self.assertIsNone(result.error)
        
        mock_request.assert_called_once()
        call_args = mock_request.call_args[1]
        self.assertEqual(call_args['method'], 'GET')
        self.assertEqual(call_args['url'], self.test_url)
        self.assertEqual(call_args['headers']['Authorization'], f'Bearer {self.test_api_key}')

    @patch('requests.request')
    def test_successful_post_request(self, mock_request):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "status": "created"}
        mock_response.status_code = 201
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Make request
        result = make_api_request(
            url=self.test_url,
            method='POST',
            data=self.test_data,
            api_key=self.test_api_key
        )

        # Verify results
        self.assertIsInstance(result, APIResponse)
        self.assertEqual(result.data, {"id": 1, "status": "created"})
        self.assertEqual(result.status_code, 201)
        self.assertIsNone(result.error)
        
        mock_request.assert_called_once()
        call_args = mock_request.call_args[1]
        self.assertEqual(call_args['method'], 'POST')
        self.assertEqual(call_args['json'], self.test_data)

    @patch('requests.request')
    def test_request_error_handling(self, mock_request):
        # Setup mock to raise an exception
        mock_response = Mock()
        mock_response.status_code = 404
        mock_request.side_effect = requests.exceptions.RequestException(response=mock_response)

        # Make request
        result = make_api_request(
            url=self.test_url,
            method='GET',
            api_key=self.test_api_key
        )

        # Verify error handling
        self.assertIsInstance(result, APIResponse)
        self.assertIsNone(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertIsNotNone(result.error)

    @patch('builtins.print')
    def test_process_response_success(self, mock_print):
        test_response = APIResponse(
            data={"status": "success"},
            status_code=200
        )
        process_response(test_response)
        mock_print.assert_called()

    @patch('builtins.print')
    def test_process_response_error(self, mock_print):
        test_response = APIResponse(
            data=None,
            status_code=404,
            error="Not Found"
        )
        process_response(test_response)
        mock_print.assert_called_with("Error: Not Found")

    @patch('builtins.print')
    def test_process_response_empty(self, mock_print):
        test_response = APIResponse(
            data=None,
            status_code=200
        )
        process_response(test_response)
        mock_print.assert_called_with("No response data to process")

if __name__ == '__main__':
    unittest.main() 