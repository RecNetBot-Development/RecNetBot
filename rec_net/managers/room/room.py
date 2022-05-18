import asyncio
from attr import dataclass, field
from ...helpers import date_to_unix
from .subroom import SubRoom
from .role import Role
from .score import Score
from .loading_screen import LoadingScreen
from ..base import BaseDataclass
from ..account import User
from ..image import Image
from ..event import Event

def resolve_warnings(x: int):
    warnings = ["Custom", "Spooky/scary themes", "Mature themes", "Bright/flashing lights", "Intense motion", "Gore/violence"]
    for index, warning in enumerate(warnings):
        if 1 << index & x:
            yield warning

@dataclass
class Room(BaseDataclass):
    id: int
    is_dorm: bool
    max_player_calculation_mode: int
    max_players: int
    cloning_allowed: bool
    disable_mic_auto_mute: bool
    disable_room_comments: bool
    encrypt_voice_chat: bool
    load_screen_lock: bool
    version: int
    name: str
    description: str
    created_at: int
    image_name: str
    warnings: list
    custom_warning: str
    creator: int or User
    state: int
    accessibility: int
    is_rro: bool
    supports_level_voting: bool
    supported_platforms: list
    min_level: int
    cheer_count: int
    favorite_count: int
    visitor_count: int
    visit_count: int
    sub_rooms: list = field(default=None)
    roles: list = field(default=None)
    tags: list = field(default=None)
    load_screens: list = field(default=None)
    scores: list = field(default=None)
    promo_images: list = field(default=None)
    promo_external_content: list = field(default=None)
    images: list = field(default=None)
    events: list = field(default = None)

    async def patch_info(self, data = {}, includes = None):
        if data is not None:
            sub_rooms = data.get("SubRooms")
            if sub_rooms is not None: self.sub_rooms = SubRoom.from_data(sub_rooms)
            roles = data.get("Roles")
            if roles is not None: self.roles = Role.from_data(roles)
            tags = data.get("Tags")
            if tags is not None: self.tags = [tag["Tag"] for tag in tags]
            load_screens = data.get("LoadScreens")
            if load_screens is not None: self.load_screens = LoadingScreen.from_data(load_screens)
            scores = data.get("Scores")
            if scores is not None: self.scores = Score.from_data(scores)
            promo_images = data.get("PromoImages")
            if promo_images is not None: self.promo_images = promo_images
            promo_external_content = data.get("PromoExternalContent")
            if promo_external_content is not None: self.promo_external_content = promo_external_content
        else: 
            data = await self.manager.get_data(self.id, includes=includes)
            await self.patch_info(data=data)

    @classmethod
    async def from_data(cls, data, **kwargs):
        if isinstance(data, list): return await asyncio.gather(*(Room.from_data(room) for room in data))
        supported_platforms = []
        if data["SupportsScreens"]: supported_platforms.append("screen")
        if data["SupportsWalkVR"]: supported_platforms.append("walk")
        if data["SupportsTeleportVR"]: supported_platforms.append("teleport")
        if data["SupportsVRLow"]: supported_platforms.append("vr low")
        if data["SupportsQuest2"]: supported_platforms.append("quest 2")
        if data["SupportsMobile"]: supported_platforms.append("mobile")
        if data["SupportsJuniors"]: supported_platforms.append("juniors")
        warnings = [warning for warning in resolve_warnings(data["WarningMask"])]
        created_at = date_to_unix(data["CreatedAt"])
        stats = data["Stats"]
        room = cls(
               id = data["RoomId"],
               is_dorm = data["IsDorm"],
               max_player_calculation_mode = data["MaxPlayerCalculationMode"],
               max_players = data["MaxPlayers"],
               cloning_allowed = data["CloningAllowed"],
               disable_mic_auto_mute = data["DisableMicAutoMute"],
               disable_room_comments = data["DisableRoomComments"],
               encrypt_voice_chat = data["EncryptVoiceChat"],
               load_screen_lock = data["LoadScreenLocked"],
               version = data["Version"],
               name = data["Name"],
               description = data["Description"],
               image_name = data["ImageName"],
               warnings = warnings,
               custom_warning = data["CustomWarning"],
               creator = data["CreatorAccountId"],
               state = data["State"],
               accessibility = data["Accessibility"],
               supports_level_voting = data["SupportsLevelVoting"],
               is_rro = data["IsRRO"],
               supported_platforms = supported_platforms,
               min_level = data["MinLevel"],
               created_at=created_at,
               cheer_count = stats["CheerCount"],
               favorite_count = stats["FavoriteCount"],
               visitor_count = stats["VisitorCount"],
               visit_count = stats["VisitCount"]
        )
        await room.patch_info(data=data, includes=kwargs.get('includes', 0))
        return room