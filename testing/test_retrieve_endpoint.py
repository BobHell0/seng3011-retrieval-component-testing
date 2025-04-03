import requests
import boto3
import pytest

tableName = "seng3011-test-dynamodb"

BASE_URL = "http://retrieval-load-balancer-334368182.ap-southeast-2.elb.amazonaws.com/"
USERNAME = "raj"

@pytest.mark.filterwarnings(r"ignore:datetime.datetime.utcnow\(\) is deprecated:DeprecationWarning")
class TestingValidRoutes():
    def test_successful_retrieval_routeV2(self):
        r = requests.get(f"{BASE_URL}/v2/retrieve/{USERNAME}/finance/apple/")
        assert r.status_code == 200
        assert (len(r.json()) > 0)
        assert r.json().get('stock_name') == 'apple'

        dynamodb_client = boto3.client('dynamodb',  region_name="ap-southeast-2")
        response = dynamodb_client.get_item(TableName=tableName, Key={
            'username': {'S': USERNAME}
        })

        item = response.get('Item')
        assert item.get('retrievedFiles').get('L')[0].get('M').get('filename').get('S') == 'finance_apple'

    def test_successful_retrieval_routeV1(self):
        r = requests.get(f"{BASE_URL}/v1/retrieve/{USERNAME}/apple/")
        assert r.status_code == 200
        assert (len(r.json()) > 0)
        assert r.json().get('stock_name') == 'apple'

        dynamodb_client = boto3.client('dynamodb',  region_name="ap-southeast-2")
        response = dynamodb_client.get_item(TableName=tableName, Key={
            'username': {'S': USERNAME}
        })

        item = response.get('Item')
        assert item.get('retrievedFiles').get('L')[1].get('M').get('filename').get('S') == 'apple'

    def test_successful_listing_routeV1(self):
        r = requests.get(f"{BASE_URL}/v1/list/{USERNAME}/")

        assert r.status_code == 200
        assert r.json().get('Success') == ['finance_apple', 'apple']

    def test_successful_deleteV1(self):
        r = requests.delete(f"{BASE_URL}/v1/delete/{USERNAME}/finance_apple")
        assert r.status_code == 200

        dynamodb_client = boto3.client('dynamodb',  region_name="ap-southeast-2")
        response = dynamodb_client.get_item(TableName=tableName, Key={
            'username': {'S': USERNAME}
        })

        item = response.get('Item')
        assert item.get('retrievedFiles').get('L')[0].get('M').get('filename').get('S') == 'apple'

        r = requests.delete(f"{BASE_URL}/v1/delete/{USERNAME}/apple")
        assert r.status_code == 200

        r = requests.get(f"{BASE_URL}/v1/list/{USERNAME}/")
        assert r.status_code == 200
        assert r.json().get("Success") == []

        response = dynamodb_client.get_item(TableName=tableName, Key={
            'username': {'S': USERNAME}
        })

        item = response.get('Item')
        assert len(item.get('retrievedFiles').get('L')) == 0

    def test_double_deleteV1(self):
        r = requests.delete(f"{BASE_URL}/v1/delete/{USERNAME}/apple")
        assert r.status_code == 400
