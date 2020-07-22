from pwn import *
import random

def flag1():
    def check_flag(s):
        sen = ''
        while 'Timmy' not in sen:
            sen = s.recvline().decode()
        if 'Amy' in sen:
            flag = s.recvuntil('}').decode().split('\n')[-1]
            return flag
        else: return None

    def get_time(s):
        sen = ''
        while 'You' not in sen and 'Timmy' not in sen:
            sen = s.recvline().decode()
        sen = sen.split()[-1]
        minute, second, micro = int(sen[:2]), int(sen[3: 5]), int(sen[-2:])
        second += 60 * (minute)
        micro = second * 10**6 + micro * 10**4
        return micro

    def get_len():
        length = 0
        while True:
            length += 1
            s = remote('cns.csie.org', 10224)
            s.sendlineafter('>', '1' * length)
            start = get_time(s)
            end = get_time(s)
            s.close()
            if end - start > 1000: return length
        return None

    def get_flag(length):
        ans = '0' * length
        for i in range(length - 1):
            d, m = None, 0
            for digit in '0123456789':
                trial = ans[:i] + digit + ans[i + 1:]
                s = remote('cns.csie.org', 10224)
                s.sendlineafter('>', trial)
                start = get_time(s)
                end = get_time(s)
                s.close()
                if end - start > m:
                    m = end - start
                    d = digit
            print(f'the {i}-th digit is {d}')
            ans = ans[:i] + d + ans[i + 1:]
        
        for digit in '0123456789':
            trial = ans[:length - 1] + digit
            s = remote('cns.csie.org', 10224)
            s.sendlineafter('>', trial)
            flag = check_flag(s)
            s.close()
            if flag is not None:
                print(f'the number is {trial}')
                return flag

        return None

    length = get_len()
    if length is None:
        print('something went wrong...')
        exit()
    flag = get_flag(length)
    if flag is None:
        print('something went wrong...')
        exit()
    return flag

def flag2():
    nonce_table = {}
    nonce = [3599364109]

    def get_flag(s, mesg):
        s.sendlineafter('>', mesg)
        while True:
            line = s.recvline().decode()
            if 'CNS' in line:
                return line
        return None

    def get_nonce(s, na):
        nonlocal nonce_table, nonce
        s.sendlineafter('>', str(na))
        while True:
            line = s.recvline().decode()
            if 'This is my message' in line:
                nt = int(line.split(':')[-1])
                if nt not in nonce:
                    nonce.append(nt)
            elif 'This is the hash' in line:
                h = line.split(':')[-1].strip()
                break
        print(f'inserted {(nt, na)} in table, current size is {len(nonce_table)}')
        nonce_table[(nt, na)] = h
        if (na, nt) in nonce_table and na != nt:
            return (na, nt)
        return None

    while True:
        s = remote('cns.csie.org', 10225)
        pair = get_nonce(s, random.choice(nonce))
        if pair is not None:
            flag = get_flag(s, nonce_table[pair])
            return flag
            s.close()
            break
        s.close()

if __name__ == '__main__':
    flag1 = flag1()
    flag2 = flag2()
    print(flag1)
    print(flag2)

    



