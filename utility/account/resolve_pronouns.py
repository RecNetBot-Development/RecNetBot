def resolve_pronouns(x):
    pronouns = ['She / her', 'He / him', 'They / them', 'Ze / hir', 'Ze / zir', 'Xe / xem']
    for index, pronoun in enumerate(pronouns):
        if 1 << index & x:
            yield pronoun