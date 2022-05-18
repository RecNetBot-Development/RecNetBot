def resolve_identities(x):
    identities = ['LGBTQIA', 'Transgender', 'Bisexual', 'Lesbian', 'Pansexual', 'Asexual', 'Intersex', 'Genderqueer', 'Nonbinary', 'Aromantic']
    for index, identity in enumerate(identities):
        if 1 << index & x:
            yield identity