from nose.tools import *
from dict.parser import *

class TestDictParser:

  def setup(self):
    self.parser = DictParser()

  def teardown(self):
    pass
  
  def test_ignore_comment(self):
    self.parser.parse("#\n #\n\t#\nColor .") 
    assert_equal(1,len(self.parser.defs))

  def test_ignore_empty_line(self):
    self.parser.parse("\n \n\t\nColor .") 
    assert_equal(1,len(self.parser.defs))

class TestWordDef:

  def test_word(self):
    assert_equal("Yellow",WordDef("Yellow Color").word)

  def test_ignore_comment(self):
    assert_equal(["Color"],WordDef("Yellow Color # bright").definitions)

  def test_primitive_def(self):
    assert_equal([],WordDef("Color .").definitions)

