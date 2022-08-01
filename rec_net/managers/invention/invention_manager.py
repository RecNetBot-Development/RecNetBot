from .invention import Invention
from ..base import BaseManager
from ...rest import run_in_queue

class InventionManager(BaseManager):
    def __init__(self, client):
        super().__init__(client, Invention)
        self.configurables = {
            "creator": self.get_creator,
        }

    @BaseManager.data_method
    def get_data(self, id):
        return {
            "id": self.rec_net.api.inventions.v1.get(params={"inventionId": id}),
            "name": self.rec_net.api.inventions.v2.search.get(params={"value": id})
        }

    @BaseManager.get_method("creator")
    async def get_creator(self, id, **options):
        resp = await self.rec_net.accounts.account(id).get().fetch()
        return resp.data
    
    @BaseManager.get_method("room")
    async def get_room(self, id, **options):
        resp = await self.rec_net.rooms.room(id).get().fetch()
        return resp.data


