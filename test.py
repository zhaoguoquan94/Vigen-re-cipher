from vigenere import *
from string import *
import unittest,logging
from multiprocessing.dummy import Pool as ThreadPool
import ConfigParser
logging.basicConfig(level=logging.DEBUG,format="in function %(funcName)s: %(message)s")
test_list=[1,2,4,8,16,32,64,128,256]

class Test(unittest.TestCase):
    def setUp(self):
        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")
        self.key_length=cf.getint("vigenere","key_length")
        text_file_path=cf.get("vigenere","plain_text_path")
        self.e=float(cf.get("vigenere","e"))
        self.plain_text=open(text_file_path).read()
        ans=[]
        for i in self.plain_text:
            if i in ascii_letters:
                ans.append(i)
        self.plain_text=''.join(ans).upper()
    def test_key_gen(self):
        for i in range(3,16,3):
            key=key_generator(i)
            # logging.info("key"+str(i)+":\t"+key)
            self.assertEqual(i,len(key))
    def test_valid(self):
        key=key_generator(self.key_length)
        logging.info("generation key with length "+str(self.key_length)+":\t"+key)
        plain_text=self.plain_text
        encode_str=vigenere_encode(key,plain_text)
        decode_str=vigenere_decode(key,encode_str)
        self.assertEqual(plain_text.upper(),decode_str,"assert failed,system failure")
        f=open("encoded_cipher.txt","w")
        f.write(encode_str)
        f.close()
        f=open("decoded_text.txt","w")
        f.write(decode_str)
        f.close()
        logging.info("encode succss!see encoded_cipher.txt for more infomation")
        logging.info("decode succss!see decoded_text.txt for more infomation")
        logging.info("success:decoded string is equal to original string!!")
    def test_frequency(self):
        self.assertEqual(3,get_frequency("ABCDEFAA")["A"])
        freq_dict=get_frequency(self.plain_text)
        self.assertEqual(self.plain_text.count("A"),freq_dict["A"])
        logging.info("plain text frequency:"+str(freq_dict))
    def test_get_largest_freq_letter(self):
        d={"A":10,"B":13,"R":11}
        self.assertEqual(get_largest_freq_letter(d),"B")
    def test_ics(self):
        for i in [4,16,32]:
            key_gen=key_generator(i)
            logging.info("using key:"+str(key_gen))
            encoded=vigenere_encode(key_gen,self.plain_text)
            logging.info("encoded string frequency:"+str(get_frequency(encoded)))
            self.encoded=encoded
            # get_ic(i,encoded)
            pools=ThreadPool()
            args=[]
            for j in test_list:
                args.append((j,encoded))
            results=pools.map(quick_ic,args)


            for l in range(len(results)):
                print("assuming key length="+str(test_list[l])+" IC:"+str(results[l]))

            #guess number section
            bei_shu=[]
            for k in range(len(results)):
                if results[k]<0.066+self.e and results[k]>0.066-self.e:
                    bei_shu.append(test_list[k])

            self.assertEqual(i,bei_shu[0])
    def test_get_shifted_cipher_letter_by_E(self):
        self.assertEqual(get_shifted_cipher_letter_by_E("E"),'A')
        self.assertEqual(get_shifted_cipher_letter_by_E("D"),"Z")
        self.assertEqual(get_shifted_cipher_letter_by_E("F"),"B")
    def test_decode(self):
        self.assertEqual(vigenere_decode("MHE","MIG"),"ABC")
if __name__ == "__main__":
    logging.info("Testing Vigenere Algorithm...")
    unittest.main()

