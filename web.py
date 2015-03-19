# -*- coding: utf-8 -*-
from flask import Flask
from flask.templating import *
from flask import request
from vigenere import *

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    if request.method=="GET":
        return render_template("index.html")
@app.route('/encrypt',methods=['GET',"POST"])
def encrypt():
    plain_text=request.form["plain_text"]
    plain_text=clean_passage(plain_text)
    key_length=request.form["key_length"]
    key=key_generator(int(key_length))
    cipher=vigenere_encode(key,plain_text)
    ans=u'<p>生成密钥:{0}</p><p>密文:</p><div style="word-break:break-all">{1}</div>'.format(key,cipher)
    return ans
@app.route("/decrypt",methods=["GET",'POST'])
def decrype():
    cipher_text=request.form["cipher_text"]
    cipher_text=clean_passage(cipher_text)
    max_key_length=int(request.form['max_key_length'])
    key_length=vigenere_attack_brute_key_length(cipher_text,max_key_length)
    print(key_length)
    ans=[]
    for i in range(0,key_length):
        cipher=cipher_text[i::key_length]
        freq_dict=get_frequency(cipher)
        letter_with_max_freq=get_largest_freq_letter(freq_dict)
        cipher_letter=get_shifted_cipher_letter_by_E(letter_with_max_freq)
        ans.append(cipher_letter)
        print(cipher_letter)
    key= "key:\t"+''.join(ans)
    plain_text=vigenere_decode(''.join(ans),cipher_text)
    return unicode(key)+u'<br>原文:<div style="word-break:break-all">{0}</div>'.format(plain_text)

if __name__ == '__main__':
    app.run(debug=True)