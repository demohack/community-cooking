import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes #only for AES CBC mode

data = 'hello world, sample data to be encrypted'
key = 'AAAAAAAAAAAAAAAA' #Must Be 16 char for AES128

#sample code from https://medium.com/@sachadehe/encrypt-decrypt-data-between-python-3-and-javascript-true-aes-algorithm-7c4e2fa3a9ff

#AES ECB mode without IV (initialization vector)


def encrypt_no_iv(raw):
        raw = pad(raw.encode(),16)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw))

def decrypt_no_iv(enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return unpad(cipher.decrypt(enc),16)

encrypted = encrypt_no_iv(data)
print('encrypted ECB Base64:',encrypted.decode("utf-8", "ignore"))

decrypted = decrypt_no_iv(encrypted)
print('data: ',decrypted.decode("utf-8", "ignore"))


#CBC with Fix IV

#FIX IV
iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8') #16 char for AES128

def encrypt_iv(data,key,iv):
        data= pad(data.encode(),16)
        cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
        return base64.b64encode(cipher.encrypt(data))

def decrypt_iv(enc,key,iv):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc),16)

encrypted = encrypt_iv(data,key,iv)
print('encrypted CBC base64 : ',encrypted.decode("utf-8", "ignore"))

decrypted = decrypt_iv(encrypted,key,iv)
print('data: ', decrypted.decode("utf-8", "ignore"))


#CBC mode with random IV

#Random IV more secure
iv =  get_random_bytes(16) #16 char for AES128

def encrypt_ran_iv(data,key,iv):
        data = pad(data.encode(),16)
        cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
        return base64.b64encode(cipher.encrypt(data)), base64.b64encode(cipher.iv).decode('utf-8')
  
def decrypt_ran_iv(enc,key,iv):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, base64.b64decode(iv))
        return unpad(cipher.decrypt(enc),16)

encrypted, iv2 = encrypt_ran_iv(data,key,iv)
print('encrypted CBC base64 : ',encrypted.decode("utf-8", "ignore"))

decrypted = decrypt_ran_iv(encrypted,key,iv2)
print('data: ', decrypted.decode("utf-8", "ignore"))

