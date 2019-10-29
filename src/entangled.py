"""
Main program
"""

from encript import encrypt
from key_gen import generate_key
from key_management import read_key_info, write_key_info
import os
import re


def realtime_mode(args):
    keyname = args[0]

    if not os.path.isfile(keyname + '.qkey'):
        print('can\'t find key')
        return
    if os.path.isfile(keyname + '.qkeyinfo'):
        shift = read_key_info(keyname)['cursor']
    else:
        shift = 0

    with open(keyname + '.qkey', mode='rb') as f:
        f.seek(shift)
        print('entered realtime mode, use \'\\exit\' to quit')

        while True:
            t = input('> ')
            if t == '\\exit':
                break
            elif t[0] == '\\':  # if input is ciphertext
                m = re.match('\\\\(.+):(.+):(.+)', t)
                g = m.groups()
                decryption_key = g[0]
                decryption_shift = int(g[1])
                ciphertext = g[2]

                plaintext = []  # convert to bytes
                assert len(ciphertext) % 2 == 0
                i = 0
                while i < len(ciphertext):
                    c = ciphertext[i:i+2]
                    plaintext.append(int(c, 16))
                    i += 2
                plaintext = bytes(plaintext)

                if not os.path.isfile(decryption_key + '.qkey'):
                    print('can\'t find key')
                    continue
                with open(decryption_key + '.qkey', 'rb') as key:  # open key file and decrypt
                    key.seek(decryption_shift)
                    key_bytes = key.read(len(plaintext))
                    plaintext = encrypt(plaintext, key_bytes)
                    print(plaintext.decode('utf8'))

            else:  # if input is plain text
                t = t.encode('utf8')
                key_bytes = f.read(len(t))
                if len(key_bytes) < len(t):
                    print("Runing out of keys!")
                    return
                miwen = encrypt(t, key_bytes)
                print('\\' + keyname + ':' + str(f.tell() - len(t)) + ':' + miwen.hex())
        write_key_info(keyname, f.tell())


def file_mode(args):
    print('unimplemented yet, please use realtime mode')
    '''
    if len(args) == 2:
        # decryption mode
        source = args[0]
        outdir = args[1]
    elif len(args) == 3:
        # encryption mode
        source = args[0]
        keyname = args[1]
        outdir = args[2]

    else:
        raise ValueError('you must provide 1 or 2 arguments for file mode')
    '''
    return


def keygen_mode(args):
    outdir = args[0]
    size = args[1].lower()

    m = re.match('([0-9]+)(kb|mb|gb)?', size) # look for unit
    g = m.groups()
    assert len(g) == 2
    if g[1] is None:
        multiplier = 1
    elif g[1] == 'kb':
        multiplier = 1
    elif g[1] == 'mb':
        multiplier = 1024
    elif g[1] == 'gb':
        multiplier = 1024 ** 2
    else:
        print('Unknown unit, must be kb, mb or gb')
        return
    size = int(g[0]) * multiplier

    if os.path.isfile(outdir):
        ans = input('file exists, overwrite? [Y/N]:\n')
        if ans.upper() == 'N':
            return
    try:
        generate_key(size, outdir)
    except FileNotFoundError:
        print('dir not exist!')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--realtime', '-r', action='store', nargs=2, metavar=('KEY_NAME', 'KEY_SHIFT'), help='enter the realtime mode')
    parser.add_argument('--encrypt', '-e', action='store', nargs=3, metavar=('FILE', 'KEY_NAME', 'OUT_DIR'), help='encrypt a file')
    parser.add_argument('--decrypt', '-d', action='store', nargs=2, metavar=('FILE', 'OUT_DIR'), help='decrypt a file')
    parser.add_argument('--keygen', '-k', action='store', nargs=2, metavar=('KEY_NAME', 'KEY_SIZE'), help='generate a key file')

    args = parser.parse_args()

    if args.realtime:
        print('Entered RealTime mode')
        realtime_mode(args.realtime)
        exit(0)
    elif args.encrypt:
        file_mode(args.encrypt)
    elif args.decrypt:
        file_mode(args.decrypt)
    elif args.keygen:
        keygen_mode(args.keygen)
    else:
        print('At least one mode should be specified, use -h to get more help')
