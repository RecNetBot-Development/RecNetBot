from typing import Generator, List

def chunks(list: list, n: int) -> Generator[List]:
    """
    Splits a list into n chunks
    """
        
    for i in range(0, len(list), n):
        yield list[i:i + n]