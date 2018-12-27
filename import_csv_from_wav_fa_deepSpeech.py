
#Usage:
#Input - The folder of wav file
#Output - THree csv file containing trainning, Testing and dev

from __future__ import absolute_import, division, print_function

# Make sure we can import stuff from util/
# This script needs to be run from the root of the DeepSpeech repository
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import csv
import tarfile
import subprocess
import progressbar
import argparse
from os import path
from os import walk
import random
import re

FIELDNAMES = ['wav_filename', 'wav_filesize', 'transcript']
SAMPLE_RATE = 16000
MAX_SECS = 10
ARCHIVE_DIR_NAME = 'cv_corpus_v1'
ARCHIVE_NAME = ARCHIVE_DIR_NAME + '.tar.gz'
ARCHIVE_URL = 'https://s3.us-east-2.amazonaws.com/common-voice-data-download/' + ARCHIVE_NAME

language = ['-Geraint', # Welsh English - Male
            '-Salli', # US English -  Female
            '-Matthew', #US English -  Male
            '-Kimberly', #US English -  Female
            '-Kendra', #US English -  Female
            '-Justin', #US English -  Male
            '-Joey', #US English -  Male        
            '-Joanna', #US English -  Female  
            '-Ivy', #US English -  Female       
            '-Raveena',  # Indian English -  Female
            '-Aditi', #Indian English -  Female         
            '-Emma', #British English -Female         
            '-Brian',  #British English - Male  
            '-Amy', #British English - Female       
            '-Russell',  # UAustralian English - Male
            '-Nicole' #UAustralian English - Female               
]

speed = ['-x-slow',
         '-slow',
         '-medium',
         '-fast',
         '-x-fast']

def custom_cv_writer(source_dir):
    new_dic = {}
    source_dir = path.abspath(source_dir)
    f = []
    for dirpath, dirnames, filenames in os.walk(source_dir):
        f.extend(filenames)
        for name in filenames:
            fullpath = (os.path.join(dirpath, name))
            new_dic.update({name:fullpath})
            
    random.shuffle(f)
    wav_files_count = len(f)
    train_wavs_count = int(0.9 * wav_files_count)
    dev_wavs_count = int(0.07 * wav_files_count)
    train_wavs = f[0:train_wavs_count]    
    dev_wavs = f[train_wavs_count:train_wavs_count+dev_wavs_count]
    test_wavs = f[train_wavs_count+dev_wavs_count:wav_files_count]
    rows = []

    def create_csv(csv_type,wavs_list):
        with open(csv_type+".csv","w") as target_csv:
            counter = {"too_short":0,"proper":0,"too_long":0}
            for wav_filename in wavs_list:
                wav_filepath = source_dir + '/' + wav_filename
                frames = int(subprocess.check_output(['soxi', '-s', wav_filepath], stderr=subprocess.STDOUT))
                file_size = path.getsize(wav_filepath)
                transcript_speed_pre = re.sub("|".join(speed), "", wav_filename)
                transcript_lang_pre = re.sub("|".join(language), "", transcript_speed_pre)
                transcript_char_pre = transcript_lang_pre.replace("-", "_")
                transcript = os.path.splitext(transcript_char_pre)[0]
                if int(frames/SAMPLE_RATE*1000/10/2) < len(str(transcript)):
                    print("Excluding samples that are too short to fit the transcript")
                    # Excluding samples that are too short to fit the transcript
                    counter['too_short'] += 1
                elif frames/SAMPLE_RATE > MAX_SECS:
                    # Excluding very long samples to keep a reasonable batch-size
                    print("Excluding very long samples to keep a reasonable batch-size")
                    counter['too_long'] += 1
                else:
                    # This one is good - keep it for the target CSV
                    #print("This one is good - keep it for the target CSV")
                    rows.append((wav_filepath, file_size, transcript))
                    counter['proper'] += 1

            writer = csv.DictWriter(target_csv, fieldnames=FIELDNAMES)
            writer.writeheader()
            bar = progressbar.ProgressBar(max_value=len(rows))
            for filename, file_size, transcript in bar(rows):
                writer.writerow({ 'wav_filename': filename, 'wav_filesize': file_size, 'transcript': transcript })

        if counter['too_short'] > 0:
            print('Skipped %d samples that were too short to match the transcript.' % counter['too_short'])
        if counter['too_long'] > 0:
            print('Skipped %d samples that were longer than %d seconds.' % (counter['too_long'], MAX_SECS))

    create_csv(source_dir+"/custom_train",train_wavs)
    create_csv(source_dir+"/custom_dev",dev_wavs)
    create_csv(source_dir+"/custom_test",test_wavs)

if __name__ == "__main__":
    #_download_and_preprocess_data(sys.argv[1])
    #Get the user input
    parser = argparse.ArgumentParser(description='Process some strings.')
    parser.add_argument('input', metavar='input folder', type=str,
                    help='input wav file folder to convert')
    args = parser.parse_args()
    src_user_input = args.input
    custom_cv_writer(src_user_input)
