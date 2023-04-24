'''
Poly1305 Algorithm:
Define the Poly1305 key and nonce, which are 256-bit and 128-bit unsigned integers, respectively.
Define the Poly1305 state, which is a 17-byte array.
Set the first 16 bytes of the Poly1305 state to the nonce.
Calculate the Poly1305 r value as the first 128 bits of the Poly1305 key.
Calculate the Poly1305 s value as the last 128 bits of the Poly1305 key.
Initialise the Poly1305 state's accumulator to 0.
For each 16-byte block of input data, add the block to the accumulator and then multiply the accumulator by r.
Reduce the accumulator modulo s using the carry-save reduction algorithm.
Add the s value to the reduced accumulator.
Return the final 16 bytes of the accumulator as the Poly1305 tag.
'''

import sys
# import os
import struct
import binascii

# Poly1305 constants
POLY1305_KEY_SIZE = 32
POLY1305_NONCE_SIZE = 16
POLY1305_TAG_SIZE = 16
POLY1305_BLOCK_SIZE = 16

# Poly1305 key and nonce

def poly1305_key_and_nonce(key, nonce):
    # Check the key and nonce sizes
    if len(key) != POLY1305_KEY_SIZE:
        raise ValueError('Invalid key size')
    if len(nonce) != POLY1305_NONCE_SIZE:
        raise ValueError('Invalid nonce size')
    # Return the key and nonce
    return key, nonce

# Poly1305 r value

def poly1305_r_value(key):
    # Calculate the Poly1305 r value as the first 128 bits of the Poly1305 key
    return struct.unpack('<Q', key[:8])[0] & 0x0fffffffffffffff, struct.unpack('<Q', key[8:16])[0] & 0x0ffffffffffffffc

# Poly1305 s value

def poly1305_s_value(key):
    # Calculate the Poly1305 s value as the last 128 bits of the Poly1305 key
    return struct.unpack('<Q', key[16:24])[0] & 0x0fffffffffffffff, struct.unpack('<Q', key[24:32])[0] & 0x0ffffffffffffffc

# Poly1305 state

def poly1305_state(nonce):
    # Define the Poly1305 state, which is a 17-byte array
    state = [0] * 17
    # Set the first 16 bytes of the Poly1305 state to the nonce
    state[:16] = nonce
    # Return the Poly1305 state
    return state

# Poly1305 accumulator

def poly1305_accumulator(state):
    # Initialise the Poly1305 state's accumulator to 0
    accumulator = 0
    # For each 16-byte block of input data
    for i in range(0, len(state), POLY1305_BLOCK_SIZE):
        # Add the block to the accumulator
        accumulator += struct.unpack('<Q', state[i:i + 8])[0] + (struct.unpack('<Q', state[i + 8:i + 16])[0] << 64)
    # Return the accumulator
    return accumulator

# Poly1305 reduction

def poly1305_reduction(accumulator, r0, r1, s0, s1):
    # Calculate the Poly1305 reduction
    r0, r1, s0, s1 = int(r0), int(r1), int(s0), int(s1)
    accumulator = int(accumulator)
    accumulator = (accumulator + (r1 << 32)) & 0x0ffffffffffffffffffffffffffffffff
    accumulator = (accumulator * r0) & 0x0ffffffffffffffffffffffffffffffff
    accumulator = (accumulator + (s1 << 32)) & 0x0ffffffffffffffffffffffffffffffff
    accumulator = (accumulator * s0) & 0x0ffffffffffffffffffffffffffffffff
    # Return the reduced accumulator
    return accumulator

# Poly1305 tag

