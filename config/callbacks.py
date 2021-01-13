def config():
    import os
    try:
        callbacks = os.environ['CALLBACKS'].split(';')
        cfg = []
        for url in callbacks:
            cfg.append(url)

        return cfg
    except KeyError as e:
        pass
    return []
