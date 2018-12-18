"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from time import sleep
import xlrd 
from xlrd.sheet import ctype_text 
from os.path import join, dirname, abspath
import re
from os.path import expanduser
import argparse


def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('input', metavar='ssml File', type=str,
                    help='the SSML input file')
args = parser.parse_args()

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="amzonPollyDev")
polly = session.client("polly")
response = polly.describe_voices()

#Adding Language list for diff accent in English supported by Amazon Polly
language = ['Geraint', # Welsh English - Male
            'Salli', # US English -  Female
            'Matthew', #US English -  Male
            'Kimberly', #US English -  Female
            'Kendra', #US English -  Female
            'Justin', #US English -  Male
            'Joey', #US English -  Male        
            'Joanna', #US English -  Female  
            'Ivy', #US English -  Female       
            'Raveena',  # Indian English -  Female
            'Aditi', #Indian English -  Female         
            'Emma', #British English -Female         
            'Brian',  #British English - Male  
            'Amy', #British English - Female       
            'Russell',  # UAustralian English - Male
            'Nicole' #UAustralian English - Female               
]
infile = args.input
index = 1
home = expanduser("~")
desPath = home 

pieces = []
with open(infile, "rb") as f:
    pieces = [l for l in (line.strip() for line in f) if l]

for accent in language:
    i = index
    for piece in pieces:
        print "piece %d: %s" % (i, piece)

        try:
            # Request speech synthesis
            response = polly.synthesize_speech(Text=piece, TextType="ssml", OutputFormat="mp3",
            VoiceId=accent)
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)
        # Access the audio stream from the response
        if "AudioStream" in response:
        # Note: Closing the stream is important as the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to   
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                #output = os.path.join(gettempdir(), "speech.mp3")

                filename = os.environ['FILENAME']
                save_to = filename + accent + ".mp3"
                output = os.path.join(desPath, save_to)
	        print("File path", output)
                try:
                # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        # Play the audio using the platform's default player
        if sys.platform == "win32":
            os.startfile(output)
        else:
            # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, output])
            sleep(3)