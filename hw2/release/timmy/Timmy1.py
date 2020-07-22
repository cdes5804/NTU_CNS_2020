#!/usr/bin/env python2
from datetime import datetime
import secret

def Check(digit, key):
    digit = ord(digit) * 0xcc9a1e41
    digit = digit >> 8
    digit = pow(digit, (1<<17))
    digit = (digit * 0x1b882673) % (0xe6546b)
    digit = pow(digit, (1<<14))
    digit = (digit * 0x85ebcc6a) % (0xe6546b)
    return digit == key

def Verify(num):
    if len(num) != len(secret.myNumber):
        return False
    for i in range(len(num)):
        try:
            if (not num[i].isdigit()) or (not Check(num[i], secret.myNumber[i])):
                return False
        except:
            print("Something is wrong ?!")
            return False
    return True

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
    Message("Hi, I'm Timmy, I'm looking for my friend, Amy. If you are Amy, you must know what is my favorite number.")
    num = EnterMsg()
    if Verify(num):
        Message("Hi~Amy, long time no see!")
        print(secret.flag1)
    else:
        Message("No, you are not my friend!")

if __name__ == '__main__':
    main()
