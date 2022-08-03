from attr import dataclass, field
from rec_net.managers.account.user import User
from rec_net.managers.invention.invention_options import InventionOptions
from ...helpers import date_to_unix
from ..base import BaseDataclass
from ..room.room import Room

@dataclass
class CurrentVersion:
    id: int # InventionId
    version: int # VersionNumber
    ink: int # InstantationCost
    lights_ink: int # LightsCost
    chips_cost: int # ChipsCost
    cloud_variables: int # CloudVariablesCost

@dataclass
class Invention(BaseDataclass):
    """Dataclass for an invention"""
    name: str # Name
    description: str # Description
    image_name: str # ImageName
    version: int # CurrentVersionNumber
    
    id: int # InventionId
    modified_at: int # ModifiedAt
    created_at: int # CreatedAt
    published_at: int # FirstPublishedAt
    in_room_count: int # NumPlayersHaveUsedInRoom
    download_count: int # NumDownloads
    cheer_count: int # CheerCount
    creator_permission: int # CreatorPermission
    general_permission: int # GeneralPermission
    price: int # Price
    
    current_version: CurrentVersion  # CurrentVersion
    creator: int | User # CreatorPlayerId
    creation_room: int | Room # CreationRoomId
    
    is_featured: bool # IsFeatured
    is_rro: bool # IsAGInvention
    is_certified: bool # IsCertifiedInvention
    is_trial_allowed: bool # AllowTrial
    is_hidden_from_player: bool # HideFromPlayer
    
    @staticmethod
    def configure(manager, user):
        return InventionOptions(manager, user)

    @classmethod
    def from_data(cls, data, **kwargs):
        if isinstance(data, list): return [*map(Invention.from_data, data)]
        
        unix_modified_at = date_to_unix(data["ModifiedAt"])
        unix_created_at = date_to_unix(data["CreatedAt"])
        unix_published_at = date_to_unix(data["FirstPublishedAt"])
        
        return cls(
            id = data["InventionId"],
            creator = data["CreatorPlayerId"],
            name = data["Name"],
            description = data["Description"],
            image_name = data["ImageName"],
            version = data["CurrentVersionNumber"],
            current_version = data["CurrentVersion"],
            is_featured = data["IsFeatured"],
            modified_at = unix_modified_at,
            created_at = unix_created_at,
            published_at = unix_published_at,
            creation_room = data["CreationRoomId"],
            in_room_count = data["NumPlayersHaveUsedInRoom"],
            download_count = data["NumDownloads"],
            cheer_count = data["CheerCount"],
            creator_permission = data["CreatorPermission"],
            general_permission = data["GeneralPermission"],
            is_rro = data["IsAGInvention"],
            is_certified = data["IsCertifiedInvention"],
            price = data["Price"],
            is_trial_allowed = data["AllowTrial"],
            is_hidden_from_player = data["HideFromPlayer"],
            **kwargs
        )
