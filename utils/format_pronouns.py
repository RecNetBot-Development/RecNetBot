from typing import List

def format_pronouns(pronouns: List[str]) -> str:
    """
    Formats pronouns to keep them concise.
    """
    if not pronouns: return None
    
    if len(pronouns) == 1:
        split_pronouns = pronouns[0].split(' / ')
        return f"`{split_pronouns[0]}` / `{split_pronouns[1]}`"
    
    first_part_pronouns = []
    for ele in pronouns:
        first_part_pronouns.append(f"`{ele.split(' / ')[0]}`")
        
    return ' / '.join(first_part_pronouns)