from asmlearner.config import config

import os


def save_snippet(owner, filename, code):
    owner_encoded = str(owner.id)
    snippet_dir = os.path.join(config.SNIPPET_PATH, owner_encoded)
    snippet_path = os.path.join(snippet_dir, filename)

    if not os.path.isdir(snippet_dir):
        os.makedirs(snippet_dir)
    f = open(snippet_path, 'wb')
    f.write(code)

    f.close()

    return f
