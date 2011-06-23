class DictParser:
  def __init__(self):
    self.dict={}

  def ignored(self,str):
    str = str.strip()
    return str == "#" or str == ""

  def parse(self,lines):
    words_used_in_def=set()
    lp = LineParser()
    for z in lines.split("\n"):
      if not self.ignored(z):
        lp.parse(z)
        self.dict[lp.word] = lp.definition
        words_used_in_def = words_used_in_def.union(lp.definition)

    self.not_used_in_any_defs = [z for z in self.dict if not z in words_used_in_def] 

    return self

  def num_words(self):
    return len(self.dict.keys())

class LineParser:

  def parse(self,line):
    word_arr = line.split("#")[0].strip().split()
    self.word = word_arr[0]
    self.definition = [z for z in word_arr[1:] if z != "."]
    return self

class SortError(Exception): 
  pass 

class TSorter:

  def __init__(self,dict):
    self.ordered = []
    self.dict = dict

  def sort(self,start_with):
    visited = set([])
    for z in start_with:
      self.visit(z,visited)
    return self
      
  def visit(self,word,visited):
    if not word in visited:
      visited.add(word)
      for z in self.dict[word]:
        self.visit(z,visited)
      self.ordered.append(word) 

