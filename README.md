Choice Words
============
This library generates random text based on an input grammar. The grammar file is specified in a "phrase book" containing named lists of phrases. The algorithm randomly replaces tags with a choice of the corresponding phrase.

This example generates "thank you" notes:

    root:
    - Dear {{ giver }}, thank you for the {{ object }}.
    - Hey {{ giver }}, thanks for the {{ object }}!

    giver:
    - Aunt Emma
    - Dave and Edna
    - Uncle Bob

    thanks:
    - thank you
    - my greatest thanks

    object:
    - purple vase
    - golden retriever
    - dishwasher

This phrase book can form phrases such as:

    Dear Dave and Edna, thank you for the dishwasher.
    Hey Uncle Bob, thanks for the purple vase!

A more complete "thank you" generator is available in the examples folder. Execute it with:

    python choicewords.py examples/thankyou.txt

The initial key is called "root" by default but you can use a custom key using the `--root` argument:

    python choicewords.py --root object examples/thankyou.txt

You can use a seed value to specify a specific random variation. The seed doesn't have to be numeric.

    python choicewords.py --seed 123 examples/thankyou.txt


License
=======
Choice Words is licensed under the BSD license. See the LICENSE file for details.

Credits
=======
Choice Words is written by Frederik De Bleser.

The idea of the project is based on the Kant Generator Pro, written by Mark Pilgrim as part of his "Dive Into Python" book. (http://www.diveintopython.net/).

