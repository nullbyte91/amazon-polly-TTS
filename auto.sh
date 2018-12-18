#!/bin/bash

#Main starts from here
#generateTxtFile and get a abs path
va=$(python excel2txt.py 2>&1)
for entry in $va/*;        
do
    echo $va$entry 
    filename=$(basename -- $entry)
    var=${filename%%.*}
    ./txt2ssml.pl -s slow $entry > $var
    python amazon_tts.py $var
done                                                                                            
