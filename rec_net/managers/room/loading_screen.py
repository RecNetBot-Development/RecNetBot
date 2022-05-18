from attr import dataclass

@dataclass
class LoadingScreen:

    image_name: str
    title: str
    subtitle: str

    @classmethod
    def from_data(cls, data):
        if isinstance(data, list): return [*map(LoadingScreen.from_data, data)]
        return cls(
            image_name = data["ImageName"],
            title = data["Title"],
            subtitle = data["Subtitle"]
        )