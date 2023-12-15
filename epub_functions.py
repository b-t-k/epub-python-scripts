import os, zipfile
from lxml import etree #for Title extract

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

# Function to extract title metadata
# https://stackoverflow.com/questions/3114786/python-library-to-extract-epub-information
def getEpubtitle(epubFile):
    zip_content = zipfile.ZipFile(epubFile)

    def xpath(element, path):
        return element.xpath(
            path,
            namespaces={
                "n": "urn:oasis:names:tc:opendocument:xmlns:container",
                "pkg": "http://www.idpf.org/2007/opf",
                # "dc": "http://purl.org/dc/elements/1.1/",
            },
        )[0]
     
    # find the contents metafile
    cfname = xpath(
        etree.fromstring(zip_content.read("META-INF/container.xml")),
        "n:rootfiles/n:rootfile/@full-path",
    ) 

    # grab the metadata block from the contents metafile
    metadata = xpath(
        etree.fromstring(zip_content.read(cfname)), "/pkg:package/pkg:metadata"
    )

    #set namespace
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}

    # Use XPath to find the dc:title element
    title_elements = metadata.xpath('//dc:title', namespaces=ns)

    # Check if dc:title exists and return its text or "missing" if not found
    if title_elements:
        print(title_elements)
        return title_elements[0].text
    else:
        return "title_missing"
