import os, random, sys, struct
from Crypto.Cipher import AES


def generate_iv(block):
    iv = ''.join(chr(random.randint(0,255)) for i in range(block))
    return iv

def pad(string, blocksize):
    string += ' '*(blocksize - len(string)%blocksize)
    return string

def encrypt_file(key, infilename, outfilename = None, chunksize = 256*256, block = 16):

    if not outfilename:
        outfilename = infilename + '.enc'

    iv = generate_iv(block)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(infilename)

    with open(infilename, 'rb') as infile:
        with open(outfilename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk = pad(chunk,block)

                outfile.write(encryptor.encrypt(chunk))

    return outfilename

def decrypt_file(key, infilename, outfilename = None, chunksize = 256*256, block = 16):

    if not outfilename:
        outfilename = os.path.splitext(infilename)[0]

    with open(infilename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(outfilename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                if (len(chunk)%16) :
                    print(origsize)

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

    return outfilename
