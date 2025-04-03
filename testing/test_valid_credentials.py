import requests

BASE_URL = "http://retrieval-load-balancer-334368182.ap-southeast-2.elb.amazonaws.com"
INVALID_USERNAME = "invalid_username"
class TestCredentialValidation():
    def test_invalid_credentials_retrievalV2(self):
        r = requests.get(f"{BASE_URL}/v2/retrieve/{INVALID_USERNAME}/finance/apple/")
        assert r.status_code == 401

    def test_invalid_credentials_retrievalV1(self):
        r = requests.get(f"{BASE_URL}/v1/retrieve/{INVALID_USERNAME}/apple/")
        assert r.status_code == 401

    def test_invalid_credentials_list(self):
        r = requests.get(f"{BASE_URL}/v1/list/{INVALID_USERNAME}/")
        assert r.status_code == 401


    def test_invalid_credentials_delete(self):
        r = requests.delete(f"{BASE_URL}/v1/delete/{INVALID_USERNAME}/apple/")
        assert r.status_code == 401
