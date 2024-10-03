from epub_func_run_clean import clean_epub
from lists.list_clean_epub_all import list_delete, list_replace, pages_list, opf_file1
from lists.list_clean_epub_nonfiction import list_nav, pages_list_nonfiction, opf_file2
from lists.list_digitalrights import digitalrights
from epub_functions import getinputfile


### Set inputs
epubFile=None
# epubFile="/Volumes/test files/Working/test.epub"

newFileEnding = "_2"
newcssfile = "/css/CSS-non-fiction.css"

###### START
epubFile= getinputfile(epubFile)

clean_epub(epubFile, newcssfile, list_delete, list_replace, pages_list, list_nav, pages_list_nonfiction, opf_file1, opf_file2, digitalrights, newFileEnding)
