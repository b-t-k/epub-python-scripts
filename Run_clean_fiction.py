from lists.list_clean_epub_all import list_delete, list_replace, pages_list, opf_file1
from lists.list_clean_epub_fiction import list_nav, pages_list_fiction, opf_file2
from lists.list_digitalrights import digitalrights
from epub_func_run_clean import clean_epub

from epub_functions import getinputfile


### Set inputs
epubFile=None
# epubFile="/Volumes/test files/Working/test.epub"

newFileEnding= "_rev"
newcssfile = "/css/CSS-fiction-base.css"

# input("Press Enter to continue...")

###### START
epubFile = getinputfile(epubFile)
print(epubFile)

##@ Run epub_func_run_clean.py
clean_epub(epubFile, newcssfile, list_delete, list_replace, pages_list, list_nav, pages_list_fiction, opf_file1, opf_file2, digitalrights, newFileEnding)
