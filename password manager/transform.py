# plaintext = "Hello world This is some sample text !"
#
#
# key = [plaintext[0]]
# counter = 1
# i = 0
#
# while counter != 16:
#     key.append(plaintext[(i+i//2)%len(plaintext)])
#     i +=9
#     counter += 1
#
#
# print(len(key))
# print("".join(key))
#
#


def convertpass(plaintext):
    key = [plaintext[0]]
    counter = 1
    i = 0
    while counter != 16:
        key.append(plaintext[(i+i//2)%len(plaintext)])
        i += 9
        counter += 1
    return "".join(key)

def convertToMUL8(m):
    length = len(m)
    spaces = length % 8
    spaces = 8 - spaces
    return m + " "*spaces

def convertToOriginal(ciphertext):
    return ciphertext.rstrip()
