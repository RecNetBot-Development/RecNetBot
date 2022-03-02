class APIRequest:
    def __init__(self, client, path, method, params=None, data=None):
        self.url = path
        self.method = method
        self.params = params
        self._client = client
        self.body = data

    async def fetch(self):
        return await self._client.push(self)

    @property
    def bucket(self):
        return f"{self.url}:{self.params}:{self.body}"


