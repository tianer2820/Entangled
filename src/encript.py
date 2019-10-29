#!/usr/bin/python3

import os


def encrypt(clear_text: bytes, key: bytes):
    """
    This function do bit-wise inverse base on the key.

    :return: a bytes object that contains the result.
    """

    assert len(clear_text) == len(key)
    result = b''
    for i in range(len(clear_text)):
        k = key[i]
        sum_value = clear_text[i] + k
        bit_and = clear_text[i] & k
        bit_shifted = bit_and << 1

        inverse = bytes([sum_value - bit_shifted])
        result += inverse
    return result
