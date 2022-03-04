def resolve_platforms(x):
    platforms = ['Steam', 'Oculus', 'PlayStation', 'Xbox', 'HeadlessBot', 'iOS', 'Android']
    for index, platform in enumerate(platforms):
        if 1 << index & x:
            yield platform