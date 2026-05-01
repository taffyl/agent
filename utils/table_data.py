from dataclasses import dataclass, field

@dataclass
class TableData(object):
    def __init__(self) -> None:
        self.id: int = None
        self.item: str = None
        self.price: float = None
        self.num: int = None
        self.buyer: str = None
        self.state: str = None
        

    