# Introduction to Adiantum - A New Encryption Method for Low-End Devices

# Introduction:
- Adiantum is a new encryption method designed for low-end devices that do not have hardware support for AES encryption.
- Adiantum was developed by Google and aims to provide strong encryption while remaining lightweight and efficient.

### Adiantum's Advantages:
- Adiantum is up to 5 times faster than existing software encryption methods like ChaCha20.
- Adiantum uses a new cryptographic primitive called the "XChaCha12 stream cipher" which provides strong encryption while remaining lightweight.
- Adiantum is resistant to side-channel attacks which can compromise other encryption methods.

### Adiantum in Android:
- Adiantum has been added to Android 10 as a standard encryption method for low-end devices.
- Adiantum is also expected to be included in future versions of Android.
- Adiantum is a preferred encryption method for the "next billion users" who may not have access to high-end devices.

### Comparison with AES:
- Adiantum is not meant to replace AES encryption, which is still the preferred method for high-end devices.
- Adiantum is specifically designed to provide strong encryption on low-end devices without AES hardware support.

### Conclusion:
- Adiantum is a promising new encryption method that addresses the need for strong encryption on low-end devices.
- Adiantum is a lightweight and efficient alternative to existing software encryption methods.
- Adiantum has been included in Android 10 and is expected to be included in future versions of Android.


### Here are the steps to implement the NH and Poly1305 algorithms according to the paper "Adiantum Encryption Scheme Implementation":

#### NH Algorithm:

1. Define the NH constants, which are 4 64-bit unsigned integers.
2. Define the NH state, which is a 32-byte array.
3. Initialise the NH state to the NH constants.
4. For each 32-byte block of input data, XOR the block with the NH state and then apply 4 rounds of the NH mixing function.
5. XOR the final NH state with the last incomplete block of input data.
6. Return the final NH state.

#### Poly1305 Algorithm:

1. Define the Poly1305 key and nonce, which are 256-bit and 128-bit unsigned integers, respectively.
2. Define the Poly1305 state, which is a 17-byte array.
3. Set the first 16 bytes of the Poly1305 state to the nonce.
4. Calculate the Poly1305 r value as the first 128 bits of the Poly1305 key.
5. Calculate the Poly1305 s value as the last 128 bits of the Poly1305 key.
6. Initialise the Poly1305 state's accumulator to 0.
7. For each 16-byte block of input data, add the block to the accumulator and then multiply the accumulator by r.
8. Reduce the accumulator modulo s using the carry-save reduction algorithm.
9. Add the s value to the reduced accumulator.
10. Return the final 16 bytes of the accumulator as the Poly1305 tag.
