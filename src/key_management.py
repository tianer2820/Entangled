
def write_key_info(key_name: str, cursor: int=0):
    with open(key_name + '.qkeyinfo', 'w') as f:
        f.write('cursor: ' + str(cursor) + '\n')


def read_key_info(key_name: str):
    with open(key_name + '.qkeyinfo') as f:
        content = f.read()
    lines = content.splitlines()
    ret = {}
    for line in lines:
        line = line.replace(' ', '')
        if line == '':
            break
        words = line.split(':')

        if words[0] == 'cursor':
            ret['cursor'] = int(words[1])
    return ret
