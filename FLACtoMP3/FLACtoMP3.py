#! /usr/bin/python
"""
Author: Vrong
Mail: getvrong@gmail.com

Description:
	This script convert any existing flac file in source directory and sub directories
	into mp3 320kb files. Mp3 files that doesn't need to be converted are just copied into
	the destination folder. The destination folder with all mp3 is ./mp3converted by default, 
	and all repertories are recreated in it.

How to:
	Just place the script with at the root of your music libraries or song folders, then open start it.

	Default source is current directory.
	Default destination is './___mp3export'
	

	(not tested) This program can be used with following arguments : source destination 
	example: python ./FLACtoMP3.py ./dir/source/dir2 "./dest folder/dst"

requirements:
	Needs 'python', 'flac', 'lame' packages installed to work.

Version 1.0.2

"""

import os
import mimetypes 
import shutil
import sys
import datetime

start = datetime.datetime.now()


src = '.'
dst = './___mp3export'
program = "./" + __file__;

#set source and destination folders from arguments and remove '/' at the end of both
if len(sys.argv) == 3:
	src = sys.argv[1]
	dst = sys.argv[2]
	if src.endswith('/'):
		src = src[:-1]
	if dst.endswith('/'):
		dst = src[:-1]



total_converted = 0
total_found = 0
total_copied = 0
total_newfolders = 0
total_ignored = 0


def convertFolder(cur_path, dst_path):
	#global variables for stats
	global total_converted
	global total_found
	global total_copied
	global total_newfolders
	global total_ignored
	
	
	#treat every file or fodler in this path
	for f in os.listdir(cur_path):
		
		# create current examinated file path and his mp3 destination equivalent 
		cur_file = cur_path + '/' + f
		dst_file = dst_path + '/' + f
		
		#don't treat the script nor the destination directory
		if cur_file != dst_path and cur_file != program:
			
			if os.path.isdir(cur_file): #if it's a folder, so create its mirror
				if not os.path.exists(dst_file):
					os.makedirs(dst_file)
					total_newfolders = total_newfolders +1
				#recrusive call to convert subfiles of the f folder
				convertFolder(cur_file, dst_file)
				
			else: #it's a file
				total_found = total_found +1
				type, enco = mimetypes.guess_type(cur_file)
				#print the current file and its MIME type
				print(cur_file + " : " + type)
				
				if type == 'audio/flac': #convert flac to mp3
					dstmp3 = change_extension(dst_file, '.flac', '.mp3')
					if not os.path.exists(dstmp3): 
						os.system("flac -dc \'" + cur_file + "\' | lame -b 320 - \'" + dstmp3 + "\'")
						total_converted = total_converted + 1;
						
				elif type == 'audio/mpeg': #copy file if it is a mp3
					if not os.path.exists(dst_file):
						shutil.copyfile(cur_file, dst_file)
						total_copied = total_copied +1

				"""
				incoming modifications to handle other formats (wav, ..)
				"""		
				else: #ignored files
					total_found = total_found -1
					total_ignored = total_ignored +1
			pass
	pass


#change the extension of the src file to newext, only if it matches with curext
def change_extension(src, curext, newext): 
	if src.endswith(curext):
		src = src[:-1*len(curext)]
	src = src + newext
	return src

if not os.path.exists(dst):
    os.makedirs(dst)
convertFolder(src, dst);

print
print("{}: {}".format("Files converted", total_converted))
print("{}: {}".format("mp3 files copied", total_copied))
print("{}: {}".format("Files found", total_found))
print
print("{}: {}".format("Ignored files", total_ignored))
print("{}: {}".format("Folders created", total_newfolders))

#flac -dc machin.flac | lame -b 320 - machin.mp3


end = datetime.datetime.now()
laps = end - start
print
print("Spent {} days, {} minutes, {} seconds, {} microseconds.".format(laps.days, laps.seconds//60, laps.seconds%60, laps.microseconds))

total_converted = 0
total_found = 0
total_copied = 0
total_newfolders = 0
total_ignored = 0
