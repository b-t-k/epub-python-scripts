#! /usr/bin/python3
# coding: utf-8
# version 0.2

import os
from bs4 import BeautifulSoup
import xlsxwriter
import shutil

from epub_functions import extract as extr
from epub_functions import getEpubtitle
from epub_functions import getlistoffiles

## Get input file
epubFile = input("Copy & paste path of epub (right-click -> opt+copy): ")
# epubFile="/Users/admin/Desktop/Animal Minds-working_working_rev.epub"

## Use function to Extract epub files
extr(epubFile)

## Split to remove .epub from path
Exportfolder=(epubFile.split('.')[0])

### Get working folder and change directory
print (Exportfolder)
# print(os.getcwd())
os.chdir(Exportfolder)

### Set input file
inputFile=os.path.basename(epubFile)

## Use Function to extact title from metadata
epubTitle = getEpubtitle(epubFile)

## Define and format XLSX file
workbook = xlsxwriter.Workbook('../' + epubTitle + '-alttext.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})
text_format = workbook.add_format({'text_wrap' : True})
worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 30)
worksheet.set_column('C:C', 50,text_format)

worksheet.write('A1',  'filename', bold )
worksheet.write('B1',  'img file', bold )
worksheet.write('C1',  'alt text', bold )

# run Function to travese files and make a list of paths & files ending in xhtml
epubfiles = getlistoffiles(Exportfolder)
# print(epubfiles)

# set spreadsheet starting place
cell=1

### Loop through list of files
for file in epubfiles:
    print(file)
    # Open file and use soup to find all img and alt
    with open(file, 'r') as inp:
            data = inp.read()
            soup = BeautifulSoup(data, "html.parser")
            #find all img tags
            imgtag = soup.findAll('img')
            # if not empty
            if imgtag != "":
                for alttext in imgtag:
                    # find base file, img name and alt text
                    epubfileName = os.path.basename(file)
                    epubimgName = os.path.basename(alttext['src'])
                 
                    if alttext.has_attr('alt'):
                        epubAlttext= alttext['alt']
                    else:
                        epubAlttext="none"
                    
                    if epubAlttext=="":
                        epubAlttext="PRESENTATION"
                
                    # # Write to excel
                    worksheet.write(cell, 0, epubfileName)
                    worksheet.write(cell, 1, epubimgName)
                    worksheet.write(cell, 2, epubAlttext)
                    cell=cell+1
workbook.close()

### Delete folder
shutil.rmtree(Exportfolder)
