from typing import Any, Callable, Dict

def node_template(partitions: Dict[str, Callable[[], Any]], parameters: dict = {}) -> Dict:
    """
    
    :meta private:
    
    """
    return partitions