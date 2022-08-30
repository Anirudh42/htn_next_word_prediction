from flask import Flask, request, render_template
from nltk.corpus import reuters, brown
from nltk.util import ngrams
import nltk
from collections import defaultdict, Counter
import random

nltk.download("reuters")

model = defaultdict(lambda: defaultdict(lambda:0))
print("Learning the corpus...")
for sents in brown.sents():
    for w1,w2,w3 in ngrams(sents,3,pad_left=True,pad_right=True):
        model[(w1,w2)][w3]+=1

for i in model:
    total = float(sum(list(model[i].values())))
    for j in model[i]:
        model[i][j]/=total

app = Flask(__name__)

@app.route("/")
def hello_world():

    return render_template("index.html")

@app.route("/generate")
def generate_sentence():
    for _ in range(100):
        next_word_possibilities = sorted(dict(model[tuple(text[-2:])]).items(),key = lambda x:x[1],reverse=True)[:3]
        size = len(next_word_possibilities)
        next_word = next_word_possibilities[random.randint(0,size-1)][0]
        text.append(next_word)
        if text[-2:]==[None,None]:
            break
        if next_word!=None:    
            full_text.append(next_word)
    return ' '.join(full_text)
    

@app.route("/generate_two")
def generate_sentence_two(text):
    if not text:
        return 0
    sentence_finished = False
    while not sentence_finished:
        # select a random probability threshold  
        r = random.random()
        accumulator = .05

        for word in model[tuple(text[-2:])].keys():
        #       print(r,accumulator,text[-2:],word)
            accumulator += model[tuple(text[-2:])][word]
            # select words that are above the probability threshold
            if accumulator >= r:
                text.append(word)
                break

        if text[-2:] == [None, None]:
            sentence_finished = True
 
    return [t for t in text if t]


@app.route("/generate_user",methods=["GET","POST"])
def generate_user_input():
    temp_list = 0
    hold_previous = []
    with open("temp_storage.txt","r") as f:
        hold_previous = f.readlines()
    if request.method=="POST":
        text = request.form['userinput']
        text = text.split()
        if hold_previous:
            hold_previous = hold_previous[-1].split(" ")
            temp_list = generate_sentence_two(hold_previous[-2:])
        else:
            temp_list = generate_sentence_two(text)
            if text:
                with open("temp_storage.txt","w") as f:
                    for i in temp_list:
                        f.writelines(i + " ")
            
        temp = ' '.join(temp_list)
        return render_template("user_input.html",data=temp)
    print("Clicked")
    return render_template("user_input.html")

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)