#! encoding=utf8
from vigenere import *
from string import *
import unittest,logging
from multiprocessing.dummy import Pool as ThreadPool
logging.basicConfig(level=logging.ERROR,format="%(message)s")

def quick_ic((key_length,encoded)):
    return get_ic(key_length,encoded)
class Test(unittest.TestCase):
    def setUp(self):
        # self.plain_text="""Gatsby believed in the green light, the orgastic future that year by year recedes before us. It eluded us then, but that's no matter to−morrow we will run faster, stretch out our arms farther. . . . and one fine morning So we beat on, boats against the current, borne back ceaselessly into the past.
# """
        self.plain_text=open("text.txt").read()
        ans=[]
        for i in self.plain_text:
            if i in ascii_letters:
                ans.append(i)
        self.plain_text=''.join(ans)
    def test_key_gen(self):
        for i in range(3,16,3):
            key=key_generator(i)
            logging.info("key"+str(i)+":\t"+key)
            self.assertEqual(i,len(key))
    def test_valid(self):
        key=key_generator(random.randint(3,16))
        logging.info("using key:\t"+key)
        plain_text=self.plain_text
        ans=[]
        for i in plain_text:
            if i in ascii_letters:
                ans.append(i)
        plain_text=''.join(ans)
        logging.info("plain_text\:\t"+plain_text)
        encode_str=vigenere_encode(key,plain_text)
        logging.info("encode_text:\t"+encode_str)
        decode_str=vigenere_decode(key,encode_str)
        logging.info("decode_text:\t"+decode_str)
        self.assertEqual(plain_text.upper(),decode_str,"assert failed")
    def test_frequency(self):
        self.assertEqual(3,get_frequency("ABCDEFAA")["A"])
        self.assertEqual(self.plain_text.count("A"),get_frequency(self.plain_text)['A'])

    def test_ics(self):
        for i in [1,2,4,8,16,32,64, 128,256]:
            key_gen=key_generator(i)
            encoded=vigenere_encode(key_gen,self.plain_text)
            self.encoded=encoded
            # get_ic(i,encoded)
            pools=ThreadPool(16)
            args=[]
            for j in [1,2,4,8,16,32,64,128,256]:
                args.append((j,encoded))
            results=pools.map(quick_ic,args)
            print(str(i)+str(results))

if __name__ == "__main__":
    unittest.main()

