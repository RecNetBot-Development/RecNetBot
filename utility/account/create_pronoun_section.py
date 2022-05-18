def create_pronoun_section(pronoun_list):
    if not pronoun_list: return None
    
    if len(pronoun_list) == 1:
        split_pronouns = pronoun_list[0].split(' / ')
        return f"`{split_pronouns[0]}` / `{split_pronouns[1]}`"
    
    first_part_pronouns = []
    for pronoun in pronoun_list:
        first_part_pronouns.append(f"`{pronoun.split(' / ')[0]}`")
        
    return ' / '.join(first_part_pronouns)