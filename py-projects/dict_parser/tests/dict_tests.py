from nose.tools import *
from dict.parser import *

class TestDictParser:

  def test_ignore_comment(self):
    p = DictParser().parse("#\n #\n\t#\nColor .") 
    assert_equal(1,p.num_words())

  def test_ignore_empty_line(self):
    p = DictParser().parse("\n \n\t\nColor .") 
    assert_equal(1,p.num_words())

  def test_words_not_used_in_any_defs(self):
    p = DictParser().parse("Color .\nRed Color\nFruit .\nApple Red Fruit") 
    assert_equal(["Apple"],p.not_used_in_any_defs)


class TestLineParser:

  def test_ignore_comment(self):
    p = LineParser().parse("Yellow Color # bright")
    assert_equal(["Color"],p.definition)

  def test_primitive_def(self):
    p = LineParser().parse("Color .")
    assert_equal([],p.definition)

  def test_word(self):
    p = LineParser().parse("Yellow Color")
    assert_equal("Yellow",p.word)

  def test_def(self):
    p = LineParser().parse("Apple Red Fruit")
    assert_equal(["Red","Fruit"],p.definition)

class TestTSorter:

  def test_only_primitives(self):
    ts = TSorter({"Color":[],"Fruit":[]}).sort(["Color","Fruit"])
    assert_equal(["Color","Fruit"],ts.ordered)
    
  def test_distance_zero(self):
    ts = TSorter({"Color":[],"Yellow":["Color"]}).sort(["Yellow"])
    assert_equal(["Color","Yellow"],ts.ordered)

  def test_distance_one(self):
    ts = TSorter({"Color":[],"Yellow":["Color"],"Fruit":[],
                 "Pear":["Yellow","Fruit"]}).sort(["Pear"])
    assert_equal(["Color","Yellow","Fruit","Pear"],ts.ordered)

  def test_has_cycle(self):
    ts = TSorter({"Egg":["Chicken","White"],"Chicken":["Egg","Yellow"],
                  "Pear":["Yellow"],"Yellow":["Color"],"White":["Color"],"Color":[]}).sort(["Pear"])
    assert_equal(["Color","Yellow","Pear"],ts.ordered)
    
class TestDictSort:

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
     ts = TSorter(p.dict).sort(p.not_used_in_any_defs)
     assert_equal(["Color","Red","Fruit","Apple","Yellow","Pear"],ts.ordered)
