#!/usr/bin/env python2
from datetime import datetime
import time
import random
import secret
import hashlib

def sha256(data):
    m = hashlib.sha256()
    m.update(data)
    return m.hexdigest()

def GetNonce():
    t_seed = time.time() * (1<<10)
    t_seed = pow(17, int(t_seed), 0x8d6a6ecc01)
    random.seed(t_seed)
    return str(random.randint(0, (1<<32)))

def Mac(my_nonce, your_nonce):
    return sha256("{},{},{}".format(my_nonce, your_nonce, secret.key))

def Verify(msg, my_nonce, your_nonce):
    if my_nonce == your_nonce:
        # NO REFLECTION ATTACK !
        return False
    ans = sha256("{},{},{}".format(your_nonce, my_nonce, secret.key))
    return ans == msg

def EnterMsg():
    msg = raw_input("> ")
    Message(msg, "You")
    return msg

def Message(msg, name="Timmy"):
    nowTime = datetime.now()
    print("----------------------------------------")
    print("{}:  {} - {}".format(name,msg, nowTime.strftime("%M:%S.%f")[:-4]))
    print("----------------------------------------\n")

def main():
    my_nonce = GetNonce()
    Message("Hi, I'm Timmy, I'm looking for my friend, Amy. Amy must remember the private key we shared before.\n\tSend me your message - N_a, and I will prove that I'm REAL Timmy first ~")
    your_nonce = EnterMsg()
    Message("In order to prevent reflection attack, I hash 2 messages together with the secret key\
             \n\tThis is my message, N_t: " + my_nonce + \
            "\n\tThis is the hash, H(N_t,N_a,key): " + Mac(my_nonce, your_nonce) + \
            "\n\tNow it's your turn to prove that you are Amy. Send me the cipher, H(N_a,N_t,key)")
    cipher = EnterMsg()
    if Verify(cipher, my_nonce, your_nonce):
        Message("It's you! Amy! I miss you so much!")
        print(secret.flag2)
    else:
        Message("No! Stop pretending Amy!")
    
if __name__ == '__main__':
    main()
