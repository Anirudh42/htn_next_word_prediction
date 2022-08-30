from flask import Flask, render_template
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

text = ["primary", "election"]
full_text = ["primary", "election"]
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
def generate_sentence_two():
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
 
    return ' '.join([t for t in text if t])

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)