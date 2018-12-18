#!/bin/bash

#Main starts from here
#generateTxtFile and get a abs path
va=$(python excel2txt.py textDataset.xlsx 2>&1)
DownloadDir="/home/nullbyte/DataSet/"
for entry in $va/*;        
do
     echo $va$entry 
     filename=$(basename -- $entry)
     var=${filename%%.*}
     export FILENAME=$DownloadDir$var
     ./txt2ssml.pl -s slow $entry > $va$var
     python amazon_tts.py $va$var
 done                                                                                            
