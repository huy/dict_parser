from nose.tools import *
from dict.parser import *

class TestParseDict:

  def test_ignore_comment(self):
    p = DictParser().parse("# this is comment\n #\n\t#\nColor .") 
    assert_equal(1,p.num_words())

  def test_ignore_empty_line(self):
    p = DictParser().parse("\n \n\t\nColor .") 
    assert_equal(1,p.num_words())

  def test_words_not_used_in_any_defs(self):
    p = DictParser().parse("Color .\nRed Color\nFruit .\nApple Red Fruit") 
    assert_equal(["Apple"],p.not_used_in_any_defs)

class TestParseLine:

  def test_ignore_comment(self):
    p = LineParser().parse("Yellow Color # bright")
    assert_equal(["Color"],p.definition)

  def test_primitive_def(self):
    p = LineParser().parse("Color .")
    assert_equal([],p.definition)

  def test_got_a_word(self):
    p = LineParser().parse("Yellow Color")
    assert_equal("Yellow",p.word)

  def test_got_a_def(self):
    p = LineParser().parse("Apple Red Fruit")
    assert_equal(["Red","Fruit"],p.definition)

class TestSort:

  def test_sort_only_primitives(self):
    ts = TSorter({"Color":[],"Fruit":[]}).tsort(["Color","Fruit"])
    assert_equal(["Color","Fruit"],ts.tsorted)
    
  def test_1hop_distance(self):
    ts = TSorter({"Color":[],"Yellow":["Color"]}).tsort(["Yellow"])
    assert_equal(["Color","Yellow"],ts.tsorted)

  def test_2hops_distance(self):
    ts = TSorter({"Color":[],"Yellow":["Color"],"Fruit":[],
                 "Pear":["Yellow","Fruit"]}).tsort(["Pear"])
    assert_equal(["Color","Yellow","Fruit","Pear"],ts.tsorted)

  def test_has_cycle(self):
    ts = TSorter({"Egg":["Chicken","White"],"Chicken":["Egg","Yellow"],
                  "Pear":["Yellow"],"Yellow":["Color"],"White":["Color"],"Color":[]}).tsort(["Pear"])
    assert_equal(["Color","Yellow","Pear"],ts.tsorted)
    
class TestParseAndSort:

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
     assert_equal(["Color","Red","Fruit","Apple","Yellow","Pear"],p.tsorted())
