import os, re
from epub_functions import getlistoffiles
from epub_functions import extract as extr
from epub_functions import compress 
from list_clean_indesign import list_delete, list_replace


### Open folder, loop though files, and do search and replaces from external lists (indesign.py)

# - delete crud
# - replace rorohiko
# - clean up figures, img, figcaptions
# - move spaces outside spans

## Get input file
epubFile = input("Copy & paste path of epub (right-click -> opt+copy): ")
# epubFile="/Volumes/Orca/Working/test/Walls-working.epub"

## Use function to Extract epub files
extr(epubFile)

## Split to remove .epub from path
Exportfolder=(epubFile.split('.')[0])

### Get working folder and change directory
print (Exportfolder)
# print(os.getcwd())
os.chdir(Exportfolder)

## run Function to travese files and make a list of paths & files ending in xhtml
epubfiles = getlistoffiles(Exportfolder)
# print (epubfiles)

# exit()

#Search all files and apply regex from list
for filename in epubfiles:
    with open(filename, 'r') as inp:
        # print(filename)
        data = inp.read()

        #loop through delete/simple substitution list
        for regex2 in list_delete:
            searchtermv =  regex2[0]
            replacetermv= regex2[1]

            replace_text =  replacetermv
            search_text = r'searchtermv'

            data = re.sub(searchtermv, replace_text, data)
            # exit()

        #loop through regex replacements
        for regex1 in list_replace:
            searchtermv =  regex1[0]
            replacetermv = regex1[1]

            replace_text = replacetermv

            data = re.sub(searchtermv, replace_text, data)
            # print (searchtermv, replace_text)
            # exit()
        # print (data)
        with open(filename, 'w') as output:
            output.write(data)
            output.close()
        # print(data)

# run Standard ebooks clean command before recompressing folder
os.system("se clean .")
### recompress and rename epub
compress(Exportfolder)