import requests

BASE_URL = "http://retrieval-load-balancer-334368182.ap-southeast-2.elb.amazonaws.com/"
USERNAME = "raj"
class TestingAllRoute():
    def test_successful_retrieval_routeV2(self):
        r = requests.get(f"{BASE_URL}/v2/retrieve/{USERNAME}/finance/apple/")
        assert r.status_code == 200
        assert (len(r.json()) > 0)
        assert r.json().get('stock_name') == 'apple'

    
    def test_successful_retrieval_routeV1(self):
        r = requests.get(f"{BASE_URL}/v1/retrieve/{USERNAME}/apple/")
        assert r.status_code == 200
        assert (len(r.json()) > 0)
        assert r.json().get('stock_name') == 'apple'

    def test_successful_listing_routeV1(self):
        r = requests.get(f"{BASE_URL}/v1/list/{USERNAME}/")

        assert r.status_code == 200

        # v2 retrieval route makes filenames of format {dataType}_{stockName}
        # v1 retrieval route makes filenames of format {stockName}
        assert r.json().get('Success') == ['finance_apple', 'apple']

    def test_successful_deleteV1(self):
        r = requests.delete(f"{BASE_URL}/v1/delete/{USERNAME}/finance_apple")
        assert r.status_code == 200

        r = requests.delete(f"{BASE_URL}/v1/delete/{USERNAME}/apple")
        assert r.status_code == 200

        r = requests.get(f"{BASE_URL}/v1/list/{USERNAME}/")
        assert r.status_code == 200
        assert r.json().get("Success") == []





