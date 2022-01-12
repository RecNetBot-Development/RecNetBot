from attr import dataclass

@dataclass
class SubRoom:

    replication_id: str
    supports_join_in_progress: bool
    match_making: list
    id: int
    unity_scene_id: str
    name: str
    is_sandbox: bool
    max_players: int
    accessibilty: int

    @classmethod
    def from_data(cls, data):
        if isinstance(data, list): return [*map(SubRoom.from_data, data)]
        match_making = []
        if data["UseLevelBasedMatchmaking"]: match_making.append("level")
        if data["UseAgeBasedMatchmaking"]:  match_making.append("age")
        if data["UseRecRoyaleMatchmaking"]: match_making.append("rec royal")
        return cls(
            replication_id = data["ReplicationId"],
            supports_join_in_progress = data["SupportsJoinInProgress"],
            match_making=match_making,
            id = data["SubRoomId"],
            unity_scene_id = data["UnitySceneId"],
            name = data["Name"],
            is_sandbox = data["IsSandbox"],
            max_players = data["MaxPlayers"],
            accessibilty = data["Accessibility"]
        ) 
