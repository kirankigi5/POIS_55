'''
NH Algorithm:
Define the NH constants, which are 4 64-bit unsigned integers.
Define the NH state, which is a 32-byte array.
Initialise the NH state to the NH constants.
For each 32-byte block of input data, XOR the block with the NH state and then apply 4 rounds of the NH mixing function.
XOR the final NH state with the last incomplete block of input data.
Return the final NH state.
'''

import sys
# import os
import struct
import binascii

# NH constants
NH_CONSTANTS = [0x6c7967656e657261, 0x7465646279746573, 0x6c7967656e657261, 0x7465646279746573]

# NH mixing function
def nh_mixing_function(state):
    state[0] += state[1]
    state[1] = (state[1] << 13) | (state[1] >> 51)
    state[1] ^= state[0]
    state[0] = (state[0] << 32) | (state[0] >> 32)
    state[2] += state[3]
    state[3] = (state[3] << 16) | (state[3] >> 48)
    state[3] ^= state[2]
    state[0] += state[3]
    state[3] = (state[3] << 21) | (state[3] >> 43)
    state[3] ^= state[0]
    state[2] += state[1]
    state[1] = (state[1] << 17) | (state[1] >> 47)
    state[1] ^= state[2]
    state[2] = (state[2] << 32) | (state[2] >> 32)

# NH algorithm

# def nh(data):
#     # Initialise the NH state to the NH constants
#     state = NH_CONSTANTS[:]
#     # For each 32-byte block of input data
#     for i in range(0, len(data), 32):
#         # XOR the block with the NH state
#         state = [state[j] ^ struct.unpack('<Q', data[i + 8 * j:i + 8 * j + 8])[0] for j in range(4)]
#         # Apply 4 rounds of the NH mixing function
#         for j in range(4):
#             nh_mixing_function(state)
#     # XOR the final NH state with the last incomplete block of input data
#     if len(data) % 32 != 0:
#         state = [state[j] ^ struct.unpack('<Q', data[-(len(data) % 32) + 8 * j:-(len(data) % 32) + 8 * j + 8])[0] for j in range(4)]
#     # Return the final NH state
#     return b''.join(struct.pack('<Q', state[j]) for j in range(4))

def nh(data):
    # Initialise the NH state to the NH constants
    state = NH_CONSTANTS[:]
    # For each 32-byte block of input data
    for i in range(0, len(data), 32):
        # XOR the block with the NH state
        state = [state[j] ^ struct.unpack('<Q', data[i + 8 * j:i + 8 * j + 8])[0] for j in range(4)]
        # Apply 4 rounds of the NH mixing function
        for j in range(4):
            nh_mixing_function(state)
    # XOR the final NH state with the last incomplete block of input data
    if len(data) % 32 != 0:
        state = [state[j] ^ struct.unpack('<Q', data[-(len(data) % 32) + 8 * j:-(len(data) % 32) + 8 * j + 8])[0] for j in range(4)]
    # Truncate each NH state value to 64 bits
    state = [(s & 0xFFFFFFFFFFFFFFFF) for s in state]
    # Return the final NH state
    return b''.join(struct.pack('<Q', s) for s in state)


# Test vectors

def test_vectors():
    print('Test vectors:')
    for i in range(1, 11):
        with open('testvectors/testvector' + str(i) + '.txt', 'rb') as f:
            data = f.read()
        print('Test vector ' + str(i) + ': ' + binascii.hexlify(nh(data)).decode('ascii'))

# Main

def main():
    if len(sys.argv) == 1:
        print('Usage: python3 NH.py [file]')
        print('If no file is specified, the test vectors are used.')
        return
    with open(sys.argv[1], 'rb') as f:
        data = f.read()
    print('NH: ' + binascii.hexlify(nh(data)).decode('ascii'))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        test_vectors()
    else:
        main()

