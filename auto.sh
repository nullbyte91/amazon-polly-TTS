#!/bin/bash

#Main starts from here
#generateTxtFile and get a abs path
va=$(python excel2txt.py textDataset.xlsx 2>&1)
DownloadDir="/home/nullbyte/DataSet/"
count=0
accent=17
for entry in $va/*;        
do
     echo $va$entry 
     filename=$(basename -- $entry)
     var=${filename%%.*}
     mkdir -p $DownloadDir$var
     count=`expr "$count" + "${#var}" '*' "$accent"`
     echo $count
     export FILENAME=$DownloadDir$var"/"$var-"x-slow-"
     ./txt2ssml.pl -s x-slow $entry > $va$var
     python amazon_tts.py $va$var
     count=`expr "$count" + "${#var}" '*' "$accent"`
     echo $count
     export FILENAME=$DownloadDir$var"/"$var-"slow-"
     ./txt2ssml.pl -s slow $entry > $va$var
     python amazon_tts.py $va$var
     count=`expr "$count" + "${#var}" '*' "$accent"`
     echo $count
     export FILENAME=$DownloadDir$var"/"$var-"medium-"
     ./txt2ssml.pl -s medium $entry > $va$var
     python amazon_tts.py $va$var
     count=`expr "$count" + "${#var}" '*' "$accent"`
     echo $count
     export FILENAME=$DownloadDir$var"/"$var-"fast-"
     ./txt2ssml.pl -s fast $entry > $va$var
     python amazon_tts.py $va$var
     count=`expr "$count" + "${#var}" '*' "$accent"`
     echo $count
     export FILENAME=$DownloadDir$var"/"$var-"x-fast-"
     ./txt2ssml.pl -s x-fast $entry > $va$var
     python amazon_tts.py $va$var
 done                                                                                            
