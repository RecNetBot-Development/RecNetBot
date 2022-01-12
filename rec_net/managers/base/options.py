from abc import ABCMeta
import asyncio

class Options(metaclass=ABCMeta):
    def __init__(self, manager, dataobject):
        self.manager = manager
        self.data = dataobject
        self.tasks = []
        
    async def build(self, includes, options):
        for include in includes:
            option = options.get(include, {})
            func = self.configurables[include]
            task = asyncio.create_task(func(self.data, **option))
            self.tasks.append(task)
        await asyncio.gather(*self.tasks)
        if isinstance(self.data, list):
            for data in self.data: data.manager = self.manager
        else: self.data.manager = self.manager
        return self.data
       