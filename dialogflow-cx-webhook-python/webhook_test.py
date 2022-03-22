"""Tests for the webhook fixture deployed via Terraform."""

import os
import unittest
import json
import google.auth

from google.auth import identity_pool
import google.cloud.functions as gcf


_TEST_FUNCTION = os.environ['TEST_FUNCTION']
_PROJECT_ID = os.environ['PROJECT_ID']
_LOCATION = 'us-central1'
if os.environ.get('SVC_ACCOUNT_FILE'):
    _SVC_ACCOUNT_FILE = os.environ['SVC_ACCOUNT_FILE']
    with open(_SVC_ACCOUNT_FILE, 'r', encoding="utf8") as f:
        svc_account_file_data = f.read()
        svc_account_config_json = json.loads(svc_account_file_data)
        credentials = identity_pool.Credentials.from_info(svc_account_config_json)
else:
    credentials, _ = google.auth.default()


class TestWebhook(unittest.TestCase):
    """Test class for Dialogflow CX webhook sample."""

    # pylint: disable=no-self-use
    def test_webhook_is_live(self):
        """Tests the the webhook is live."""

        # Test live webhook after deployment:
        client = gcf.CloudFunctionsServiceClient(credentials=credentials)
        text = 'example_text'
        tag = 'example_tag'
        example_request = {'text':text, 'fulfillmentInfo': {'tag': tag}}
        request = gcf.CallFunctionRequest(
          name=f'projects/{_PROJECT_ID}/'
               f'locations/{_LOCATION}/'
               f'functions/{_TEST_FUNCTION}', data=json.dumps(example_request))
        response = client.call_function(request)
        response_dict = gcf.CallFunctionResponse.to_dict(response)
        result = json.loads(response_dict['result'])
        msg = result['fulfillment_response']['messages'][0]['text']['text'][0]
        assert msg == f'Webhook received: {text} (Tag: {tag})'


if __name__ == '__main__':
    unittest.main()
