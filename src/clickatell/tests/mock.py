import logging
from clickatell.http import HttpClient
from clickatell.client import Client
from clickatell.errors import ClickatellError

class TestHttpClient(HttpClient):
    """A Client that allows us to mock the expected response"""
    
    def __init__(self):
        super(TestHttpClient, self).__init__()
        self.queue = {}
    
    def mock(self, method, url, data={}, headers={}, response={}):
        method = method.upper()
        self.queue.setdefault(method, [])
        self.queue[method].append((url, data, headers, response))
    
    def get_mocked(self, method, url, data={}, headers={}):
        method = method.upper()
        method_queue = self.queue.get(method, [])
        for s_url, s_data, s_headers, response in method_queue:
            if (url == s_url) \
                and (data == s_data) \
                and (headers == s_headers):
                logging.warning("Mocked response: %s" % response)
                return response
        raise ClickatellError, 'No matching mocked data matches %s, %s, %s, %s' \
                                    % (method, url, data, headers)
    def log_mocks(self):
        for method, mocks in self.queue.items():
            for url, data, headers, response in mocks:
                logging.debug("%(method)s %(url)s with %(data)s and "
                                "headers (%(headers)s):" % locals())
                logging.debug("\t\t -> %s" % response)
    
    def get(self, *args, **kwargs):
        return self.get_mocked('get', *args, **kwargs)
    
    def post(self, *args, **kwargs):
        return self.get_mocked('post', *args, **kwargs)
    

class TestClient(TestHttpClient, Client):
    pass


