from sorter import TSorter

class DictParser:
  def __init__(self):
    self.dict={}
    self.duplicated={}
    self.sorted=[]
    self.not_used_in_any_defs=[]
    self.not_defined_in_dict=[]

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
    self.not_defined_in_dict = [z for z in words_used_in_def if not z in self.dict]
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

if __name__ == "__main__":
  from sys import argv,exit,stderr
  from os.path import exists 

  if len(argv) !=2:
    print >> stderr, "ERROR: missing inputfile"
    exit(-1)
  
  script, filename = argv 

  if not exists(filename):
    print >> stderr, "ERROR: file %s does not exists" % filename
    exit(-2)

  input = open(filename) 
  p = DictParser().parse(input.read())
  input.close() 
  
  if p.num_words() == 0:
    print >> stderr, "ERROR: file %s is empty or contains only comments" % filename
    exit(-3)

  p.tsort()
  print ",".join(p.sorted)

  if len(p.duplicated):
    print >> stderr, "WARNING: detect duplicated definition(s)"
    for z in p.duplicated:
      print >> stderr, "\t%d x %s" % (len(p.duplicated[z]),z)

  if len(p.not_defined_in_dict):
    print >> stderr, "WARNING: detect words used in definition but are not defined in dict"
    print >> stderr, "\t%s" % ",".join(p.not_defined_in_dict)

  if len(p.cycles):
    print >> stderr, "WARNING: detect cyclic definition(s)"
    for z in p.cycles:
      print >> stderr, "\t%s" % z