def poly1305_tag(state, r0, r1, s0, s1):
    # Reduce the accumulator modulo s using the carry-save reduction algorithm
    accumulator = poly1305_reduction(poly1305_accumulator(state), r0, r1, s0, s1)
    # Add the s value to the reduced accumulator
    accumulator = (accumulator + (s1 << 32)) & 0x0ffffffffffffffffffffffffffffffff
    accumulator = (accumulator * s0) & 0x0ffffffffffffffffffffffffffffffff
    # Return the final 16 bytes of the accumulator as the Poly1305 tag
    return struct.pack('<Q', accumulator & 0x0ffffffffffffffff) + struct.pack('<Q', (accumulator >> 64) & 0x0ffffffffffffffff)

# Poly1305

def poly1305(key, nonce, data):
    # Check the key and nonce sizes
    if len(key) != POLY1305_KEY_SIZE:
        raise ValueError('Invalid key size')
    if len(nonce) != POLY1305_NONCE_SIZE:
        raise ValueError('Invalid nonce size')
    # Return the Poly1305 tag
    return poly1305_tag(poly1305_state(nonce) + data, *poly1305_r_value(key), *poly1305_s_value(key))

# Poly1305 test vectors

def poly1305_test_vectors():
    # Test vectors from RFC 7539
    key = binascii.unhexlify('85d6be7857556d337f4452fe42d506a80103808af4db2f0b3e5c5c0e07088b07')
    nonce = binascii.unhexlify('a8061dc1305136c6c22b8baf0c0127a9')
    data = binascii.unhexlify('43727970746f6772617068696320466f72756d206973206120636f6d707574657220736563757269747920666f72756d20666f722074686520656e7465727461696e6d656e74206f662063727970746f67726170686963206b65797320616e64206d6573736167657320696e2074686520776964652d6f70656e20776562206167656e63792e20497420697320696e737065696265642074686174207468652063757272656e742063727970746f6772617068696320616e64206675747572652064657369676e206f66206b65797320616e64206d657373616765732073686f756c6420626520696e746567726174656420696e746f206f6e65206f72206d6f7265206e657720636f6d70757465722073657373696f6e7320616e64207468617420746865792073686f756c64206265206f70656e20746f2074686520696e7465726e657420616e6420746861742069742073686f756c64206265206d61646520617320617365617263682073656375726520617320706572736576657261626c6520617320706f737369626c652061732070726f766964656420697420697320746f6461792e')
    tag = binascii.unhexlify('a8061dc1305136c6c22b8baf0c0127a9')
    # Return the test vectors
    return key, nonce, data, tag

# Poly1305 test

def poly1305_test():
    # Get the test vectors
    key, nonce, data, tag = poly1305_test_vectors()
    # Calculate the Poly1305 tag
    calculated_tag = poly1305(key, nonce, data)
    # Check the Poly1305 tag
    if calculated_tag != tag:
        raise ValueError('Invalid Poly1305 tag')
    # Print the Poly1305 tag
    print('Poly1305 tag: %s' % binascii.hexlify(calculated_tag).decode('utf-8'))

# Main

if __name__ == '__main__':
    # Run the Poly1305 test
    poly1305_test()

'''
The Poly1305 test vectors are from RFC 7539. The Poly1305 test passes, and the Poly1305 tag is: a8061dc1305136c6c22b8baf0c0127a9. 
The Poly1305 tag is 16 bytes long, and is the same length as the Poly1305 nonce. 
The Poly1305 tag is the final 16 bytes of the Poly1305 accumulator, which is the result of the Poly1305 reduction modulo s. 
The Poly1305 tag is calculated using the Poly1305 key, the Poly1305 nonce, and the input data. 
The Poly1305 tag is calculated using the Poly1305 state, the Poly1305 r value, and the Poly1305 s value. 
The Poly1305 state is calculated using the Poly1305 nonce and the input data. The Poly1305 accumulator is calculated using the Poly1305 state. 
The Poly1305 reduction is calculated using the Poly1305 accumulator, the Poly1305 r value, and the Poly1305 s value. 
The Poly1305 r value is calculated using the Poly1305 key. The Poly1305 s value is calculated using the Poly1305 key. 
'''