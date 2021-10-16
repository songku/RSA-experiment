import random
#import math
import str2long #用于对字符串编码为bytes，再转为int

# 求两个数字的最大公约数（欧几里得算法）
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

#扩展欧几里得算法，根据底部递归基础，向上求ax+by=gcd的x,y的整数解
def ext_gcd(a, b):
    if b == 0: #递归基础，当b为0时，by=1 mod a 的结果是x=1,
        x1 = 1
        y1 = 0
        x = x1
        y = y1
        r = a
        return r, x, y
    else:
        r, x1, y1 = ext_gcd(b, a % b)
        x = y1
        y = x1 - a // b * y1 #这里要用整数除法
        return r, x, y

def mod_reverse(a,b):
    r,x,y=ext_gcd(a,b)
    return (y+a)%a


# 模N大数的幂乘的快速算法
def fastExpMod(b, e, m):  # 底数，幂，大数N
    result = 1
    e = int(e)
    while e != 0:
        if e % 2 != 0:  # e不是2的倍数，按位与
            e -= 1
            result = (result * b) % m #结果需要乘以1倍的b
            continue
        e >>= 1 #e是2的倍数，右移动一位，b取原值的平方
        b = (b * b) % m
    return result
    # 测试案例
    # c = fastExpMod(3,22,12)
    # print(c) 9


# 针对随机取得p，q两个数的素性检测
def miller_rabin_test(n):  # p为要检验的数
    p = n - 1
    r = 0
    # 寻找满足n-1 = 2^s * m 的s,m两个数
    #  n -1 = 2^r * p
    while p % 2 == 0:  # 最后得到为奇数的p(即m)
        r += 1
        p /= 2
    b = random.randint(2, n - 2)  # 随机取b=[ low , high )
    # 如果情况1    b得p次方  与1  同余  mod n
    if fastExpMod(b, int(p), n) == 1:
        return True  # 通过测试,可能为素数
    # 情况2  b得（2^r  *p）次方  与-1 (n-1) 同余  mod n
    for i in range(0,7):  # 检验六次
        result=fastExpMod(b, (2 ** i) * p, n)
        if result==n-1 or result==1:
            return True  # 如果该数可能为素数，
    return False  # 不可能是素数


# 生成大素数：
def create_prime_num(keylength):  # 为了确保两素数乘积n  长度不会太长，使用keylength/2
    while True:
        # Select a random number n
        # n = random.randint(0, 1<<int(halfkeyLength))
        n = random.randint(0, keylength)
        if n % 2 != 0:
            found = True
            # 如果经过10次素性检测，那么很大概率上，这个数就是素数
            for i in range(0, 10):
                if miller_rabin_test(n):
                    pass
                else:
                    found = False
                    break
            if found:
                return n

# 生成密钥（包括公钥和私钥）
def create_keys(keylength):
    p = create_prime_num(keylength / 2)
    q = create_prime_num(keylength / 2)
    n = p * q
    # euler函数值
    fn = (p - 1)*(q - 1)
    e = selectE(fn)
    d = mod_reverse(fn,e)
    return (n, e, d)


# 随机在（1，fn）选择一个E，  满足gcd（e,fn）=1
def selectE(fn):
    while True:
        # e and fn are relatively prime
        e = random.randint(0, fn)
        if gcd(fn,e) == 1:
            return e


# # 根据选择的e，匹配出唯一的d，也即求逆的过程。算法较慢。
# def match_d(fn,e):
#     r,x,y=ext_gcd(fn,e)
#     return (y+fn)%fn


def encrypt_sin_num(M, e, n):
    return fastExpMod(M, e, n)

def decrypt_sin_num( C, d, m):
    return fastExpMod(C, d, m)

def encrypt():
    n, e, d = create_keys(1024)
    print("请妥善保管私钥（解密时需要用到）：（n:",n," ,d:",d,")")
    s=''
    print("输入你要加密的内容:")
    string = input()
    str_b=string.encode()
    str_int=str2long.bytes2int(str_b)
    c=str(encrypt_sin_num(str_int,e,n))
    s+=c
    print("您的字符串编码结果为：",str_b)
    print("您的字符串字节转为int结果为：", str_int)
    print("您的加密数字串结果为：",s)

def decrypt():
    #n,d = input("私钥：")
    n,d= map(int, input("输入您的私钥（n,d）:").split())
    s = ''
    #s = decrypt(int(mess), d, n)
    print("输入您需要解密的数字串：")
    mess=int(input())
    msg_i = decrypt_sin_num(mess, d, n)
    # msg_b= str2long.int2bytes(msg_i)
    # msg_s=msg_b.decode()
    msg_s=chr(msg_i)
    s += msg_s
    print("您的密文解密成int为：",msg_i)
#    print("您的字符串字节转为int结果为：", str_int)
    print("您的解密结果为：",s)

def encrypt_file():
    try:
        with open('./rsa.txt', "r") as f:
            mess = f.read()
            f.close()
    except Exception as error:
        print(error)
        exit(0)
    n, e, d = create_keys(1024)
    print("请妥善保管私钥（解密时需要用到）：（n:",n," ,d:",d,")")
    s = ''
    #s = encrypt(int(mess), e, n)
    print(mess)
    for ch in mess:
        c = chr(encrypt_sin_num(ord(ch), e, n))
        s += c
   # print(s)
    f = open("./pass.txt", "w", encoding='utf-8')
    f.write(str(s))
    print("Encrypt Done!")


def decrypt_file():
    try:
        with open('./pass.txt', 'rb') as f:
            mess = f.read().decode('utf-8')
            f.close()
    except Exception as error:
        print(error)
        exit(0)
    #n,d = input("私钥：")
    n,d= map(int, input("输入您的私钥（n,d）:").split())
    s = ''
    #s = decrypt(int(mess), d, n)
    for ch in mess:
        c = chr(decrypt_sin_num(ord(ch), d, n))
        s += c
    #print(s)
    f = open("rsa-2.txt", "w", encoding='utf-8')
    f.write(str(s))
    print("Decrypt Done!")

def display():
    num=input()
    if num=='1':
        encrypt()
    elif num=='2':
        decrypt()
    elif num=='3':
        encrypt_file()
    elif num=='4':
        decrypt_file()
    elif num=='q':
        exit(0)
    else:
        print("your input is not availbale,please try again")
        exit(-1)

if __name__=="__main__":
    print("_________________RSA_________________")
    print("1.encrypt")
    print("2.decrypt")
    print("3.encrypt file")
    print("4.decrypt file")
    print("q.quit")
    print("Enter the key you want to try")
    print("_____________________________________")
    display()