from attr import dataclass

@dataclass
class Comment:

    id: int
    player: int
    comment: str

    @classmethod
    def from_data(cls, data):
        if isinstance(data, list): return [*map(Comment.from_data, data)]
        return cls(
            id = data["SavedImageCommentId"],
            player = data["PlayerId"],
            comment = data["Comment"]
        )