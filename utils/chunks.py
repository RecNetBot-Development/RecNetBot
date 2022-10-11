def chunks(list: list, n: int) -> list:
    """
    Splits a list into n chunks
    """
        
    for i in range(0, len(list), n):
        yield list[i:i + n]