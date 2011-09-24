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
    if word not in call_chain:
      call_chain.append(word)
      if word in self.dict:
        for z in self.dict[word]:
          self.visit(z,call_chain)
          call_chain.pop()
        if word not in self.visited:
          self.visited.add(word)
          self.sorted.append(word)
    else:
      call_chain.append(word)
      self.cycles.append(list(call_chain))


