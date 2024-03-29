import unittest
from dict.parser import *

class TestParseDict(unittest.TestCase):

  def test_ignore_comment(self):
    p = DictParser().parse("# this is comment\n #\n\t#\nColor .") 
    self.assertEqual(1,len(p.dict))

  def test_ignore_empty_line(self):
    p = DictParser().parse("\n \n\t\nColor .") 
    self.assertEqual(1,len(p.dict))

  def test_words_not_used_in_any_defs(self):
    p = DictParser().parse("Color .\nRed Color\nFruit .\nApple Red Fruit") 
    self.assertEqual(["Apple"],p.not_used_in_any_defs)

class TestParseLine(unittest.TestCase):

  def test_ignore_comment(self):
    w,d = DictParser().parse_a_line("Yellow Color # bright")
    self.assertEqual(["Color"],d)

  def test_primitive_def(self):
    w,d = DictParser().parse_a_line("Color .")
    self.assertEqual([],d)

  def test_got_a_word(self):
    w,d = DictParser().parse_a_line("Yellow Color")
    self.assertEqual("Yellow",w)

  def test_got_a_def(self):
    w,d = DictParser().parse_a_line("Apple Red Fruit")
    self.assertEqual(["Red","Fruit"],d)

class TestSort(unittest.TestCase):

  def test_sort_only_primitives(self):
    sorted = TSorter({"Color":[],"Fruit":[]}).sort(["Color","Fruit"])
    self.assertTrue(sorted.index("Color")>=0)
    self.assertTrue(sorted.index("Fruit")>=0)
    
  def test_1hop_distance(self):
    sorted = TSorter({"Color":[],"Yellow":["Color"]}).sort(["Yellow"])
    self.assertTrue(sorted.index("Color") < sorted.index("Yellow"))

  def test_2hops_distance(self):
    sorted = TSorter({"Color":[],"Yellow":["Color"],"Fruit":[],
                 "Pear":["Yellow","Fruit"]}).sort(["Pear"])
    self.assertTrue(sorted.index("Color") < sorted.index("Yellow"))
    self.assertTrue(sorted.index("Fruit") < sorted.index("Pear"))
    self.assertTrue(sorted.index("Yellow") < sorted.index("Pear"))

  def test_has_cycle(self):
    s = TSorter({"Egg":["White","Chicken"],
            "Chicken":["Yellow","Egg"],
            "Bird":["Egg"],
            "Yellow":["Color"],
            "White":["Color"],
            "Color":[]})
   
    s.sort(["Bird"])
    self.assertEqual(["Bird","Egg","Chicken","Egg"],s.cycles[0])

    s.sort(["Egg"])
    self.assertEqual(["Egg","Chicken","Egg"],s.cycles[0])

    s.sort(["Chicken"])
    self.assertEqual(["Chicken","Egg","Chicken"],s.cycles[0])
    
class TestParseAndSort(unittest.TestCase):

   def test_sample_input(self):
     p = DictParser().parse(
"""
Apple    Red Fruit    # Hey, this is the first line 
Red      Color 
Yellow   Color 
Color    .    # This is a primitive 
Fruit    . 
Pear     Yellow Fruit 
"""
     )
     p.tsort()
     sorted = p.sorted
 
     self.assertTrue(sorted.index("Red") < sorted.index("Apple"))
     self.assertTrue(sorted.index("Fruit") < sorted.index("Apple"))
     self.assertTrue(sorted.index("Color") < sorted.index("Red"))
     self.assertTrue(sorted.index("Color") < sorted.index("Yellow"))
     self.assertTrue(sorted.index("Yellow") < sorted.index("Pear"))
     self.assertTrue(sorted.index("Fruit") < sorted.index("Pear"))

if __name__ == '__main__':
    unittest.main()
