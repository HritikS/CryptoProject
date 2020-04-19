import random
import math

def gcd(a,b):
    r1=a
    r2=b
    while(r2>0):
        q=r1//r2
        r=r1-q*r2
        r1=r2
        r2=r
    return r1

def prime(n,k=10):
    if n < 2 or n % 2 == 0:
        return False
    if n == 2:
        return True
    def check(a,s,d,n):
        x=pow(a,d,n)
        if x==1:
            return True
        for i in range(s-1):
            if x==n-1:
                return True
            x=pow(x,2,n)
        return x==n-1
    s=0
    d=n-1
    while d%2==0:
        d>>=1
        s+=1
    for i in range(k):
        a=random.randrange(2,n-1)
        if not check(a,s,d,n):
            return False
    return True

def inverse(e,p):
    l=[i for i in range(2,p) if gcd(i,p)==1]
    d=0
    for i in l:
        if (e*i)%p==1:
            d = i
    return d

def F2(Ga,Gb,a,p):
    if(Ga==Gb):
        s=((3*((Ga[0])**2)+a)*inverse(2*Ga[1],p))%p
    else:
        s=((Gb[1]-Ga[1])*inverse(Gb[0]-Ga[0],p)%p)
    Gcx = (s**2-Ga[0]-Gb[0])%p
    Gc=(Gcx,(s*(Ga[0]-Gcx)-Ga[1])%p)
    return Gc

def F1(n,G0,a,p,o):
    G1=G0
    if(n>o and n%o!=0):
        n=n%o
    elif (n>o and n%o==0):
        n=o
    for i in range(1,n):
        G1=F2(G1,G0,a,p)
    return G1

def encrypt(Pb,Pm,k,G0,a,p,o):
    C=F1(k,G0,a,p,o)
    R=F1(k,Pb,a,p,o)
    e=(R[0]*ord(Pm))%p
    Cm=(e,C)
    return Cm

def decrypt(Cm,nb,a,p,o):
    R=F1(nb,Cm[1],a,p,o)
    d=(Cm[0]*inverse(R[0],p))%p
    return chr(d)

def convert(pwd,o):
    s=0
    for i in pwd:
        i=ord(i)
        s+=i
    s=s%o
    return s

if __name__ == "__main__":
    p=2011
    a=9
    b=7
    o=2048
    Gx=2
    Gy=2
    na=121
    Pa=F1(na,(Gx,Gy),a,p,o)
    nb=input("Enter the password: ")
    nb=convert(nb,o)
    Pb=F1(nb,(Gx,Gy),a,p,o)
    print("The public0 key of B is {}".format(Pb))
    k1=F1(na,Pb,a,p,o)
    k2=F1(nb,Pa,a,p,o)
    print("The shared secret key is: ")
    print("Calculated by A {}".format(k1))
    print("Calculated by B {}".format(k2))
    k=41
    Pm=input("Enter the plaintext: ")
    Cm=encrypt(Pb,Pm,k,(Gx,Gy),a,p,o)
    print("Cipher Text: {}".format(Cm))
    Pmm=decrypt(Cm,nb,a,p,o)
    print("Calculated plaintext: {}".format(Pmm))
