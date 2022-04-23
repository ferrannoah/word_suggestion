import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

text = open("data.txt", "r").read() 
sentences = split_into_sentences(text)


words = []
all_nodes = []

for sentence in sentences:
	words.append(sentence.split())

class node:
	def __init__(self, id, parent = None, freq = 0):
		self.id = id
		self.freq = freq
		self.parent = parent
		self.children = []
		self.total_nodes = []

	def increment(self):
		self.freq += 1
	
	def has_child(self, word):
		for node in self.children:
			if node.id == word:
				return node, True
		return False, False
	
	def addChild(self, node):
		self.children.append(node)
		return node
	
	def print(self, tab=0):
		print(' ' * tab + self.id)
		for node in self.children:
			node.print(tab+1)


	def filter(self, freq):
		chil = []
		remove = []
		for node in self.children:
			if node.freq >= freq:
				chil.append(node)
			else:
				remove.append(node)
		for node in remove:
			self.children.remove(node)
		for node in chil:
			node.filter(freq)



	def get_all(self):
		all_nodes.append(self)
		for node in self.children:
			node.get_all()
		
			

	
class tree: 
	def __init__(self, text):
		self.text = text
		self.total_nodes = []
		self.root = node('null')
		self.total_nodes.append(self.root)
		self.words = []
		self.create_tree()
		self.get_freq()
		self.filter_freq(2)

	def append(self, node):
		self.total_nodes.append(node)
		return node

	def filter_freq(self, min):
		self.root.filter(min)
		self.root.get_all()
		self.total_nodes = all_nodes
		
		
		
	def create_tree(self):
		sentences = split_into_sentences(text)
		for sentence in sentences:
			s = re.sub(r'[^A-Za-z0-9 ]+', '', sentence).lower()
			self.words.append(s.split())
		for sentence in self.words:
			self.add_nodes(sentence)

	def add_nodes(self, node_string):
		if node_string == []:
			return
		parent_node = self.root
		for i in range(len(node_string)):
			n, b = parent_node.has_child(node_string[i].lower())
			if not b:
				parent_node = parent_node.addChild(node(node_string[i].lower(), parent = parent_node))
				self.total_nodes.append(parent_node)
			else:
				parent_node = n
			parent_node.increment()

	def get_nodes(self, freq):
		nodes = []
		for node in self.total_nodes:
			if node.freq >= freq:
				nodes.append(node)
		return nodes

	def get_suggestion2(self, word, parent):
		suggestions = []
		for node in self.total_nodes:
			if node.id == word and node.parent.id == parent:
				suggestions = suggestions + node.children
		
		if suggestions == []:
			return 'null'
		
		suggestions.sort(key=lambda x: x.freq, reverse=True)

		if len(suggestions) < 3:
			s = []
			for sug in suggestions:
				s.append(sug.id)
		else:
			s = [suggestions[0].id, suggestions[1].id, suggestions[2].id]

		return s
	
	def get_suggestion3(self, word, parent):
		suggestions = []
		streak = 0
		for n in self.total_nodes:
			if streak < len(parent) * 1:
				if n.id == word:
					# check value in for loop
					check = True
					streak = 0
					curr_node = n
					# run through loop check each parent to see if it equals the parent in the loop
					for i in range(len(parent)-1, -1, -1):
						if check:
							if curr_node.parent.id != parent[i]:
								check = False
							else: 
								streak += 1
							curr_node = curr_node.parent
					# if check > 1:
					# 	print(n.children[0].id)
					if n.children != []:
						suggestions.append([n.children, streak])
		suggestions.sort(key=lambda x: x[1], reverse=True)
		if suggestions == []:
			return "null"
		for s in suggestions:
			s[0].sort(key=lambda x: x.freq, reverse=True)

		return suggestions[0][0][0].id

	def get_suggestion_current(self, word, parent, current):
		suggestions = []
		streak = 0
		for n in self.total_nodes:
			if streak < len(parent) * 1:
				if n.id == word:
					# check value in for loop
					check = True
					streak = 0
					curr_node = n
					# run through loop check each parent to see if it equals the parent in the loop
					for i in range(len(parent)-1, -1, -1):
						if check:
							if curr_node.parent.id != parent[i]:
								check = False
							else: 
								streak += 1
							curr_node = curr_node.parent
					# if check > 1:
					# 	print(n.children[0].id)
					if n.children != []:
						suggestions.append([n.children, streak])
		suggestions.sort(key=lambda x: x[1], reverse=True)
		if suggestions != []:
			
			for s in suggestions:
				s[0].sort(key=lambda x: x.freq, reverse=True)

			for s in suggestions:
				for word in s[0]:
					if word.id[:len(current)] == current:
						return word.id
		for word in self.all_words:
			if word[:len(current)] == current:
				return word
		return "null"


	def get_suggestion(self, word, parent):
		suggestions = []
		for n in self.total_nodes:
			if n.id == word:
				placeholder = n
				# check value in for loop
				for i in range(len(parent)-1, -1, -1):
					if placeholder.parent.id != parent[i]:
						print(placeholder.parent.id + " is not the same as " + parent[i])
					placeholder = placeholder.parent
				suggestions.append([n.children])
		return "Test"
	
	def get_freq(self):
		self.node_dict = {}
		for node in self.total_nodes:
			if node.id in self.node_dict:
				self.node_dict[node.id] += node.freq
			else:
				self.node_dict[node.id] = node.freq
		self.all_words = []
		for words in self.words:
			for word in words:
				self.all_words.append(word)
		self.all_words = list(set(self.all_words))
		self.all_words.sort(key=lambda x: self.node_dict[x], reverse=True)

from datetime import datetime

start = datetime.now()


t = tree(text)

print(datetime.now() - start)
# print("Word Count: " + len(list(set(t.words))))


all_words = []
for n in all_nodes:
		all_words.append(n.id)
all_words = list(set(all_words))
all_words.sort(key=lambda x: t.node_dict[x], reverse=True)
words = open('words.txt', 'w')
for word in all_words:
	words.write(word + "\n")

print("Word Count: " + str(len(all_words)))


# typing = input("Start sentence and go word by word: ").lower().strip()
# typing = re.sub(r'[^a-zA-Z0-9]', '', typing)
# parent = ['null'] 

# while typing != 'x':
# 	print(t.get_suggestion3(typing, parent))
# 	parent.append(typing)
# 	if typing == "":
# 		parent = ['null'] 
# 	typing = input(" : ").lower().strip() 
# 	typing = re.sub(r'[^a-zA-Z0-9]', '', typing)
	




			



# create node tree
