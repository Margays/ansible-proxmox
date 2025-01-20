from typing import Any, Dict, Optional, List
from ...resource import Resource
from .....utils import load_objs_from_list


class Node:
    
    def __init__(self, data: Dict[str, Any]):
        self.name: Optional[str] = data.get('name', None)
        self.priority: Optional[str] = data.get('priority', None)

    def __str__(self):
        value = self.name
        if self.priority is not None:
            value += f":{self.priority}"

        return value


class Nodes:

    def __init__(self, data: List[Dict[str, Any]]):
        self.nodes: List[Node] = []
        match type(data).__name__:
            case "list":
                self._load_from_list(data)
            case "str":
                self._load_from_str(data)
            case _:
                raise ValueError(f"Invalid type for nodes: {type(data)}")

    def _load_from_list(self, data: List[Dict[str, Any]]):
        self.nodes.extend(load_objs_from_list(data, Node))

    def _load_from_str(self, data: str):
        for node in data.split(','):
            parts = node.split(':')
            if len(parts) == 1:
                self.nodes.append(Node({'name': parts[0]}))
            elif len(parts) == 2:
                self.nodes.append(Node({'name': parts[0], 'priority': parts[1]}))
            else:
                raise ValueError(f"Invalid format for nodes: {data}")

    def __str__(self):
        return ','.join([str(node) for node in self.nodes])


class ClusterHAGroup(Resource):

    def __init__(self, data: Dict[str, Any]):
        super().__init__()
        self.group: Optional[str] = data.get('group', None)
        self.nodes = Nodes(data.get('nodes', []))
        self.comment: Optional[str] = data.get('comment', None)
        self.nofailback: Optional[str] = data.get('nofailback', None)
        self.restricted: Optional[str] = data.get('restricted', None)
        self.type: Optional[str] = data.get('type', None)
