from abc import ABCMeta, abstractmethod

class BaseManager(metaclass=ABCMeta):
    def __init__(self, client, dataclass):
        self.client = client
        self.rec_net = client.rec_net
        self._dataclass = dataclass 
        
    async def create_builder(self, id = None, name = None, data = None, **kwargs):
        if data is None:
            data = await self.get_data(name, "name") if id is None else await self.get_data(id, "id")
        dataobject = self._dataclass.from_data(data, **kwargs.pop("data", {}))
        config = self._dataclass.configure(self, dataobject)
        return await self.build_dataclass(config, **kwargs)
        
    def resolve_id(self, id):
        if isinstance(id, self._dataclass):
            return id.id
        return id
        
    def response(self, id, attr, data):
        if isinstance(id, self._dataclass):
            id.set(attr, data)
        return data
        
    async def handle_bulk(self, req, do, type):
        ids = [*map(self.resolve_id, do)]
        req.body = {type: ids}
        resp = await req.fetch()
        return resp.data

    async def resolve_multiple(self, Obj, do, key, attr, **options):
        unique = []
        for i in do:
            id = getattr(i, key)
            if id not in unique: unique.append(id)
        data = await Obj(id=unique, **options)
        data_dict = {d.id: d for d in data}
        return [self.response(i, attr, data_dict[getattr(i, key)]) for i in do]

    @abstractmethod
    async def get_data(self, id = None, type = None):
        pass
    
    @abstractmethod
    async def build_dataclass(self, config):
        pass