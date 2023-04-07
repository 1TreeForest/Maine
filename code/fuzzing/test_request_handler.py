import unittest
from unittest.mock import Mock, patch
from helpers.request_handler import RequestHandler
from definition.seed_input import SeedInput

class TestRequestHandler(unittest.TestCase):

    @patch('requests.get')
    def test_handle_request_get(self, mock_get):
        seed_input = SeedInput(url='http://example.com', method='GET', parameters="param1=value1", headers={'header1': 'value1'})
        mock_get.return_value.content = b'response content'
        handler = RequestHandler()
        response = handler.handle_request(seed_input)
        self.assertEqual(response.content, b'response content')
        print("Test: get")
        print("Seed Input: ", seed_input)
        print("Response: ", response.content)
        print("-------------------------------")

    @patch('requests.post')
    def test_handle_request_post(self, mock_post):
        seed_input = SeedInput(url='http://example.com', method='POST', parameters="param1=value1", headers={'header1': 'value1'})
        mock_post.return_value.content = b'response content'
        handler = RequestHandler()
        response = handler.handle_request(seed_input)
        self.assertEqual(response.content, b'response content')
        print("Test: post")
        print("Seed Input: ", seed_input)
        print("Response: ", response.content)
        print("-------------------------------")
        
    def test_handle_request_invalid_method(self):
        seed_input = SeedInput(url='http://example.com', method='PUT', parameters="param1=value1", headers={'header1': 'value1'})
        handler = RequestHandler()
        with self.assertRaises(ValueError):
            handler.handle_request(seed_input)
        print("Test: invalid method")
        print("Seed Input: ", seed_input)
        print("-------------------------------")
        
    def test_local_get_request(self):        
        seed_input = SeedInput(url='http://localhost/index.php', method='GET', parameters="action=file3&input1=admin&input2=password", headers={'header1': 'value1'})
        handler = RequestHandler()
        response = handler.handle_request(seed_input)
        self.assertIsNotNone(response)
        print(response.content)
        
if __name__ == '__main__':
    unittest.main()
