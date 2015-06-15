#! /usr/bin/python
"""
Author: Vrong
Mail: getvrong@gmail.com

Description:
	This script converts any existing flac/wave file in a given source directory and its sub directories
	into mp3 320kb files organised in a identical file tree. Mp3 files that doesn't need to be converted are just copied into
	the destination folder. The destination folder with all mp3 is ./___mp3export by default, 
	and all repertories are recreated in it.

How to:
	Just place the script with at the root of your music libraries or song folders, then start it.

	Default source is current directory.
	Default destination is './___mp3export'
	
	You can execute this script from another location using arguments:
	python ./FLACtoMP3 <source> <out_directory>

Requirements:
	Needs 'python', 'flac', 'lame' packages installed to work.

Version 2.1

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

total_removed = 0
total_removed_folders = 0
total_removed_emptyfolders = 0

total_folders_scanned = 0
total_files_scanned = 0



def removeOutdatedMp3(cur_path, dst_path):
	global total_removed
	global total_removed_folders
	global total_removed_emptyfolders
	
	for f in os.listdir(dst_path):
		
		# create current examinated file path and his mp3 destination equivalent 
		cur_file = cur_path + '/' + f #file that is supposed to exist (but with mp3 extension)
		dst_file = dst_path + '/' + f
		
		#don't treat the script nor the destination directory
		if cur_file != dst_path and cur_file != program:
			
			if os.path.isdir(dst_file): #if it's a folder, so create its mirror
				if not os.path.exists(cur_file):
					shutil.rmtree(dst_file)
					total_removed_folders = total_removed_folders + 1
				#recrusive call to convert subfiles of the folder
				else: 
					removeOutdatedMp3(cur_file, dst_file)
					#remove empty folder if its the case
					if not os.listdir(dst_file):
						os.rmdir(dst_file)
						total_removed_emptyfolders =  total_removed_emptyfolders + 1
					
			else: #it's a non directory file
				type, enco = mimetypes.guess_type(dst_file)
				if type == 'audio/mpeg':
					dstmp3 = dst_file
					issrc = False
				
					#flac test
					srcflac = change_extension(cur_file, '.mp3', '.flac');
					if os.path.exists(srcflac):
						issrc = True
					
					#wav test
					srcwav = change_extension(cur_file, '.mp3', '.wav');
					if os.path.exists(srcwav):
						issrc = True
					#wave test
					srcwave = change_extension(cur_file, '.mp3', '.wave');
					if os.path.exists(srcwav):
						issrc = True
				
					#mp3 test
					srcmp3 = cur_file
					if os.path.exists(srcmp3):
						issrc = True
					
					#tests end
					if issrc == False:
						print('Removing ' + dstmp3)
						os.remove(dstmp3)
						total_removed = total_removed + 1
				else: #this file has nothing to do here
					print('Removing ' + dst_file)
					os.remove(dst_file)
					total_removed = total_removed + 1
				
	pass

def convertFolder(cur_path, dst_path):
	#global variables for stats
	global total_converted
	global total_found
	global total_copied
	global total_newfolders
	global total_ignored
	global total_folders_scanned
	global total_files_scanned
	
	
	#treat every file or folder in this path
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
				total_folders_scanned = total_folders_scanned + 1
				convertFolder(cur_file, dst_file)
				
			else: #it's a file
				total_found = total_found +1
				type, enco = mimetypes.guess_type(cur_file)
				total_files_scanned = total_files_scanned + 1
				#print the current file and its MIME type
				#print("__________________________________________")
				
				#if type != None:
				#	print(cur_file + " : " + type)
				#else:
				#	print(cur_file + " : None")
				
				if type == 'audio/flac': #convert flac to mp3
					dstmp3 = change_extension(dst_file, '.flac', '.mp3')
					if not os.path.exists(dstmp3):
						print("__________________________________________")
						print(cur_file + " : " + type) 
						os.system("flac -dc " + shellprotect(cur_file) + " | lame -b 320 - " + shellprotect(dstmp3) )
						total_converted = total_converted + 1;
						
				if type == 'audio/wav' or type == 'audio/x-wav': #convert flac to mp3
					dstmp3 = change_extension(dst_file, '.wav', '.mp3')
					dstmp3 = change_extension(dstmp3, '.wave', '.mp3')
					if not os.path.exists(dstmp3):
						print("__________________________________________")
						print(cur_file + " : " + type) 
						os.system("lame -h -b 320 " + shellprotect(cur_file) + " " + shellprotect(dstmp3) )
						total_converted = total_converted + 1;
						
				elif type == 'audio/mpeg': #copy file if it is a mp3
					if not os.path.exists(dst_file):
						print("__________________________________________")
						print(cur_file + " : " + type)
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
	if src.upper().endswith(curext.upper()):
		src = src[:-1*len(curext)]
		src = src + newext
	return src

def shellprotect(s):
	return "'" + s.replace("'", "'\\''") + "'"

#PROGRAM START

if not os.path.exists(dst):
	os.makedirs(dst)
print('Scanning for music...')
print('Source : ' + src)
print('Destination : ' + dst)
convertFolder(src, dst);
removeOutdatedMp3(src, dst);


print
print("Conversion ended. Stats :")
print("{}: {}".format("Folders scanned", total_folders_scanned))
print("{}: {}".format("Files scanned", total_files_scanned))
print
print("{}: {}".format("Files converted", total_converted))
print("{}: {}".format("mp3 files copied", total_copied))
print("{}: {}".format("Files found", total_found))
print
print("{}: {}".format("Ignored files", total_ignored))
print("{}: {}".format("Folders created", total_newfolders))
print("{}: {}".format("Folders created", total_removed))
print("{}: {}".format("Outdated folders removed", total_removed_folders))
print("{}: {}".format("Single files removed", total_removed))
print("{}: {}".format("Empty folders removed", total_removed_emptyfolders))

#flac -dc machin.flac | lame -b 320 - machin.mp3


end = datetime.datetime.now()
laps = end - start
print
print("Spent {} days, {} hours, {} minutes, {} seconds, {} microseconds.".format(laps.days, (laps.seconds//60)//60, (laps.seconds//60)%60, laps.seconds%60, laps.microseconds))

total_converted = 0
total_found = 0
total_copied = 0
total_newfolders = 0
total_ignored = 0
