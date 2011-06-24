class DictParser:
  def __init__(self):
    self.dict={}
    self.duplicated={}
    self.sorted=[]

  def ignored(self,str):
    str = str.strip()
    return str == "" or str[0] == "#"

  def parse(self,lines):
    words_used_in_def=set()
    lp = LineParser()
    for str in lines.split("\n"):
      if not self.ignored(str):
        lp.parse(str)
        if lp.word in self.dict:
          self.process_duplicated(lp.word,lp.definition)
        self.dict[lp.word] = lp.definition
        for z in lp.definition:
          words_used_in_def.add(z)

    self.not_used_in_any_defs = [z for z in self.dict if not z in words_used_in_def] 
    return self

  def num_words(self):
    return len(self.dict.keys())

  def process_duplicated(self,word,definition):
    if word in self.duplicated:
       self.duplicated[word].append(definition)
    else:
       self.duplicated[word] = [self.dict[word],definition] 
      
  def tsort(self):
    s = TSorter(self.dict)
    s.sort(self.not_used_in_any_defs)
    self.sorted = s.sorted
    self.cycles = s.cycles

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

  p.tsort()
  print ",".join(p.sorted)

  if len(p.duplicated):
    print "WARNING: detect duplicated definition(s)"
    for z in p.duplicated:
      print "\t%d x %s" % (len(p.duplicated[z]),z)

  if len(p.cycles):
    print "WARNING: detect cyclic definition(s)"
    for z in p.cycles:
      print "\t%s" % z
