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

with open("temp_storage.txt","w") as f:
    pass

app = Flask(__name__)


def fetch_current_words():
    hold_previous = []
    with open("temp_storage.txt","r") as f:
        hold_previous = f.readlines()
    if hold_previous:
        hold_previous = hold_previous[-1].strip().split(" ")
    print('here current')
    return hold_previous[-2:]

def fetch_all():
    print("here all")
    with open("temp_storage.txt","r") as f:
        return ' '.join(f.readlines())

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
        text = list(model.keys())[random.randint(0,len(model))]
    if not model[tuple(text[-2:])].keys():
        text = list(model.keys())[random.randint(0,len(model))]
    text = [text[0],text[1]]
    print(text)
    sentence_finished = False
    while not sentence_finished:
        # select a random probability threshold  
        r = random.random()
        accumulator = .05
        for word in model[tuple(text[-2:])].keys():
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
    if request.method=="POST":
        hold_previous = fetch_current_words()
        text = request.form['userinput']
        text = text.split()
        if hold_previous:
            print("Calling with previous")
            print("Previous:",hold_previous)
            temp_list = generate_sentence_two(hold_previous)
        else:
            print("Calling with entered input")
            print("Text:",text)
            temp_list = generate_sentence_two(text)
        if temp_list[0]!="0":
            with open("temp_storage.txt","a") as f:
                for i in temp_list:
                    f.writelines(i + " ")
            
        temp = ' '.join(temp_list)
        return render_template("user_input.html",data=temp)
    return render_template("user_input.html")

def helper(text,flag):
    if not text:
        text = list(model.keys())[random.randint(0,len(model))]
    if not model[tuple(text[-2:])].keys():
        text = list(model.keys())[random.randint(0,len(model))]
    if list(model[tuple(text[-2:])].keys())[0]==None:
        text = list(model.keys())[random.randint(0,len(model))]
    print(text)
    print(model[tuple(text[-2:])].keys())
    text = [text[0],text[1]]
    next_word_possibilities = sorted(dict(model[tuple(text[-2:])]).items(),key = lambda x:x[1],reverse=True)[:3]
    size = len(next_word_possibilities)
    next_word = next_word_possibilities[random.randint(0,size-1)][0]
    text.append(next_word)
    with open("temp_storage.txt","a") as f:
        if flag==0:
            if next_word!=None:
                f.writelines(next_word + " ")
        else:
            for i in text:
                if i!=None:
                    f.writelines(i + " ")

@app.route("/generate_next",methods=["GET","POST"])
def generate_next():
    print(request.method)
    if request.method=="POST":
        print("Inside post")
        hold_previous = fetch_current_words()
        text = request.form['userinput']
        text = text.split()
        if hold_previous:
            helper(hold_previous,0)
        else:
            helper(text,1)
        temp = fetch_all()
        return render_template("user_input.html",data=temp)
    with open("temp_storage.txt","w") as f:
        pass
    return render_template("user_input.html")
if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)