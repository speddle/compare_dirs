#! /usr/bin/python3
import glob
import sys
import os
import hashlib
from pathlib import Path

path_ref = {}
hash_ref = frozenset()
path_dut = {}
hash_dut = frozenset()

# BUF_SIZE is totally arbitrary, change for your app!
#print("MD5: {0}".format(md5.hexdigest()))
#print("SHA1: {0}".format(sha1.hexdigest()))

def tree_hasher(dir):
    pathdict = {}
    filehash = set()
    for filename in glob.iglob(f"{dir}/**/*", recursive = True):
        #print("GOB", filename)
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()

        try:
            with open(filename, 'rb') as f:
                BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    md5.update(data)
                    sha1.update(data)
            mdtxt= md5.hexdigest()
            #print("MD5: {0}".format(md5.hexdigest()))
            #print(mdtxt, filename)
            filehash.add(mdtxt)
            pathdict[mdtxt]=filename
        except:
            pass
    return filehash, pathdict

def main(dir_ref,dir_dut):

    print("hashing LEFT ...")
    hash_ref, path_ref = tree_hasher(dir_ref)
    print("hashing RIGHT ...")
    hash_dut, path_dut = tree_hasher(dir_dut)

    right_only= hash_dut.difference(hash_ref)
    for item in right_only:
        print("RIGHT ONLY {0}".format(item), path_dut[item])
    left_only = hash_ref.difference(hash_dut)
    for item in left_only:
        print(" LEFT ONLY {0}".format(item), path_ref[item])

    print()
    print(f" LEFT total files: {len(hash_ref)}    LEFT ONLY files: {len(left_only)}")
    print(f"RIGHT total files: {len(hash_dut)}   RIGHT ONLY files: {len(right_only)}")


main(sys.argv[1], sys.argv[2])
