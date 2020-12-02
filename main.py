from collections import defaultdict
# from itertools import chain
import string
import timeit

# Example: ["a","ta","oat","iota","niota","lation","elation","bonetail","anabolite","dealbation","labiodental","nondilatable"]


k = int(input("""Select word list:
0: /usr/share/dict/words
1: 100k words (Wiktionary)
2: 3000 words (EF)
3: Simple word list\n"""))
#note that "100k.txt" is the top 100k words on Wikitionary, so includes French and German words

word_list = ["words.txt", "100k.txt", "3000.txt", "simplewords.txt"][k]

words = dict()
words_by_length = defaultdict(list)
sorted_words = defaultdict(list)
with open(word_list) as f:
  for word in f:
    word = word.strip().lower()
    word_len = len(word)
    words[word] = word_len
    words_by_length[word_len].append(word)
    sorted_words["".join(sorted(word))].append(word)

def old_anagrams(word):
  return [other for other in words_by_length[len(word)]
                if sorted(other) == sorted(word)]

def anagrams(word):
  return sorted_words["".join(sorted(word))]

def extend(word):
  return [char + word for char in string.ascii_lowercase]

def extended_anagrams(word, start_only=False, end_only=True):
  def condition(xword, anagram):
    if end_only:
      # new anagrams only count if the last letter is new
      return xword[0] == anagram[-1]
    elif start_only:
      # new anagrams only count if the first letter is new (default)
      return xword[0] == anagram[0]
    else:
      # no restrictions on new anagrams
      return True
  return {anagram for xword in extend(word)
                  for anagram in anagrams(xword)
                  if condition(xword, anagram)}
                  # if anagram[0] == xword[0]}

class Node():
  def __init__(self, value, parent=None, start_only=False, end_only=True):
    self.value = value
    self.parent = parent
    self.ancestry = Path(self.parent.ancestry.path + [self]) if parent else Path([self])
    self.children = [Node(anagram, self, start_only, end_only)
                    for anagram in extended_anagrams(value, start_only, end_only)]
  
  def __repr__(self):
    return self.value
    # old verbose version (use show_descendents() instead):
    # return f"{self.value} -> {self.children}" if self.children else self.value

  def show_descendents(self, level=0):
    print(" "*level + self.value)
    for child in self.children:
      child.show_descendents(level+1)

  def leaves(self):
    return {subchild for child in self.children for subchild in child.leaves()} if self.children else {self}

  # def possible_parents(self):
  #   return {anagram for anagram in anagrams(self.value[1:]) if anagram in words}

  def paths(self):
    return [leaf.ancestry for leaf in self.leaves()]
    # we need a list rather than a set because the elements (lists) are unhashable

  def descendents(self):
    return {step for path in self.paths() for step in path}
  
  def longest_paths(self):
    max_length = max(map(len, self.paths()))
    return [path for path in self.paths() if len(path) == max_length]

  def paths_to(self, word):
    descendents = self.descendents()
    if not word in [leaf.value for leaf in descendents]:
      print(f"It is not possible to reach \"{word}\" from \"{self.value}\"")
    else:
      return [leaf.ancestry for leaf in descendents if leaf.value == word]

class Path():
  """ A simple wrapper for paths (lists of Node objects)
  This allows us to use __repr__ to represent them neatly with arrows """
  def __init__(self, path):
    self.path = path

  def __repr__(self):
    return " -> ".join(step.value for step in self.path)

  def __len__(self):
    return len(self.path)

  def __iter__(self):
    return iter(self.path)

def find_paths(source, target=None, start_only=False, end_only=True):
  n = Node(source, None, start_only, end_only)
  if target:
    return n.paths_to(target)
  else:
    return n.paths()

def find_paths_to(target, start_only=False, end_only=True):
  return find_paths("", target, start_only, end_only)

def extended_anagrams2(word):
  return {anagram for xword in extend(word)
                  for anagram in anagrams(xword)
                  if anagram[0] == xword[0]}

def expand_tree2(current_words: list):
  if not isinstance(current_words, list):
    raise TypeError("Must be a list!")
  #print(current_words)

  new_words=[]
  temp_word=["null"]
  for ancestry in (current_words):
    print("V ancestry")
    print(ancestry)
    for word in extended_anagrams2(ancestry[0]):
      temp_word[0] = word
      #print("to add ="+ word)
      new_words.append(temp_word + ancestry)
      print("V new words")
      print(new_words)
      return new_words
 

#run2([["a"]])
def run2(word_lists, show_working=True):
  counter=0

  while counter<50:
    word_lists_old = word_lists
    #print(word_lists)
    Word_lists = expand_tree2(word_lists_old)
    counter+=1
    print(counter)
  return words


def expand(words, start_only=False, end_only=True):
  # previously called expand_tree
  return {l for w in words for l in extended_anagrams(w, start_only, end_only)}

def run(word, show_working=True, start_only=False, end_only=True):
  """ Quickly finds maximum depth but does not keep track of which word leads to which, so ancestry cannot be traced """
  current_layer = {word}
  while current_layer:
    if show_working:
      print(current_layer)
    current_layer, last_layer = expand(current_layer, start_only, end_only), current_layer
  display_result(word, last_layer)
  return last_layer

def run_all(starts=string.ascii_lowercase):
  for start in starts:
    run(start, show_working=False)

def display_result(word, result):
  if len(max(result)) == 1:
    return
  if len(result) > 1:
    print(f"\"{word}\": {len(result)} distinct longest words of length {len(max(result))} (e.g. \"{max(result)}\")")
    #print(result)
  else:
    print(f"\"{word}\": unique longest word of length {len(max(result))} (\"{max(result)}\")")
