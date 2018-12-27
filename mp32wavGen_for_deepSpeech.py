from os import walk
from os import path
import subprocess
import pdb
import os 
import argparse

#Get the user input
parser = argparse.ArgumentParser(description='Process some strings.')
parser.add_argument('input', metavar='input folder', type=str,
                    help='input mp3 file folder to convert')
parser.add_argument('output', metavar='output folder', type=str,
                    help='output folder store wav file')
args = parser.parse_args()
src_user_input = args.input
src_user_output = args.output

#Check the sox dep on host and install
subprocess.call(['./cvformat_dep.sh'])

source_dir = path.abspath(src_user_input)
dest_folder = path.abspath(src_user_output)

#Dic store filename and dir name
new_dic = {}

#List to store filename
f = []

#List to store dir name
d = []

# for (dirpath, dirnames, filenames) in walk(source_dir):	
# 	d.extend(dirnames)

for (dirpath, dirnames, filenames) in walk(source_dir):	
	f.extend(filenames)
	for name in filenames:
		fullpath = (os.path.join(dirpath, name))
		new_dic.update({name:fullpath})

# i = -1

print("Sox processing .................")
for srcfile in f:
	wav_filepath = new_dic[srcfile]
	# if not os.path.exists(dest_folder+'/'+d[i]):
	# 	os.makedirs(dest_folder+'/'+d[i])
		# i += 1
	final = dest_folder+'/'+srcfile.split('.')[0]+'.wav'
	print(final)
	subprocess.Popen(['sox',wav_filepath, final,'channels','1','rate','16000'])
print("Conversion done.................")