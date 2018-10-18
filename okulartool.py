#!/usr/bin/python3
# repository: github.com/umitkabuli/okulartool
# This script import to pdf okular bookmarks 
import sys
import os
import codecs
import cgi
import subprocess
import tempfile
import pathlib
import xml.etree.ElementTree as ET
okularbm=pathlib.Path.home().joinpath('.local', 'share', 'okular', 'bookmarks.xml')
pdf_file=pathlib.Path(sys.argv[1])
if not okularbm.is_file():
		print("file '"+str(okularbm)+"' not found")
		exit(1)

if not pdf_file.is_file():
		print("file '"+str(pdf_file)+"' not found")
		exit(2)

localuri=""		
localuri="file://"+str(pdf_file.resolve())
tree=ET.parse(okularbm)		
root=tree.getroot()
page_numbers = []
titles  = []
bookmarks =""
title=""
output=""
for folder in root.iter('folder'):
    if localuri == folder.attrib['href']:
        for bookmark in folder.iter('bookmark'):
            page_numbers.append(bookmark.attrib['href'].split('#')[1].split(';')[0])
            title=bookmark.find('title').text.encode("ascii","xmlcharrefreplace").decode()
            print(title)
            titles.append(title)  
   
for i  in range(len(titles)):
		bookmarks +="BookmarkBegin\n"
		bookmarks +="BookmarkTitle: "+str(titles[i])+"\n"
		bookmarks +="BookmarkLevel: 1"+"\n"
		bookmarks +="BookmarkPageNumber: "+str(int(page_numbers[i])+1)+"\n"

bmfile="bookmarks.txt"
if os.path.isfile(bmfile):
    os.remove(bmfile)

newbookmarks="newbookmarks.txt"
if os.path.isfile(newbookmarks):
    os.remove(newbookmarks)

print("Yerimleri çıkartılıyor")
result=os.system("pdftk '" + str(pdf_file) + "' dump_data output " + bmfile)
line_number=0
lines=0
fbm=open(bmfile,"r")
bmlines=fbm.readlines()
for line in bmlines:
     lines +=1
     if "BookmarkPageNumber" in line:
         line_number =lines
         
newbm=open(newbookmarks,"a+")
line=""
for i in range(0, line_number):
     newbm.write(bmlines[i])
   
newbm.writelines(bookmarks)
for i in range(line_number+1, len(bmlines)):
     newbm.write(bmlines[i])
    
fbm.close()
newbm.close()
newpdf=str(pdf_file) + ".new.pdf"
if os.path.isfile(newpdf):
    os.remove(newpdf)
    
print("'"+newpdf+"' yazılıyor...")
result=os.system("pdftk '" + str(pdf_file) + "' update_info " + newbookmarks + " output '" + newpdf+"'")

#if os.path.isfile(bmfile):
    #os.remove(bmfile)

#if os.path.isfile(newbookmarks):
    #os.remove(newbookmarks)
exit(0)
