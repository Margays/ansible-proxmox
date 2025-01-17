from typing import Optional, Dict
from dataclasses import asdict, dataclass


@dataclass
class Pool:
    poolid: Optional[str] = None
    comment: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        return cls(
            poolid=data.get('poolid', None),
            comment=data.get('comment', None)
        )
    
    def to_dict(self) -> Dict[str, str]:
        return asdict(self)
    
    def diff(self, other: Optional['Pool']) -> Dict[str, str]:
        diff: Dict[str, str] = {}
        for key, value in asdict(self).items():
            if value is None:
                continue

            if value != getattr(other, key, None):
                diff[key] = value

        return diff