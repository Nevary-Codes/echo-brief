from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from tkinter import *
from tkinter import messagebox
from gtts import gTTS
import os
import sys
import subprocess

summ = ""
n = 0


# --------------------------------------------------------------------------------------------------------------------------------------------------------------#
def summarize():
    global summ
    text = article.get()
    if len(text) == 0:
        messagebox.showerror(message="Please fill all the fields", title="Oops")
    else:
        filtered_sentence = []
        sentence = ""
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        for i in filtered_sentence:
            sentence += i + " "
        freqtable = dict()
        for word in word_tokens:
            word = word.lower()
            if word in stop_words:
                continue
            if word in freqtable:
                freqtable[word] += 1
            else:
                freqtable[word] = 1

        sentences = sent_tokenize(text)
        sentencevalue = dict()
        for j in sentences:
            for word, freq in freqtable.items():
                if word in j.lower():
                    if j in sentencevalue:
                        sentencevalue[j] += freq
                    else:
                        sentencevalue[j] = freq

        sumvalues = 0
        for k in sentencevalue:
            sumvalues += sentencevalue[k]
        average = int(sumvalues / len(sentencevalue))
        summary = ''
        for l in sentences:
            if (l in sentencevalue) and (sentencevalue[l] > (1.2 * average)):
                summary += " " + sentence
        f = open("summary.txt", 'a')
        f.write(f"{summary}\n")
        f.close()
        messagebox.showinfo(message="Summary has been saved to summary.txt", title="Success")
        listen = Button(text="Convert to MP3", command=sound)
        listen.grid(column=0, row=4, columnspan=2)
        summ = summary


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def sound():
    global n
    n = n + 1
    myobj = gTTS(text=summ, lang="en-us", slow=False)
    myobj.save(f"welcome{n}.mp3")
    listen = messagebox.askyesno(message="File has been saved. Do you want to play it?", title="Saved")
    if listen:
        open_file(f"welcome{n}.mp3")
    else:
        pass


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------#
window = Tk()
window.title("EchoBrief")
window.config(pady=50, padx=50)
bot = Label(text="Hi! My name is Echo Brief\nDo you want me to summarise anything?", width=40, font=("", 20, ""))
bot.grid(column=0, row=0, columnspan=2)
article = Entry(width=40)
article.grid(column=0, row=1, columnspan=2)
article.focus()
enter = Button(text="Summarize", command=summarize)
enter.grid(column=0, row=3, columnspan=2)

window.mainloop()
