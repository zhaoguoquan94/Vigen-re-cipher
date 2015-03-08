# coding=utf-8
import random,string,ConfigParser
from multiprocessing.dummy import Pool as ThreadPool
from string  import ascii_letters,ascii_uppercase
def quick_ic((key_length,encoded)):
    return get_ic(key_length,encoded)
def shift_by_letter(origin_text,key,method):
    assert len(origin_text)==len(key)
    origin_text=origin_text.upper()
    key=key.upper()
    str_list=[]
    if method=="encode":
        for i  in range(len(origin_text)):
            str_list.append(chr((ord(origin_text[i])+ord(key[i])-2*ord("A"))%26+ord("A")))
        return ''.join(str_list)
    else:
        for i  in range(len(origin_text)):
            str_list.append(chr(ord("A")+(26+(ord(origin_text[i])-ord("A"))-(ord(key[i])-ord("A")))%26))
        return ''.join(str_list)

def vigenere_encode(key,plaintext):
    key=key.upper()
    plaintext=plaintext.upper()
    key=(key*int(len(plaintext)/len(key)+1))[:len(plaintext)]
    return shift_by_letter(plaintext,key,"encode")

def vigenere_decode(key,cipher_text):
    key=key.upper()
    plaintext=cipher_text.upper()
    key=(key*int(len(plaintext)/len(key)+1))[:len(plaintext)]
    return shift_by_letter(plaintext,key,"decode")
def key_generator(key_length):
    return ''.join([random.choice(string.ascii_letters.upper()) for i in range(key_length)])

def get_frequency(text):
    d={}
    text=text.upper()
    for l in string.ascii_uppercase:
        d[l]=text.count(l)
    return d

def get_ic(key_length,text):
    ics=[]
    for j in range(key_length):
        str_group=""
        for i in range(j,len(text),key_length):
            str_group+=text[i]
        freq=get_frequency(str_group)
        Ic_sum=0
        for k,v in freq.items():
            Ic_sum+=float(v)*v/len(str_group)/len(str_group)
        ics.append(Ic_sum)
    # print("ic with key_length="+str(key_length)+"\t:"+str(float(sum(ics))/len(ics)))
    return float(sum(ics))/len(ics)


def vigenere_attack_brute(cipher,top_key_length):
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    e=float(cf.get("vigenere","e"))
    test_list=[i for i in range(2,200)]
    pools=ThreadPool()
    args=[]
    for j in test_list:
        args.append((j,cipher))
    results=pools.map(quick_ic,args)


    for l in range(len(results)):
        print("assuming key length="+str(test_list[l])+" IC:"+str(results[l]))

    #guess number section
    bei_shu=[]
    for k in range(len(results)):
        if results[k]<0.066+e and results[k]>0.066-e:
            bei_shu.append(test_list[k])
    print(bei_shu)

if __name__=="__main__":
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    text_file_path=cf.get("vigenere","plain_text_path")
    e=float(cf.get("vigenere","e"))
    plain_text=open(text_file_path).read()
    ans=[]
    for i in plain_text:
        if i in ascii_letters:
            ans.append(i)
    plain_text=''.join(ans).upper()
    key_length=26
    encoded=vigenere_encode(key_generator(key_length),plain_text)
    vigenere_attack_brute(encoded,len(plain_text))
