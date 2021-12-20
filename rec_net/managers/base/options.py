from abc import ABCMeta
import asyncio

class Options(metaclass=ABCMeta):
    def __init__(self, manager, dataobject):
        self.manager = manager
        self.data = dataobject
        self.tasks = []
        
    async def build(self):
        await asyncio.gather(*self.tasks)
        if isinstance(self.data, list):
            for data in self.data: data.manager = self.manager
        else: self.data.manager = self.manager
        return self.data
        
    def __getattr__(self, attr):
        if attr in self.configurables:
            return self.option(self.configurables[attr])
    
    def option(self, func):
        def inner(include, **kwargs):
            if include:
                task = asyncio.create_task(func(self.data, **kwargs))
                self.tasks.append(task)
            return self
        return inner