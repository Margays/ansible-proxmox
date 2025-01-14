from typing import Dict


class BaseProxmoxResource:
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
            if key.startswith('_'):
                continue

            if key == 'idx':
                idx = value
                continue

            if value:
                params.append(f"{key}={value}")

        return {f"{self._resource}{idx}": ",".join(params)}
