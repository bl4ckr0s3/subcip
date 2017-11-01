"""
simple substitution cipher program. PoC.
"""
import string
import sys
import os
from cipKeys import *


# some other input lists
action_input_list = ['f', 'p', 'q']
action_mode_list = ['e', 'd', 'q']

def main():
    print("------------------------------------")
    print("Welcome to bl4ckr0s3's subCipher encryptor")
    print("------------------------------------\n\n")

    ### ensure proper input
    while True:
        action_input = input("Type 'f' for a file or 'p' for a phrase or 'q' to quit: ")
        if action_input in action_input_list:
            if action_input == 'q':
                sys.exit(0)
            print()
            break
        else:
            print("Try again.")
    while True:
        action_mode = input("\nType 'e' for encrypt or 'd' for decrypt or 'q' to quit: ")
        if action_mode in action_mode_list:
            if action_mode == 'q':
                sys.exit(0)
            print()
            break
        else:
            print("Try again.")

    ### perform the en/decryption
    # if input is an entire file
    if action_input == 'f':
        while True:
                infile_path = input("\nEnter path + filename or 'q' to quit: ")

                # read from the file and store contents into a single 'phrase'
                if infile_path == 'q':
                    sys.exit(0)
                phrase=""
                try:
                    with open(infile_path, 'r') as infile:
                        for line in infile:
                            phrase += str(line)
                    break
                except FileNotFoundError:
                    print("File Not found. Try again")
    # if input is already a phrase
    else:
        while True:
            phrase = input("\nEnter the phrase: ")
            # something must be entered
            if phrase != '':
                break

    ## encrypt
    if action_mode == 'e':
        while True:
            key = input("\nEnter 'rot13' for rot13. 'tres' for tres letras: ")
            if key in key_list:
                key = eval(key) # turn the parsed string to a key variable
                break
            else:
                print("Try again")
        print("--------------------------------------------------------")
        print("Encrypting...")
        outString = subCipher_encrypt(phrase, key)

        ### write out the encrypted text to a unique file ~/Documents/cip-output/out[x]
        write_out(outString)


    ## decrypt
    if action_mode == 'd':
        while True:
            key = input("\nEnter 'rot13' for rot13. 'tres' for tres letras: ")
            if key in ['rot13', 'tres']:
                # tres uses a different shift
                if key == 'tres':
                    shift = 3
                else:
                    shift = 1
                key = eval(key) # turn the parsed string to a key variable
                break
            else:
                print("Try again")
        print("--------------------------------------------------------")
        print("Obtaining decryption key...")
        decryptKey = decryptKey_generator(key)

        print("Decrypting...")
        outString = subCipher_decrypt(phrase, decryptKey, shift)

        ### write out the encrypted text to a unique file ~/Documents/cip-output/out[x]
        write_out(outString)

    ### success
    return 0


def subCipher_encrypt(phrase, key):
    """
    Takes a string phrase and encrypts its letters using any letter substitution dictionary
    key. Assumes the key pairs are in uppercase
    """
    inList = [] #list that will place hold the input to be encrypted

    for c in phrase:
        c = c.upper()
        inList += [c]

    outList = inList[:] #copy of the list to be crypted
    i = 0 #index for substitution cypher
    for c in inList:
        if c in string.ascii_letters: #only letters will be substituted
            i = inList.index(c, i)
            outList[i] = key[c] #substitution

    for c in outList:
        outString = "".join(outList)
    return outString


def decryptKey_generator(key):
    """ helper function to reverse the encryption key-value pairs for decryption"""
    deKey = {} #dict to hold the decryption key
    tmpList = list(key) #list to hold the keys of the encrypt key
    for k in tmpList:
        deKey[key[k]] = k
    return deKey


def subCipher_decrypt(phrase, key, shift=1):
    """
    Takes a phrase and decrypts it according to given decryption key.
    shift is the number of letters in the key that the function shifts over w.r.t the key
    default shift == 1 for single character substitutions.
    Assumes the keys are always in uppercase.
    """
    inList = [] #to hold the encrypted phrase
    outList = [] #to hold the decrypted phrase

    for c in phrase:
        inList += [c.upper()]

    seek = 0 #seek through the encrypted characters
    indx = 0 #keep track of the decrypted characters in the outList
    while seek < len(inList):
        try:
            if inList[seek] in string.ascii_letters:
                outList.append(key["".join(inList[seek:seek+shift])])
                seek += shift
                indx += 1
            else: #for non alpha characters that aren't encrypted
                outList.append(inList[seek])
                seek += 1
                indx += 1
        except IndexError: # beyond end of list
            break
    return "".join(outList)


def write_out(outString):
    """
    writes out the result of the en/decryption into to a unique file:
     ~/Documents/cip-output/out[x] starting with out1. Returns 0.
    """
    print("Preparing output file...")
    indx = 1
    base_path = "~/Documents/cip-output/"
    ## if file exists, don't overwrite
    # create base directory if it doesn't exist
    try:
        os.mkdir(base_path)
    except FileExistsError:
        pass
    # now create a new file out[x]
    while True:
        if os.path.isfile(base_path + "out" + str(indx)):
            indx += 1
        else:
            print("Writing to output file...")
            outfile_path = base_path + "out" + str(indx)
            with open(outfile_path, 'w+') as outFile:
                outFile.write(outString)
            break
    print("Done! Check the file: " + outfile_path)
    print("--------------------------------------------------------")
    return 0



if __name__ == "__main__":
    main()
