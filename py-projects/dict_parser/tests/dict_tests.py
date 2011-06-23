import unittest
from dict.parser import *

class TestParseDict(unittest.TestCase):

  def test_ignore_comment(self):
    p = DictParser().parse("# this is comment\n #\n\t#\nColor .") 
    self.assertEqual(1,p.num_words())

  def test_ignore_empty_line(self):
    p = DictParser().parse("\n \n\t\nColor .") 
    self.assertEqual(1,p.num_words())

  def test_words_not_used_in_any_defs(self):
    p = DictParser().parse("Color .\nRed Color\nFruit .\nApple Red Fruit") 
    self.assertEqual(["Apple"],p.not_used_in_any_defs)

class TestParseLine(unittest.TestCase):

  def test_ignore_comment(self):
    p = LineParser().parse("Yellow Color # bright")
    self.assertEqual(["Color"],p.definition)

  def test_primitive_def(self):
    p = LineParser().parse("Color .")
    self.assertEqual([],p.definition)

  def test_got_a_word(self):
    p = LineParser().parse("Yellow Color")
    self.assertEqual("Yellow",p.word)

  def test_got_a_def(self):
    p = LineParser().parse("Apple Red Fruit")
    self.assertEqual(["Red","Fruit"],p.definition)

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
    sorted = TSorter({"Egg":["Chicken","White"],"Chicken":["Egg","Yellow"],
                  "Pear":["Yellow"],"Yellow":["Color"],"White":["Color"],"Color":[]}).sort(["Pear"])
   
    self.assertTrue(sorted.index("Color") < sorted.index("Yellow"))
    self.assertTrue(sorted.index("Yellow") < sorted.index("Pear"))
    
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
     sorted = p.tsort()
 
     self.assertTrue(sorted.index("Red") < sorted.index("Apple"))
     self.assertTrue(sorted.index("Fruit") < sorted.index("Apple"))
     self.assertTrue(sorted.index("Color") < sorted.index("Red"))
     self.assertTrue(sorted.index("Color") < sorted.index("Yellow"))
     self.assertTrue(sorted.index("Yellow") < sorted.index("Pear"))
     self.assertTrue(sorted.index("Fruit") < sorted.index("Pear"))

if __name__ == '__main__':
    unittest.main()
