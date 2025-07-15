import pytest
from service.API_client import APIClient

class TestAPIClient:
    def test_get_constructs_correct_url_and_params(monkeypatch):
        client = APIClient()
        client.api_url = "http://example.com/"

        calls = {}
        def fake_get(url, timeout):
            calls['url'] = url
            calls['timeout'] = timeout
            class FakeResponse:
                def raise_for_status(self): pass
                def json(self): return {"success": True}
            return FakeResponse()

        monkeypatch.setattr('service.API_client.requests.get', fake_get)
        result = client.get(endpoint='test/endpoint', params={'a': '1'})

        assert calls['url'] == 'http://example.com/test/endpoint?a=1'
        assert calls['timeout'] == 600
        assert result == {"success": True}
