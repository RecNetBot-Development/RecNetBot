from typing import Generator, List, Any

def chunks(list: list, n: int) -> Generator[List, Any, Any]:
    """
    Splits a list into n chunks
    """
        
    for i in range(0, len(list), n):
        yield list[i:i + n]