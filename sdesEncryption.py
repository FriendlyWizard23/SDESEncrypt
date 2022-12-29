CHUNKSIZE=12
NUMROUNDS=3
KEYMATERIAL=[]
CHUNKEDPLAINTEXT=[]
ENCRYPTED=[]
SBOX1=[["101","010","001","110","011","100","111","000"],["001","100","110","010","000","111","101","011"]]
SBOX2=[["100","000","110","101","111","001","011","010"],["101","011","000","011","110","010","001","100"]]

def rotate(str,d):
   Lfirst = str[0 : d]
   Lsecond = str[d :]
   Rfirst = str[0 : len(str)-d]
   Rsecond = str[len(str)-d : ]
   return Lsecond + Lfirst

def generatekeymaterial(key):
    KEYMATERIAL.append(key[0:len(key)-1])
    for i in range(0,NUMROUNDS):
        key=rotate(key,1)
        KEYMATERIAL.append(key[0:len(key)-1])

def tobinary(str):
    return ''.join(format(ord(i), '08b') for i in str)

def generatechunks(binplaintext):
    #padding cicle
    while(len(binplaintext)%CHUNKSIZE!=0):
        binplaintext+="0"
    blocks=len(binplaintext)//CHUNKSIZE
    for i in range(0,blocks):
        CHUNKEDPLAINTEXT.append(binplaintext[i*CHUNKSIZE:(i+1)*CHUNKSIZE])

def xor(first, second):
    xored = ""
    for i in range(len(second)):
        if (first[i] == second[i]):
            xored += "0"
        else:
            xored += "1"
    return xored

def binaryToDecimal(binary):
    binary=int(binary,2)
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

def expand(str):
    expanded=str[0:2]
    expanded+=str[3]
    expanded+=str[2]
    expanded+=str[3]
    expanded+=str[2]
    expanded+=str[4:6]
    return expanded

def DESRound(plaintext,roundnumber):
    print("****************************************************")
    print("DES ROUND NUMBER: ["+str(roundnumber+1)+"]")
    print("****************************************************")
    print("plaintext: "+plaintext)
    print("current key: "+KEYMATERIAL[roundnumber])
    left=plaintext[0:CHUNKSIZE//2]
    right=plaintext[6:CHUNKSIZE]
    print("Left: "+left)
    print("Right: "+right)
    expanded=expand(right)
    print("(1) Expanding right: "+expanded)
    xored=xor(expanded,KEYMATERIAL[roundnumber])
    print("(2) Xoring right with the key: "+xored)
    p1=xored[0:4]
    p2=xored[4:8]
    print("(2.1) p1: "+p1)
    print("(2.2) p2: "+p2)
    sbox1=SBOX1[binaryToDecimal(p1[0:1])][binaryToDecimal(p1[1:4])]
    sbox2=SBOX2[binaryToDecimal(p2[0:1])][binaryToDecimal(p2[1:4])]
    print("(3) SBOX1 generates: "+sbox1)
    print("(3) SBOX2 generates: "+sbox2)
    sboxed=sbox1+sbox2
    print("(3.1) SBOXES generated: "+sboxed)
    finalxor=xor(left,sboxed)
    print("(4) XORing left with the sbox generated content: "+finalxor)
    merged=right+finalxor
    print("(5) Merging right slice with xored content: "+merged)
    print("")
    print("ROUND "+str(roundnumber+1)+" GENERATED: "+merged)
    return merged

def DESRoundHidden(plaintext,roundnumber):
    left=plaintext[0:CHUNKSIZE//2]
    right=plaintext[6:CHUNKSIZE]
    expanded=expand(right)
    xored=xor(expanded,KEYMATERIAL[roundnumber])
    p1=xored[0:4]
    p2=xored[4:8]
    sbox1=SBOX1[binaryToDecimal(p1[0:1])][binaryToDecimal(p1[1:4])]
    sbox2=SBOX2[binaryToDecimal(p2[0:1])][binaryToDecimal(p2[1:4])]
    sboxed=sbox1+sbox2
    finalxor=xor(left,sboxed)
    merged=right+finalxor
    return merged

def DES(plaintext,mode):
    if(mode=="visible"):
        for i in range(0,NUMROUNDS):
            plaintext=DESRound(plaintext,i)
        print("================================================")
        print("DES CHUNK ENCRYPTED: "+plaintext)
        print("================================================")
    else:
        for i in range(0,NUMROUNDS):
            plaintext=DESRoundHidden(plaintext,i)
    return plaintext

def main():
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@ S-DES Encrypt program by friendlyWizard23 @@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    choice=input("Would you like to visualize every step of the Algorithm?[yes/no]: ")
    plaintext=input("Input the plaintext: ")

    key=input("input 9 bit key: ")
    tobin=tobinary(plaintext)

    generatechunks(tobin)
    print("Plaintext chunks: ")
    print(CHUNKEDPLAINTEXT)

    generatekeymaterial(key)
    print("Key material: ")
    print(KEYMATERIAL)
    if choice=="yes":
        for i in CHUNKEDPLAINTEXT:
            ENCRYPTED.append(DES(i,"visible"))
    else:
        for i in CHUNKEDPLAINTEXT:
            ENCRYPTED.append(DES(i,"hidden"))

    print("ENCRYPTED CHUNKS: ")
    print(ENCRYPTED)

if __name__ == "__main__":
    main()
