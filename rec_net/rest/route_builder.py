from .make_request import APIRequest

HTTP_METHODS = [
    "get",
    "post",
    "delete",
    "patch",
    "put"
]

class APIRouteBuilder(object):
    def __init__(self, manager, host):
        self._route = []
        self._BaseURL = host
        self._client = manager.http_client

    def build_request(self, method, param, body):
        path = self._BaseURL + "/".join(self._route)
        return APIRequest(self._client, path, method, param, body)

    def __getattr__(self, name):
        if name in HTTP_METHODS:
            return lambda params=None, data=None: self.build_request(name, params, data)
        self._route.append(name)
        return self

    def __call__(self, *args):
        self._route += [*map(str, args)]
        return self
