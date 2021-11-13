from rest import make_request

class APIRouteBuilder(object):
    def __init__(self, host):
        self._route = []
        self._BaseURL = host

    def get(self, params=None):
        path = self._BaseURL + "/".join(self._route)
        return make_request.APIRequest(path=path, method="get", params=params)

    def post(self, params=None, data=None):
        path = self._BaseURL + "/".join(self._route)
        return make_request.APIRequest(path=path, method="post", params=params, data=data)

    def __getattr__(self, name):
        self._route.append(name)
        return self

    def __call__(self, *args):
        self._route += [*map(str, args)]
        return self
