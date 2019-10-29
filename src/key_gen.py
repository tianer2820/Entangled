import random
from key_management import write_key_info


def generate_key(length: int, out_file_name):
    """
    generate a random key, length in kilobytes
    """

    with open(out_file_name + '.qkey', 'wb') as f:
        for i in range(length):
            f.write(bytes([random.randint(0, 255) for j in range(1024)]))
    write_key_info(out_file_name)


