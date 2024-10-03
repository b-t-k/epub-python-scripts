import os, re
from epub_functions import getinputfile, get_file,open_and_get,clean_and_close
from lists.list_clean_indesign import list_delete, opf_file
# from lists.list_digitalrights import digitalrights


### Open folder, loop though files, and do search and replaces from external lists (lists/list_clean_indesign.py)

# - delete crud
# - replace rorohiko
# - clean up figures, img, figcaptions
# - move spaces outside spans
# - rename nav file
# - rename css file
# - edit .opf file for above name changes
# - add css path to cover

### Set inputs
epubFile=None
# epubFile="/Volumes/test files/Working/test.epub"

###### START
epubFile= getinputfile(epubFile)

Exportfolder,epubfiles = open_and_get(epubFile)
# filepath,file_folder = findFilePath(Exportfolder)

########################################
########################################
### To be added/used if I ever want to use InDesign's pagenumber function

# from working_Func_shift_pagenumbers import Func_shift_pagenumbers

### run function to shift page numbers from indesign files
# Func_shift_pagenumbers(Exportfolder)

########################################
########################################

#Search all files and apply regex from list
for filename in epubfiles:
    with open(filename, 'r') as inp:
        # print(filename)
        data = inp.read()

        #loop through delete/simple substitution list
        for regex1 in list_delete:
            searchtermv =  regex1[0]
            replacetermv= regex1[1]

            # search_text = searchtermv
            # replace_text =  replacetermv

            # data = re.sub(search_text, replace_text, data)
            # data = re.sub(searchtermv, replacetermv, data,flags=re.DOTALL)
            # not sure why I had the DOTALL as it seems to grab too much?
            data = re.sub(searchtermv, replacetermv, data)
            # exit()

        # #loop through regex replacements
        # for regex2 in list_replace:
        #     searchtermv =  regex2[0]
        #     replacetermv = regex2[1]

        #     # replace_text = replacetermv

        #     data = re.sub(searchtermv, replacetermv, data)
        #     # print (searchtermv, replacetermv)
        #     # exit()

        # print (data)
        with open(filename, 'w') as output:
            output.write(data)
            output.close()
        # print(data)

    ## rename nav and css files
    if os.path.basename(filename) == 'toc.xhtml':
        file_name = os.path.basename(filename)
        nav_path=os.path.dirname(filename)+"/"
        os.rename(filename, nav_path + 'nav.xhtml')


# rename css file
css_file,css_path=get_file(Exportfolder,"css")
# css_path=os.path.dirname(css_file) +"/"
print(css_file)
print(css_path)

if os.path.basename(css_file) ==  'idGeneratedStyles.css':
    os.rename(css_path + 'idGeneratedStyles.css', css_path + 'styles.css')

# open opf file and make changes
opffile,_ = get_file(Exportfolder,"opf")
with open(opffile, 'r') as inp:
    # print(filename)
    # print(os.getcwd())
    data = inp.read()
    # print (data)
    for regex in opf_file:
        search_string = regex[0]
        replace_string= regex[1]

        data = re.sub(search_string, replace_string, data)

with open(opffile, 'w') as output:
    output.write(data)
    output.close()

# open cover file and add css file
coverfile,_ = get_file(Exportfolder,"cover")
print("coverfile")
with open(coverfile, 'r') as inp:
    data = inp.read()

    # extract the relative path between cover file and css file
    rel_css_path=os.path.relpath(css_path,os.path.dirname(coverfile)) + "/"

    search_string = '</title>'
    replace_string= '</title>\n<link href="' + rel_css_path + 'styles.css" rel="stylesheet" type="text/css"/>'

    data = re.sub(search_string, replace_string, data)

with open(coverfile, 'w') as output:
    output.write(data)
    output.close()

clean_and_close(Exportfolder, skip_check=True)