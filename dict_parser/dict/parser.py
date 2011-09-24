from sorter import TSorter

class DictParser:
  def __init__(self):
    self.dict={}
    self.duplicated={}

  def ignored(self,str):
    return (not str) or (str[0] == "#")

  def parse(self,lines):
    words_used_in_def=set()
    for str in lines.split("\n"):
      str = str.strip()
      if not self.ignored(str):
        word,definition = self.parse_a_line(str)
        if word in self.dict:
          self.add_duplicated(word,definition)
        self.dict[word] = definition
        for z in definition:
          words_used_in_def.add(z)

    self.not_used_in_any_defs = [z for z in self.dict if z not in words_used_in_def] 
    self.not_defined_in_dict = [z for z in words_used_in_def if z not in self.dict]
    return self

  def parse_a_line(self,line):
    word_arr = line.split("#")[0].strip().split()
    return word_arr[0],[z for z in word_arr[1:] if z != "."]

  def add_duplicated(self,word,definition):
    if word in self.duplicated:
       self.duplicated[word].append(definition)
    else:
       self.duplicated[word] = [self.dict[word],definition] 
      
  def tsort(self):
    s = TSorter(self.dict)
    s.sort(self.not_used_in_any_defs)
    self.sorted = s.sorted
    self.cycles = s.cycles

if __name__ == "__main__":
  from sys import argv,exit,stderr
  from os.path import exists 

  if len(argv) <2:
    print >> stderr, "ERROR: missing inputfile"
    exit(-1)
  
  script, filename = argv 

  if not exists(filename):
    print >> stderr, "ERROR: file %s does not exists" % filename
    exit(-2)

  input = open(filename) 
  p = DictParser().parse(input.read())
  input.close() 
  
  if not p.dict:
    print >> stderr, "ERROR: file %s is empty or contains only comments" % filename
    exit(-3)

  p.tsort()
  print ",".join(p.sorted)

  if p.duplicated:
    print >> stderr, "WARNING: detect duplicated definition(s)"
    print >> stderr, "\t%s" % ",".join(["%dx%s" % (len(d),w) for w,d in p.duplicated.items()])

  if p.not_defined_in_dict:
    print >> stderr, "WARNING: detect words used in definition but are not defined in dict"
    print >> stderr, "\t%s" % ",".join(p.not_defined_in_dict)

  if p.cycles:
    print >> stderr,"ERROR: detect cyclic definition(s)"
    print >> stderr,"\t","\n\t".join(["->".join(z) for z in p.cycles])
