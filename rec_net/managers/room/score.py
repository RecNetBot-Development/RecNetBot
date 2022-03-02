from attr import dataclass

@dataclass
class Score:
    visit_type: int
    score: float
    backup_score: float

    @classmethod
    def from_data(cls, data):
        if isinstance(data, list): return [*map(Score.from_data, data)]
        return cls(
            visit_type = data["VisitType"],
            score = data["Score"],
            backup_score = data["BackupScore"]
        )