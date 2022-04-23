import tkinter as tk
from pynput import keyboard
from pynput.keyboard import Key
import word_suggestion
import re
import subprocess

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|pbcopy'
    return subprocess.check_call(cmd, shell=True)

s = ""
window = tk.Tk()
window.title("Word Suggestion")
window.geometry("700x350")
label = tk.Label(
	text="Word Suggestion: null",
	foreground="black",
	background="white"
)
entry = tk.Entry(window, width=50)
label.pack()
entry.pack()
suggestion = [""]

def on_press(key):
	pass

def on_release(key):
	if key == Key.space:
		text = re.sub(r'[^A-Za-z ]+', '', entry.get().lower())
		text = ["null", *text.split()]
		if text != []:
			word = text.pop()
			suggestion[0] = word_suggestion.t.get_suggestion3(word, text)
			copy2clip(suggestion[0])
			label.config(text="Word Suggestion: " + suggestion[0])
			# copy2clip(suggestion)
			
	else:
		text = re.sub(r'[^A-Za-z ]+', '', entry.get().lower())
		text = ["null", *text.split()]
		if text != []:
			current = text.pop()
			if text == []:
				word = "null"
			else:
				word = text.pop()
			if suggestion[0][:len(current)] != current:
				suggestion[0] = word_suggestion.t.get_suggestion_current(word, text, current)
				copy2clip(suggestion[0][len(current):])
				label.config(text="Word Suggestion: " + suggestion[0])
			copy2clip(suggestion[0][len(current):])


		
			 

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
	window.mainloop()
	listener.join()

