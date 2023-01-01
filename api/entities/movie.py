class Movie:
    def __init__(
        self,
        *,
        _id: str,
        title: str,
        description: str,
        year: int,
        watched: bool = False
    ) -> None:
        if not _id:
            raise ValueError("Movie id is required !")
        self._id = _id
        self._title = title
        self._description = description
        self._year = year
        self._watched = watched

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def year(self) -> int:
        return self._year

    @property
    def watched(self) -> bool:
        return self._watched

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Movie):
            return False
        else:
            return (
                self.id == __o.id
                and self.title == __o.title
                and self.description == __o.description
                and self.year == __o.year
                and self.watched == __o.watched
            )

    def to_dict(self) -> dict:
        return {
            "_id": self.id,
            "title": self.title,
            "description": self.description,
            "year": self.year,
            "watched": self.watched,
        }
