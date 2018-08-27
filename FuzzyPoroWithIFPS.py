from triplesec import TripleSec
from fuzzy_extractor import FuzzyExtractor
import ipfsapi

def FuzzyPoro():
    
    extractor = FuzzyExtractor(10, 2) #(CharacterLength, ErrorAllowed)
    BiometricData = input("Enter a biometric data (10 characters):") #Sample Biometric Data
    BiometricData = BiometricData.encode('utf-8')
    PrivateKey = input("Enter your private key:")
    PrivateKey = PrivateKey.encode('utf-8')
    key, helper = extractor.generate(BiometricData) #Create the key and the helper

    print ('Your key is: %s' % (key))

    KeyForTripleSec = TripleSec(key) #Runs your generated key through TripleSec
    EncryptedPrivateKey = KeyForTripleSec.encrypt(PrivateKey) #Encrypts your private key
    FileWrite = open("EncryptedKey.txt", "w+") #This is very insecure obviously. But this is just for testing so :/
    FileWrite.write(str(EncryptedPrivateKey))
    FileWrite.close()
    
    print ('Your encrypted private key is: %s' % (EncryptedPrivateKey))

    KeyRecover = input("Enter your biometric data again:") #The second time you scan your fingerprint/biometric data

    KeyReturn = extractor.reproduce(KeyRecover, helper) #Creates your original key

    print ('Your recovered key is: %s' % (KeyReturn))
    
    ExtractedKey = TripleSec(KeyReturn) #Runs your regenerated key through TripleSec
    
    try:     
            print ('Your private key is: ')

            print(ExtractedKey.decrypt(EncryptedPrivateKey).decode()) #Decodes your EncryptedPrivateKey with your regenerated encryption key
    except:
            print ('Wrong encryption key BAD BAD BAD')

def IPFS():
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
        print(api)
    
    except ipfsapi.exceptions.ConnectionError as ce:
        print(str(ce))

    UploadKey = api.add('EncryptedKey.txt')
    print(UploadKey)

FuzzyPoro()
IPFS()
