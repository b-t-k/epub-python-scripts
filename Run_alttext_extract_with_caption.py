#! /usr/bin/python3
# coding: utf-8
# version 0.2

import os
from bs4 import BeautifulSoup
import xlsxwriter
import shutil
from epub_functions import getEpubtitle,getinputfile,open_and_get
from epub_functions import getlistoffiles


### Set inputs
epubFile=None
# epubFile="/Volumes/test files/Working/test.epub"

###### START
epubFile= getinputfile(epubFile)
Exportfolder,epubfiles = open_and_get(epubFile)


## Use Function to extact title from metadata
epubTitle = getEpubtitle(epubFile)
print("TITLE: ",epubTitle)

base_filename = '../' + epubTitle + '-alttext.xlsx'

# Check if the file exists
filename = base_filename
file_exists = os.path.exists(filename)
counter = 1

# If it exists, append '-1' (or higher number) to the file name
while file_exists:
    filename = '../' + epubTitle + f'-alttext-{counter}.xlsx'
    file_exists = os.path.exists(filename)
    counter += 1

# Define and format XLSX file with the final filename
workbook = xlsxwriter.Workbook(filename)
workbook.set_size(1200, 1200)
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})
text_format = workbook.add_format({'text_wrap' : True})
worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 30)
worksheet.set_column('C:C', 50,text_format)
worksheet.set_column('D:D', 50,text_format)


worksheet.write('A1',  'filename', bold )
worksheet.write('B1',  'img file', bold )
worksheet.write('C1',  'alt text', bold )
worksheet.write('D1',  'caption text', bold )

# run Function to travese files and make a list of paths & files ending in xhtml
epubfiles = getlistoffiles(Exportfolder)
# print(epubfiles)

def finddivs():

# Inside this div, find the <p> tag that comes after an <img>
    if div:
        img = div.find('img')
        if img:
            p_tag = img.find_next_sibling('p')
            if p_tag:
                print(p_tag.text)
                if p_tag != None:
                    epubcaption=(p_tag.text)
                else:
                    epubcaption="No_Caption"


### Loop through list of files
cell=1
for file in epubfiles:
    # print(file)
    # Open file and use soup to find all img and alt
    with open(file, 'r') as inp:
            data = inp.read()
            soup = BeautifulSoup(data, "html.parser")
            #find all img tags
            imgtag = soup.find_all('figure')
            # if not empty
            if imgtag != "":
                for alttext in imgtag:
                    
                    # find base file, img name and alt text
                    epubfileName = os.path.basename(file)
                    # print(epubfileName)
                    # print(alttext)
                    epubimgName = os.path.basename(alttext.find('img')['src'])
                    imagetest = alttext.find('img')
                    if imagetest.has_attr('alt'):
                        epubAlttext= alttext.find('img')['alt']
                    else:
                        epubAlttext="none"
                    
                    if epubAlttext=="":
                        epubAlttext="PRESENTATION"

                    epubCaptiontext= alttext.find('figcaption')

                    # if epubCaptiontext != None:
                    #     epubcaption=(epubCaptiontext.text)
                    # else:
                    #     epubcaption="No_Caption"
                
                    # epubAltcredit="No_Credit"


                    if epubCaptiontext is not None:
                        epubcaption = epubCaptiontext.text

                        if epubCaptiontext.find('span') is not None:
                            epubAltcredit = epubCaptiontext.find('span').text
                    else:
                        epubcaption = "No_Caption"
                        epubAltcredit = "No_Credit"

                    # # Write to excel
                    worksheet.write(cell, 0, epubfileName)
                    worksheet.write(cell, 1, epubimgName)
                    worksheet.write(cell, 2, epubAlttext)
                    worksheet.write(cell, 3, epubcaption)
                    worksheet.write(cell, 4, epubAltcredit)
                    cell=cell+1

            ## Redo the loop to check if the img's are in divs instead of proper figures

            divs = soup.find_all('div')

            if divs:
                for div in divs:
                    img = div.find('img')
                    # if img:
                    if img and not img.find_parent('figure'):  # Make sure it's not inside a figure

                        # Check if the img tag has an 'alt' attribute
                        if img.has_attr('alt'):
                            epubAlttext = img['alt']
                        else:
                            epubAlttext = "none"
                        
                        if epubAlttext=="":
                            epubAlttext="PRESENTATION"
                            
                        # Find the next sibling <p> tag
                        p_tag = img.find_next_sibling('p')
                        if p_tag:
                            epubcaption = p_tag.text
                        else:
                            epubcaption = "No_Caption"
                        
                        # Assuming worksheet and cell are defined elsewhere
                        worksheet.write(cell, 0, file)
                        worksheet.write(cell, 1, img['src'])
                        worksheet.write(cell, 2, epubAlttext)
                        worksheet.write(cell, 3, epubcaption)
                        cell += 1
workbook.close()

### Delete folder
shutil.rmtree(Exportfolder)
