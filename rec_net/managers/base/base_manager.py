from abc import ABCMeta, abstractmethod
from .base_dataclass import BaseDataclass
from ...rest import run_in_queue
import asyncio
  

class BaseManager(metaclass=ABCMeta):
    def __init__(self, client, dataclass):
        self.client = client
        self.rec_net = client.rec_net
        self._dataclass = dataclass
        #map string values to the appropriate object factory
        self.resolvables = {
            "account": self.client.account,
            "image": self.client.image, 
            "event": self.client.event, 
            "room": self.client.room 
        }
        
    async def create_builder(self, id = None, name = None, data = None, includes = None, options = {}, **kwargs):
        if data is None:
            data = await self.get_data(name, "name") if id is None else await self.get_data(id, "id")
        dataobject = self._dataclass.from_data(data)
        return await self.build(dataobject, includes, options)
        
    async def build(self, data, includes = None, options = {}):
        tasks = []
        if includes is not None:
            for include in includes:
                option = options.get(include, {})
                func = self.configurables[include]
                task = asyncio.create_task(func(data, **option))
                tasks.append(task)
        await asyncio.gather(*tasks)
        if isinstance(data, list):
            for obj in data: obj.manager = self
        else: data.manager = self
        return data

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

    async def resolve(self, resolve_type, **options): 
        dataclass = self.resolvables.get(resolve_type)
        return await dataclass(**options)

    @staticmethod
    def data_method(func):
        async def inner(self, id, type, **options):
            reqs = func(self, id, **options)
            if isinstance(id, list):
                return await self.handle_bulk(reqs["bulk"], id, type)
            resp = await reqs[type].fetch()
            return resp.data
        return inner

    @staticmethod
    def get_method(attr, resolve = None, type = "data"):
        def decorator(func):
            async def inner(self, data_obj, **options):
                if isinstance(data_obj, list): return await run_in_queue(lambda obj, **kwargs: inner(self, obj, **kwargs), data_obj, **options)
                id = self.resolve_id(data_obj)
                data = await func(self, id, data_object = data_obj, **options)
                if resolve is not None:
                    if type == "id":
                        if options.pop("resolve", False): data = await self.resolve(resolve, id=data, **options)
                    else:
                        data = await self.resolve(resolve, data=data, **options)
                return self.response(data_obj, attr, data)
            return inner
        return decorator

    @staticmethod 
    def resolve_method(attr, resolve):
        def decorator(func):
            async def inner(self, data_obj, **options):
                ids = func(self, data_obj, **options)
                if ids is not None:
                    data = await self.resolve(resolve, id=ids, **options)
                    return self.response(data_obj, attr, data)
                return None
            return inner
        return decorator

    @staticmethod
    def bulk_get_method(attr, resolve = None, data_key = None):
        def decorator(func):
            async def inner(self, data_obj, **options):
                req = func(self)
                if isinstance(data_obj, list):
                    resp = await self.handle_bulk(req, data_obj, "id")
                    if data_key is not None:
                        return [self.response(data_obj[i], attr, d[data_key]) for i, d in enumerate(resp.data)]
                    return [self.response(data_obj[i], attr, d) for i, d in enumerate(resp.data)]
                id = self.resolve_id(data_obj)
                req.body = {"id": id}
                resp = await req.fetch()
                data = resp.data[0]
                if data_key is not None: data = data[data_key]
                return self.response(data_obj, attr, data)
            return inner
        return decorator

    @abstractmethod
    async def get_data(self, id = None, type = None):
        pass
    