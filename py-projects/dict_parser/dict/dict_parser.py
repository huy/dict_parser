from sys import argv,exit
from os.path import exists 

if len(argv) !=2:
  print "missing inputfile"
  exit(-1)

script, dict_file = argv 

print "parse from %s" % (dict_file) 

input = open(dict_file) 
p = DictParser().parse(input.read())
input.close() 

print p.tsorted()
