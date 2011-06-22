class DictParser:
  def __init__(self):
    self.defs=[]

  def ignored(self,str):
    str = str.strip()
    return str == "#" or str == ""

  def parse(self,lines):
    self.defs = [z for z in lines.split("\n") if not self.ignored(z)]

class WordDef:

  def __init__(self,line):
    word_arr = line.split("#")[0].strip().split()
    self.word = word_arr[0]
    self.definitions = [z for z in word_arr[1:] if z != "."]
