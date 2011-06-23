class DictParser:
  def __init__(self):
    self.dict={}

  def ignored(self,str):
    str = str.strip()
    return str == "" or str[0] == "#"

  def parse(self,lines):
    words_used_in_def=set()
    lp = LineParser()
    for str in lines.split("\n"):
      if not self.ignored(str):
        lp.parse(str)
        self.dict[lp.word] = lp.definition
        for z in lp.definition:
          words_used_in_def.add(z)

    self.not_used_in_any_defs = [z for z in self.dict if not z in words_used_in_def] 

    return self

  def num_words(self):
    return len(self.dict.keys())

  def tsort(self):
    return TSorter(self.dict).sort(self.not_used_in_any_defs)

class LineParser:

  def parse(self,line):
    word_arr = line.split("#")[0].strip().split()
    self.word = word_arr[0]
    self.definition = [z for z in word_arr[1:] if z != "."]
    return self

class SortCycleError(Exception):
  pass

class TSorter:

  def __init__(self,dict):
    self.dict = dict

  def sort(self,start_with):
    self.sorted = []
    self.visited = set()
    self.cycles = []
    for z in start_with:
      self.visit(z,[])
    return self.sorted
      
  def visit(self,word,call_chain):
    if not word in call_chain:
      call_chain.append(word)
      if word in self.dict:
        for z in self.dict[word]:
          self.visit(z,call_chain)
        if not word in self.visited:
          self.visited.add(word)
          self.sorted.append(word) 
    else:
      call_chain.append(word)
      self.cycles.append("->".join(call_chain))
  
if __name__ == "__main__":
  from sys import argv,exit
  from os.path import exists 

  if len(argv) !=2:
    print "ERROR: missing inputfile"
    exit(-1)
  
  script, filename = argv 

  if not exists(filename):
    print "ERROR: file %s does not exists" % filename
    exit(-2)

  input = open(filename) 
  p = DictParser().parse(input.read())
  input.close() 
  
  if p.num_words() == 0:
    print "ERROR: file %s is empty or contains only comments" % filename
    exit(-3)
  else:
    print ",".join(p.tsort())
    exit(0)

