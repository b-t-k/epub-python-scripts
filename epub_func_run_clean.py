import os, zipfile
import re
import shutil
import sys
from datetime import datetime
from epub_functions import rename_files, getlistoffiles, get_file
from epub_functions import extract as extr
from epub_functions import clean_and_close, add_items_to_epub
# from Run_add_adpage_new import add_ads_to_epub


def clean_epub(epubFile, newcssfile, list_delete, list_replace, pages_list, list_nav, pages_list_fiction, opf_file1, opf_file2, digitalrights,newFileEnding):
    print(epubFile)
    extr(epubFile)

    Exportfolder = epubFile.split('.')[0]
    os.chdir(Exportfolder)

    epubfiles = rename_files(Exportfolder) # renames older .html to .xhtml
    epubfiles = getlistoffiles(Exportfolder)

    opffile,_ = get_file(Exportfolder,"opf")
    cssfile,_ = get_file(Exportfolder,"css")
    coverfile,_ = get_file(Exportfolder,"cover")
    imagefolder,imagefolderpath = get_file(Exportfolder,"imagefolder")
    print(imagefolder,imagefolderpath)
    nav_file,_ = get_file(Exportfolder,"nav")

    def apply_regex_patterns(filename, regex_list):
        for named_files in regex_list:
            for named_file in named_files[0]:
                if re.match(named_file, os.path.basename(filename)):
                    print("MATCH: " + os.path.basename(filename))
                    with open(filename, 'r') as inp:
                        data = inp.read()
                        for regex in named_files[1]:
                            searchterm2 = regex[0]
                            replaceterm2 = regex[1]
                            data = re.sub(searchterm2, replaceterm2, data)
                    with open(filename, 'w') as output:
                        output.write(data)

    for filename in epubfiles:
        print("Loop File: " + filename)
        if filename != nav_file:
            with open(filename, 'r') as inp:
                data = inp.read()
                #loop through delete/simple substitution list
                for regex2 in list_delete:
                    searchtermv =  regex2[0]
                    replacetermv= regex2[1]

                    replace_text =  replacetermv
                    search_text = r'searchtermv'

                    data = re.sub(searchtermv, replace_text, data)

                for regex1 in list_replace:
                    searchtermv = regex1[0]
                    replacetermv = regex1[1]
                    data = re.sub(searchtermv, replacetermv, data)
            
            with open(filename, 'w') as output:
                output.write(data)

        if filename == nav_file:
            with open(filename, 'r') as inp:
                data = inp.read()
                for regex1 in list_nav:
                    searchtermv = regex1[0]
                    replacetermv = regex1[1]
                    data = re.sub(searchtermv, replacetermv, data)
            with open(filename, 'w') as output:
                output.write(data)

        apply_regex_patterns(filename, pages_list)
        apply_regex_patterns(filename, pages_list_fiction)

    filename = opffile
    with open(filename, 'r') as inp:
        data = inp.read()
        for regex in opf_file1:
            search_string = regex[0]
            replace_string = regex[1]
            data = re.sub(search_string, replace_string, data)

        mod_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        search_date = '<meta property="dcterms:modified">.*?</meta>'
        replace_date = f'<meta property="dcterms:modified">{mod_date}</meta>'
        data = re.sub(search_date, replace_date, data)

        for regex in opf_file2:
            search_string = regex[0]
            replace_string = regex[1]
            data = re.sub(search_string, replace_string, data)
            
    with open(filename, 'w') as output:
        output.write(data)

    sys_path = sys.path[0]
    shutil.copy2(sys_path + newcssfile, cssfile)
    
    ## Add Digital rights file with correct css
    # extract the relative path between cover file and css file
    filepath=os.path.dirname(coverfile)
    css_path=os.path.dirname(cssfile)
    rel_css_path=os.path.relpath(css_path,filepath) + "/"

    itemlist = [
        ["digitalrights.xhtml", digitalrights, "front"],
        # ["logo_book_publishers.png"]
    ]

    add_items_to_epub(itemlist, opffile, cssfile, imagefolder, imagefolderpath, filepath)

    # Read, modify, and rewrite the file in a single step
    with open(filepath+"/digitalrights.xhtml", "r+") as file:
        data = file.read()
        search_string = "INSERT_CSS_PATH_HERE"
        replace_string = rel_css_path + 'styles.css'
        data = re.sub(search_string, replace_string, data)
        
        # Move the file pointer to the beginning and overwrite the file
        file.seek(0)
        file.write(data)
        file.truncate()

    ## Adds logos and fonts based on series
    # seriesname = add_ads_to_epub(Exportfolder)
    # if seriesname is not None:
    #     # Read, modify, and rewrite the file in a single step
    #     with open(filepath+"/titlepage.xhtml", "r+") as file:
    #         data = file.read()
    #         search_string = '<img alt="Logo: Orca SERIES_NAME" src="image/orca_NAME_logo.png"/>'
    #         replace_string = '<img alt="Logo: Orca ' + seriesname + '" src="image/orca_' + seriesname.lower() + '_logo.png"/>'
    #         data = re.sub(search_string, replace_string, data)
            
    #         # Move the file pointer to the beginning and overwrite the file
    #         file.seek(0)
    #         file.write(data)
    #         file.truncate()
        
    #     # function to copy fonts
    #     from epub_add_fonts import add_fonts
    #     add_fonts(seriesname,cssfile,opffile,Exportfolder)

    clean_and_close(Exportfolder,newFileEnding)
