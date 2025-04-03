import requests

BASE_URL = "http://retrieval-load-balancer-334368182.ap-southeast-2.elb.amazonaws.com/"
USERNAME = "raj"
class TestCredentialValidation():
    # def test_invalid_input_retrievalV2(self):
    #     r = requests.get(f"{BASE_URL}/v2/retrieve/{USERNAME}/wrong-data-type/apple/")
    #     print(r.json())
    #     assert r.status_code == 400

    def test_invalid_input_retrievalV1(self):
        r = requests.get(f"{BASE_URL}/v1/retrieve/{USERNAME}/wrong-stock-name/")
        print(r.json())
        assert r.status_code == 400

    def test_invalid_input_delete(self):
        r = requests.delete(f"{BASE_URL}/v1/delete/{USERNAME}/nonexistent-file-name/")
        print(r.json())
        assert r.status_code == 400
