import unittest
from unittest.mock import patch, MagicMock
from decimal import Decimal  # Import Decimal to handle decimal numbers
import json
from src.my_lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    @patch('src.my_lambda_function.boto3.resource')
    def test_lambda_handler(self, mock_dynamodb_resource):
        print("Test is running")  # Debugging line to confirm the test is running

        # Mock the DynamoDB table and its update_item method
        mock_table = MagicMock()
        mock_dynamodb_resource.return_value.Table.return_value = mock_table
        mock_table.update_item.return_value = {
            'Attributes': {'count': Decimal('10')}  # Use Decimal to match your Lambda function
        }

        print("Calling lambda_handler")  # Debugging line to confirm we're about to call the function

        # Call the lambda_handler function
        event = {}
        context = {}
        response = lambda_handler(event, context)

        print("Lambda handler returned a response")  # Debugging line to confirm the function was called

        # Verify the DynamoDB update_item call
        mock_table.update_item.assert_called_once_with(
            Key={'id': 'visitorCount'},
            UpdateExpression='SET #count = if_not_exists(#count, :start) + :inc',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':inc': 1, ':start': 0},
            ReturnValues='UPDATED_NEW'
        )

        print("Update item call was successful")  # Debugging line after verifying the mock call

        # Verify the response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], '*')
        self.assertEqual(
            json.loads(response['body']),
            {'visitor_count': 10}
        )

if __name__ == '__main__':
    unittest.main()
