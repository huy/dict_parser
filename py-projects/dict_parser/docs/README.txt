# Dictionary Parser

This simple program parse a text file in form of a simple dictionary, each line define one word. 
The definition uses other words in the dictionary and so on.

The program generates one line of comma-separated list of words sorted in topological order, 
in which words used in definition always precede the word being defined.

## Usage

To parse input file and print out the result, execute the following command

    python dict/parser.py samples/testfile1.txt 2>/dev/null
    color,red,shape,roundish,apple,yellow,onion,long,corn,pear,banana

To run a test
 
    python -m tests.dict_tests
    ............
    ----------------------------------------------------------------------
    Ran 12 tests in 0.001s
    
    OK

## Examples

1. parse file testfile1.txt

        python dict/parser.py samples/testfile1.txt 
        color,red,shape,roundish,apple,yellow,onion,long,corn,pear,banana
        WARNING: detect words used in definition but are not defined in dict
    	    fruit,vegetable
    
2. parse file testfile2.txt

        python dict/parser.py samples/testfile2.txt 
        no,missing
        WARNING: detect words used in definition but are not defined in dict
    	    definition
3. parse file testfile3.txt
    
        python dict/parser.py samples/testfile3.txt 
        ERROR: file samples/testfile3.txt is empty or contains only comments

4. parse non existence file
    
        python dict/parser.py missing.txt 
        ERROR: file missing.txt does not exists

## Error handling

There are following edge cases

* if a word in the dictionary is defined more than once then the later definition 
will overwrite the earlier and duplicated word are reported as WARNING
* if a word is used in definition of other words but not defined in dictionary then
the program will report it as WARNING
* if the dictionary has a cycle meaning e.g. word_a is defined using word_b which 
in turn is defined using word_a then the program will report such cycle as ERROR

ERROR and WARNING are printed in stderr
