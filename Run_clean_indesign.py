import os, re, shutil
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
# epubFile="/Volumes/Working/test/epub_file_name.epub"

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

        #loop through regex replacements list
        for regex1 in list_replace:
            searchtermv =  regex1[0]
            replacetermv = regex1[1]

            replace_text = replacetermv

            data = re.sub(searchtermv, replace_text, data)
            # print (searchtermv, replace_text)

        with open(filename, 'w') as output:
            output.write(data)
            output.close()
        # print(data)

# run Standard ebooks clean command before recompressing folder. This is a script from the Standard ebooks toolset. It can be dangerous becasue it will lowercase all the style names in the css file but not in the epub xhtml files themselves. And of course you have to install the entire toolset—which I think you should do  because you really want to help contribute to the project :-) https://standardebooks.org/contribute
# os.system("se clean .")

### recompress and rename epub
compress(Exportfolder)
### delete working folder
shutil.rmtree(Exportfolder)