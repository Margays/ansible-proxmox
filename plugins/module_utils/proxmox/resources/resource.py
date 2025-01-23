from typing import Dict, Optional, List


class __Base:
    def __init__(self):
        self._mappings: Dict[str, str] = {}
        self._serialize_skip: List[str] = ["_mappings", "_serialize_skip"]

    def to_dict(self) -> Dict[str, str]:
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    data.update(self._normalize(key, item))
            else:
                data.update(self._normalize(key, value))

        return data

    def _normalize(self, key: str, value: Optional[str]) -> Dict[str, str]:
        if value is None:
            return {}

        if hasattr(value, "to_dict"):
            return value.to_dict()
        else:
            mapped_key = self._mappings.get(key, key)
            return {mapped_key: str(value)}


class Resource(__Base):
    def __init__(self):
        super().__init__()
        self._diff_skip: List[str] = []
        self._serialize_skip.extend(["_diff_skip"])

    def __normalize(self, key: str, value: Optional[str]) -> Dict[str, str]:
        if value is None:
            return {}

        if hasattr(value, "serialize"):
            return value.serialize()
        else:
            mapped_key = self._mappings.get(key, key)
            return {mapped_key: str(value)}

    def serialize(self) -> Dict[str, str]:
        data = {}
        for key, value in self.__dict__.items():
            if key in self._serialize_skip:
                continue

            if isinstance(value, list):
                for item in value:
                    data.update(self.__normalize(key, item))
            else:
                data.update(self.__normalize(key, value))

        return data

    def diff(self, other: Optional["Resource"]) -> Dict[str, str]:
        diff: Dict[str, str] = {}
        serialized_other = other.serialize() if other else {}
        for key, value in self.serialize().items():
            if value is None or key in self._diff_skip:
                continue

            other_value = serialized_other.get(key, None)
            if other_value is None or value.strip() != serialized_other.get(key, None).strip():
                diff[key] = value

        return diff


class ResourceField(__Base):
    def __init__(self, name: str, idx: Optional[int] = None):
        super().__init__()
        self._name = name
        self.idx = idx
        self._serialize_skip.extend(["idx", "_name"])

    def serialize(self) -> Dict[str, str]:
        params = []
        for key, value in self.__dict__.items():
            if key in self._serialize_skip:
                continue

            mapped_key = self._mappings.get(key, key)
            if value:
                params.append(f"{mapped_key}={value}")

        key = self._name
        if self.idx is not None:
            key = f"{key}{self.idx}"

        return {key: ",".join(params)}
