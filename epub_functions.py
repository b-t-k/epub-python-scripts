import os, zipfile

### Extract files from epub
def extract(inputFolder):
    epubFile = zipfile.ZipFile(inputFolder, 'r')
    epubFile.extractall(inputFolder[:-5])
    epubFile.close()

### Recompress folder into epub with _rev ending
def compress(Exportfolder):
    ### Change back to top directory
    os.chdir("..")
    if (os.path.isdir(Exportfolder)):
        epubFile = zipfile.ZipFile(Exportfolder + "_rev.epub", 'w', zipfile.ZIP_STORED)
        epubFile.writestr('mimetype', 'application/epub+zip')
        
        os.chdir(Exportfolder)
        
        for root, dirs, files in os.walk("."):
            for file in files:
                # print(root, file)
                if file !='mimetype':
                    epubFile.write(os.path.join(root, file), compress_type=zipfile.ZIP_DEFLATED)
        epubFile.close()
    else:
        print("wrong directory")

    ## Change back to top directory
    os.chdir("..")
    # print(os.getcwd())

### change directory to current folder and get list of .xhtml
def getlistoffiles(Exportfolder):
    ## get list of files
    os.chdir(Exportfolder)
    # print(os.getcwd())
    items=[]
    files=""
    for root, dirs, files in os.walk("."):
        for file in files:
            # print(file)
            if file.endswith(".xhtml"):
                items.append(root + "/" + file)
            if file.endswith(".html"):
                items.append(root + "/" + file)
    print("Retrieved .xhtml filenames")
    # print(items)
    return(items)

