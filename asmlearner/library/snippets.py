import os
import binascii

def save_snippet(owner, filename, code):
    owner_encoded = binascii.hexlify( bytes(owner, 'utf-8') ).decode('utf-8')
    snippet_dir = 'data/snippets/' + owner_encoded
    snippet_path = os.path.join(snippet_dir, filename)

    if os.path.isdir(snippet_dir) == False:
        os.makedirs(snippet_dir)
    f = open(snippet_path, 'wb')
    f.write(bytes(code, 'utf-8'))

    f.close()

    return f


