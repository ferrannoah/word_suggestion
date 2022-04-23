import io
from tkinter import PAGES
import pdftotext
import os
# assign directory
directory = 'pdfs'
s = ""
# iterate over files in
# that directory
for i in range(len(os.listdir(directory))):
	f = os.path.join(directory, os.listdir(directory)[i])
# checking if it is a file
	if os.path.isfile(f):
		file = open(f, "rb")
		pdf = pdftotext.PDF(file)
		for page in pdf:
			s += page

f = open("data.txt", "w")
f.write(s)

