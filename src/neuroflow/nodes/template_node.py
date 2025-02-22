from typing import Any, Callable, Dict

def node_template(partitions: Dict[str, Callable[[], Any]], parameters: dict = {}) -> Dict:
    return partitions