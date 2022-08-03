from .invention import Invention
from ..base import BaseManager
from ...rest import run_in_queue

class InventionManager(BaseManager):
    def __init__(self, client):
        super().__init__(client, Invention)
        self.configurables = {
            "creator": self.resolve_creator,
            "room": self.resolve_room
        }

    @BaseManager.data_method
    def get_data(self, id):
        return {
            "id": self.rec_net.api.inventions.v1.get(params={"inventionId": id}),
            "name": self.rec_net.api.inventions.v2.search.get(params={"value": id})
        }
    
    @BaseManager.resolve_method("creator", "account")
    def resolve_creator(self, invention, **options):
        if isinstance(invention.creator, int): return invention.creator
        return None
    
    @BaseManager.resolve_method("room", "room")
    def resolve_room(self, invention, **options):
        if isinstance(invention.room, int): return invention.room
        return None


