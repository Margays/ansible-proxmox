from typing import Dict


class BaseProxmoxResource:
    def __init__(self):
        self._mappings = {}
        self._serialize_skip = ['_mappings', '_serialize_skip']

    def to_dict(self) -> Dict[str, str]:
        data = {}
        for key, value in self.__dict__.items():
            if hasattr(value, 'to_dict'):
                data.update(value.to_dict())
            else:
                data[key] = value

        return data

    def serialize(self) -> Dict[str, str]:
        params = []
        idx = ""
        for key, value in self.__dict__.items():
            if key in self._serialize_skip:
                continue

            if key == 'idx':
                idx = value
                continue

            mapped_key = self._mappings.get(key, key)
            if value:
                params.append(f"{mapped_key}={value}")

        return {f"{self._resource}{idx}": ",".join(params)}
