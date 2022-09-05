from flask import Flask, request, render_template
from nltk.corpus import reuters, brown
from nltk.util import ngrams
import nltk
from collections import defaultdict, Counter
import random

#These lines will run when the app starts

# Download the "brown" corpus using nltk
nltk.download("brown")
# Create the dictionary which will act as the next-word prediction model
model = defaultdict(lambda: defaultdict(lambda:0))
print("Learning the corpus...")
# Create a tri-gram language model:

# Count the occurrences of the different tri-grams present in the "brown" corpus
for sents in brown.sents():
    for w1,w2,w3 in ngrams(sents,3,pad_left=True,pad_right=True):
        model[(w1,w2)][w3]+=1

# Calculate the probabilities for each tri-gram by dividing it with the total count
for i in model:
    total = float(sum(list(model[i].values())))
    for j in model[i]:
        model[i][j]/=total

with open("temp_storage.txt","w") as f:
    pass

app = Flask(__name__)


def fetch_current_words():
    '''Function to fetch the most recent 2 words'''
    hold_previous = []
    with open("temp_storage.txt","r") as f:
        hold_previous = f.readlines()
    if hold_previous:
        hold_previous = hold_previous[-1].strip().split(" ")
    return hold_previous[-2:]

def fetch_all():
    '''Function to fetch the entire text from the text file'''
    print("Getting full text")
    full_text = ""
    with open("temp_storage.txt","r") as f:
        full_text = ' '.join(f.readlines())
    return full_text

@app.route("/")
def hello_world():
    '''Function to render a sample HTML page'''
    return render_template("index.html")
    

@app.route("/generate_random")
def generate_random():
    '''
    This function randomly generates a sentence until it hits the end of the sentence
    '''
    text = list(model.keys())[random.randint(0,len(model))]
    text = [text[0],text[1]]
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
    return ' '.join([t for t in text if t])



def helper(text,flag):
    '''
    This function executes the logic to fetch the next possible word, given the current bi-gram/phrase
    '''
    # Start with a random bi-gram if user does not enter any text
    if not text:
        text = list(model.keys())[random.randint(0,len(model))]
    # Pick a random bi-gram if the current phrase does not have a value(next possible word) in the model
    if not model[tuple(text[-2:])].keys():
        text = list(model.keys())[random.randint(0,len(model))]
    # Pick a random bi-gram if the current phrase does not have a value(next possible word) in the model
    if list(model[tuple(text[-2:])].keys())[0]==None:
        text = list(model.keys())[random.randint(0,len(model))]
    text = [text[0],text[1]]
    # Sort all the keys for the current bi-gram and pick the top 3 next possible words
    next_word_possibilities = sorted(dict(model[tuple(text[-2:])]).items(),key = lambda x:x[1],reverse=True)[:3]
    size = len(next_word_possibilities)
    # From the top 3, pick a random next word
    next_word = next_word_possibilities[random.randint(0,size-1)][0]
    # Store the next word along with the previous two words in the list and write it to a file
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
    '''
    This function takes in the user input or existing phrase and uses it to predict the next word
    '''
    # this method is executed when user provides data in the text box and CLICKS generate
    if request.method=="POST":
        # Fetch the current words from the file if there are any
        hold_previous = fetch_current_words()
        # Fetch the user input from the text box
        text = request.form['userinput']
        text = text.split()
        # If a phrase exists previously, then use it to predict the next word
        if hold_previous:
            helper(hold_previous,0)
        # If there is not phrase the use the user input form the text box
        else:
            helper(text,1)
        # Fetch the complete sentence that has been written to the text file
        temp = fetch_all()
        # Send the data to the HTML page and display the result on screen
        return render_template("user_input.html",data=temp)
    # If the page is refreshed without clicking the Generate button, 
    # then delete the contents of the text file and start new
    with open("temp_storage.txt","w") as f:
        pass
    return render_template("user_input.html")

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)