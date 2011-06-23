class DictParser:
  def __init__(self):
    self.dict={}

  def ignored(self,str):
    str = str.strip()
    return str == "" or str[0] == "#"

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

  def tsorted(self):
    return TSorter(self.dict).tsort(self.not_used_in_any_defs).tsorted

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
    self.tsorted = []
    self.dict = dict

  def tsort(self,start_with):
    visited = set([])
    for z in start_with:
      self.visit(z,visited)
    return self
      
  def visit(self,word,visited):
    if not word in visited:
      visited.add(word)
      if word in self.dict:
        for z in self.dict[word]:
          self.visit(z,visited)
        self.tsorted.append(word) 
  
if __name__ == "__main__":
  from sys import argv,exit
  from os.path import exists 

  if len(argv) !=2:
    print "missing inputfile"
    exit(-1)
  
  script, filename = argv 

  if not exists(filename):
    print "file %s does not exists" % filename
    exit(-1)

  input = open(filename) 
  p = DictParser().parse(input.read())
  input.close() 
  
  print ",".join(p.tsorted())

