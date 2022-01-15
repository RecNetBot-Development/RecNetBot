from abc import ABCMeta

class BaseDataclass(metaclass=ABCMeta):
    def set(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

    def __getattr__(self, attr):
        value = getattr(self.manager, attr)
        if attr not in ("get_data", "build_dataclass", "create_builder") and callable(value):
            async def ret(**kwargs):
                return await value(self, **kwargs)
            return ret