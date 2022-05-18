def resolve_platforms(x):
    platforms = ['Steam', 'Meta', 'PlayStation', 'Xbox', 'RecNet', 'iOS', 'Android', 'Standalone']
    for index, platform in enumerate(platforms):
        if 1 << index & x:
            yield platform