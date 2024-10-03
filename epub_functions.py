import os, zipfile, re, glob
import shutil
import pathlib
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime

### Epub Functions
# open_and_get
    # extract
# getinputfile
# clean_and_close
    # compress
# get_file
# getlistoffiles
# getfilelocation
# rename_files
# getEpubtitle

### Series of functions to add files to epubs
# add_items_to_epub
	# load_file
	# create_directory
	# handle_file
	# write_file
	# add_to_manifest
	# add_to_spine
	# append_css

### not in use
# sortby
# getspinelist
# runloops

def open_and_get(epubFile):

    extract(epubFile)

    ## Split to remove .epub from path
    Exportfolder=(epubFile.split('.')[0])

    ### Get working folder and change directory
    print (Exportfolder)
    # print(os.getcwd())
    os.chdir(Exportfolder)

    ## run Function to travese files and make a list of paths & files ending in xhtml
    epubfiles = getlistoffiles(Exportfolder)

    return(Exportfolder,epubfiles)


### Extract files from epub
def extract(inputFolder):

    epubFile = zipfile.ZipFile(inputFolder, 'r')
    epubFile.extractall(inputFolder[:-5])
    epubFile.close()


## get the epub (or other input) file from string or drag and drop
def getinputfile(inputFile=None,importFilename=None):
    """
    A function to display a message to drag a file to the window which returns a string
    """
    if inputFile is None:
        if importFilename is None:
            importFilename="epub file"
        inputFile = input (f"\nCopy & paste path of the {importFilename} (right-click -> opt+copy)\nor drag the folder into the terminal window: ")
    
    ##clean osx quotes from drag and drop
    inputFile = inputFile[1:-1] if inputFile.startswith("'") and inputFile.endswith("'") else inputFile
    print("Inputfile ",inputFile)
    if not os.path.exists(inputFile):
        print("\n\nNO FILE. Did you remember to change the file path?\n")
        exit()

    path = pathlib.Path(inputFile)
    if not path.exists():
        print("Path is invalid")
        exit()

    return(inputFile)

def clean_and_close(Exportfolder, ending=None, skip_check=False):
    ## Cleans and compresses the EPUB files in Exportfolder.
    ## ending is the suffix to add to the compressed EPUB filename. Defaults to None.
    ## skip ahead to compress if skip_check=True is passed
    
    if skip_check: #and os.path.basename(__file__) == "Run_clean_indesign.py":
        compress(Exportfolder, ending or "_rev")
        shutil.rmtree(Exportfolder)
        print("FUNCTION SKIPPED THE CLEAN PROCESS")
        return
    
    opffile,_ = get_file(Exportfolder, "opf")
    with open(opffile, 'r') as inp:
        data = inp.read()
        soup = BeautifulSoup(data, 'xml')
        findDesc = soup.find('dc:description')
        
        # Run Standard eBooks clean command before recompressing folder
        os.system('find . -name ".DS_Store" -type f -delete')
        os.system("se clean .")
        
        if findDesc is not None:
            soup.find('dc:description').replace_with(findDesc)
        
        newoutput = str(soup)

        ## Change Mod date
        mod_date=datetime.now()
        mod_date=mod_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        # print(mod_date)
        search_date = '<meta property="dcterms:modified">.*?</meta>'
        replace_date = '<meta property="dcterms:modified">' +  mod_date + '</meta>'

        newoutput = re.sub(search_date, replace_date, data)

    
    with open(opffile, 'w') as output:
        output.write(newoutput)

    # Recompress and rename the EPUB file
    compress(Exportfolder, ending or "_rev")
    shutil.rmtree(Exportfolder)



def compress(Exportfolder, ending="_rev"):
    ## Compresses the content of Exportfolder into an EPUB file.
    ## ending (str, optional): The suffix to add to the compressed EPUB filename. Defaults to "_rev".

    epub_filename = f"{Exportfolder}{ending}.epub"

    # Change directory to the parent of Exportfolder
    os.chdir("..")

    if os.path.isdir(Exportfolder):
        # Create the EPUB file
        with zipfile.ZipFile(epub_filename, 'w', zipfile.ZIP_STORED) as epubFile:
            epubFile.writestr('mimetype', 'application/epub+zip')

            # Navigate to the Exportfolder and add all files to the EPUB
            os.chdir(Exportfolder)
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file != 'mimetype':
                        epubFile.write(os.path.join(root, file), compress_type=zipfile.ZIP_DEFLATED)
    else:
        print("Export folder does not exist or is not a directory.")

    # Change back to the top directory
    os.chdir("..")
    # print(os.getcwd())

def get_file(Exportfolder, file_type):
    """
    Find specific files or folders in the Exportfolder based on file_type.
    Returns:
        tuple: Path to the file/folder and its directory path, or (None, None) if no file is found.
    
    Usage:
        css_file = get_file(Exportfolder, "css")[0]
        opf_file, opf_path = get_file(Exportfolder, "opf")
        cover_file, cover_path = get_file(Exportfolder, "cover")
        nav_file, nav_path = get_file(Exportfolder, "nav")
        image_folder,image_folder_path = get_file(Exportfolder, "imagefolder")
        font_folder,font_folder_path = get_file(Exportfolder, "fontfolder")
    """
    search_criteria = {
        "css": {"extensions": [".css"]},
        "opf": {"extensions": [".opf"]},
        "cover": {"extensions": [".xhtml"], "contains": ["cover"]},  # Ensures "cover" and ".xhtml"
        "nav": {"contains": ["nav.xhtml", "toc.xhtml"]},
        "imagefolder": {"extensions": [".jpg", ".png"]},
        "fontfolder": {"extensions": [".otf", ".ttf"]}
    }

    criteria = search_criteria.get(file_type, {})
    
    os.chdir(Exportfolder)
    
    # Special case for image and font folders
        # Special case for image and font folders
    if file_type in ["imagefolder", "fontfolder"]:
        for root, dirs, files in os.walk("."):
            for dir_name in dirs:
                # Check for files within each directory
                folder_path = os.path.join(root, dir_name)
                for file in os.listdir(folder_path):
                    if file.endswith(tuple(criteria.get("extensions", []))):
                        print(f"Got {file_type} Folder: {dir_name} - Path: {folder_path}")
                        return dir_name, folder_path + "/"
    
    # Check for files for other types
    for root, dirs, files in os.walk("."):
        for file in files:
            # Check if the file matches the criteria for both extensions and contains
            extensions_match = "extensions" not in criteria or file.endswith(tuple(criteria["extensions"]))
            contains_match = "contains" not in criteria or any(s in file for s in criteria["contains"])

            if extensions_match and contains_match:
                item = os.path.join(root, file)
                path = os.path.dirname(item) + "/"
                print(f"Got {file_type} File: {path}")
                return item, path

    # Return None, None if no file or folder is found
    return None, None

### change directory to current folder and get list of .xhtml
def getlistoffiles(Exportfolder):
    ##get list of files
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

def getfilelocation(Exportfolder,filename):
            ##get list of files
    os.chdir(Exportfolder)
    # print(os.getcwd())
    for root, dirs, files in os.walk("."):
        for file in files:
            # print(file + " vs "+ filename)
            if file==filename:
                item = root + "/" + file
                print("item: " + item)
                # print("Got " + filename + " File")
                return item

   
    print("Can't find " + filename + " in " + Exportfolder)
    return  "Not Found"

### change directory to current folder and get list of .html and change name to .xhtml
def rename_files(Exportfolder):
    ##get list of files
    os.chdir(Exportfolder)
    # print(os.getcwd())
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                # print(file)
                newname = file.replace('.html', '.xhtml')
                file = os.rename(root + "/" + file, root + "/" + newname)
                # print(root + "/" + file)


def getEpubtitle(epubFile):
    """
    ## Function to extract title metadata
    # https://stackoverflow.com/questions/3114786/python-library-to-extract-epub-information
    """

    zip_content = zipfile.ZipFile(epubFile)

    def xpath(element, path):
        return element.xpath(
            path,
            namespaces={
                "n": "urn:oasis:names:tc:opendocument:xmlns:container",
                "pkg": "http://www.idpf.org/2007/opf",
                "dc": "http://purl.org/dc/elements/1.1/",
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

    # repackage the data
    epubTitle = (str(xpath(metadata, f"dc:title/text()")))
    return epubTitle




###############
# Series of functions to add files to epubs

def add_items_to_epub(itemlist, opffile, cssfile=None, imagefolder=None, imagefolderpath=None, filepath=None, css_string=None, fontfolder=None, fontfolderpath=None):
    # Define storage paths
    image_storage_path = "/images/"
    font_storage_path = "/fonts/"
    
    # Load OPF data
    opf_data = load_file(opffile)

    # Ensure directories exist if provided
    if imagefolderpath:
        create_directory(imagefolderpath)
    if fontfolderpath:
        create_directory(fontfolderpath)

    # Process each item in the list
    for item in itemlist:
        filename = item[0]
        
        # Handle images and XHTML files
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Handle images
            if imagefolder and imagefolderpath:
                handle_file(filename, image_storage_path, imagefolderpath)
                opf_data = add_to_manifest(opf_data, os.path.join(imagefolder, filename), 'image/jpeg' if filename.endswith(('.jpg', '.jpeg')) else 'image/png')
        
        elif len(item) > 1:  # Handle XHTML files
            content = item[1]
            position = item[2] if len(item) > 2 else None
            
            # Check if filepath is provided before writing the file
            # print("FILENAME IS: ", filename)
            # print("FILEPATH IS: ", filepath)
            if filepath is not None:
                write_file(os.path.join(filepath, filename), content)
                opf_data = add_to_manifest(opf_data, filename, 'application/xhtml+xml')
                opf_data = add_to_spine(opf_data, filename, position)
            else:
                print(f"Warning: filepath is None. Cannot write {filename}.")
        
        elif filename.endswith(('.otf', '.ttf')):  # Handle font files
            if fontfolder and fontfolderpath:
                handle_file(filename, font_storage_path, fontfolderpath)
                opf_data = add_to_manifest(opf_data, os.path.join(fontfolder, filename), 'application/x-font-ttf' if filename.endswith('.ttf') else 'application/vnd.ms-opentype')

    # Write the updated OPF data back to the file
    write_file(opffile, opf_data)

    # Append CSS string if provided
    if css_string and cssfile:
        append_css(cssfile, css_string)


def load_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return None

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def handle_file(filename, storagepath, folderpath):
    src = os.path.join(storagepath, filename)
    dst = os.path.join(folderpath, filename)
    try:
        shutil.copy2(os.path.dirname(__file__) + src, dst)
        # print(os.path.dirname(__file__) + src)
    except FileNotFoundError:
        print(f"Error: Image {filename} not found at {src}.")
    except Exception as e:
        print(f"Error: Could not copy {filename} to {folderpath}. Reason: {e}")

def write_file(filepath, content):
    try:
        with open(filepath, 'w') as f:
            f.write(content)
    except Exception as e:
        print(f"Error: Could not write to {filepath}. Reason: {e}")

def add_to_manifest(opf_data, filename, media_type):
    manifest_match = re.search(r'<manifest>(.*?)<\/manifest>', opf_data, re.DOTALL)
    if manifest_match:
        manifest_contents = manifest_match.group(1)

        # Determine if the file is an image based on the media type
        if "image" in media_type:
            item_id = f'x{os.path.basename(filename)}'
        else:
            item_id = os.path.basename(filename)

        # Check if the filename already exists in the manifest
        if re.search(rf'href="{re.escape(filename)}"', manifest_contents):
            # print(f"Item with filename '{filename}' already exists in the manifest.")
            return opf_data

        # Add the new item to the manifest
        new_item = f'\n<item id="{item_id}" href="{filename}" media-type="{media_type}"/>'
        manifest_contents += new_item
        opf_data = opf_data.replace(manifest_match.group(0), f'<manifest>{manifest_contents}\n</manifest>')
    
    return opf_data

def add_to_spine(opf_data, filename, position):
    spine_match = re.search(r'<spine[^>]*>(.*?)<\/spine>', opf_data, re.DOTALL)
    if spine_match:
        spine_contents = spine_match.group(1)
        spine_items = re.findall(r'idref="([^"]+)"', spine_contents)
        if position == "front":
            spine_items.insert(1, os.path.basename(filename))
        elif position == "back":
            spine_items.append(os.path.basename(filename))
        else:
            print(f"Warning: Invalid position '{position}' for {filename}. Adding to the end by default.")
            spine_items.append(os.path.basename(filename))
        new_spine_contents = '\n'.join([f'<itemref idref="{item}"/>' for item in spine_items])
        opf_data = opf_data.replace(spine_match.group(0), f'<spine toc="ncx">\n{new_spine_contents}\n</spine>')
    return opf_data

def append_css(cssfile, css_string):
    try:
        with open(cssfile, 'a') as f:
            f.write(css_string)
    except Exception as e:
        print(f"Error: Could not append to {cssfile}. Reason: {e}")



##### NOT CURRENTLY IN USE

### a function to grab page, turn it into an integer (unless it is a roman numeral), and then designate it as a sort key
### not currently in use
def sortby(x):
    try:
        return int(x[0])
    except ValueError:
        return float('inf')
    

### Currently only used in testing-ConvertTagToPageMarker.py
def getspinelist(Exportfolder):
    spinelist=[]
    #walk through folder to find path of xhtml files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".xhtml"):
                path=root
    # print(path)
    #run function to get opf file
    opffile = get_file(Exportfolder, "opf")

    #open opf and  make list from spine items
    with open(opffile, 'r') as inp:
        data = inp.read()
        soup = BeautifulSoup(data, features="xml")
        spine=soup.find_all('itemref')
        for file in spine:
            spinelist.append(path + "/" +file['idref'])
    print("Got spine list")
    return(spinelist)

def runloops(anchorfile, list, items, search_text,):
    newpagelist=[]
    completepagelist=[]
    
    ### for each link in list extract 3 groups
    for link in list:
        linkurl = re.match(search_text,  link)
        filename=linkurl.group('file')
        anchortext=linkurl.group('anchor')
        pagenum=linkurl.group('page')
        # print( filename + anchortext + pagenum)
        
        ### Loop through files in ebook
        for file in items:
            # print(file)

            ### loop through each file and read html
            with open(file, 'r') as inp:
                data = inp.read()
                # print (file[8:])
                # print (data)

                ### if text after 8th character is equal to filename
                # print (linkurl) 
                # print(file[8:] + ", " + filename)
                if (file[8:]) == filename:
                    # print(anchortext)
                    
                    ### if anchor text in list from index is NOT present in file
                    if data.find(anchortext) == -1:
                        string = file + "\t" +filename + "\t" + anchortext+ "\t" + pagenum + "\n"
                        # print(string)
                        if  anchorfile:
                            anchorfile.write(string)

                        ### write new strings to list in list
                        newpagelist=(filename,anchortext,pagenum)
                        completepagelist.append(newpagelist)
                    # else:
                    #     anchorfile.write(file + ": FOUND"+ "\n")     
    
    return(completepagelist)



# # get text files location based on where the cover is
# def findFilePath(Exportfolder):
#     filepath=os.path.dirname(get_file(Exportfolder, "cover")[1])
#     # print("NEWFILEPATH ",filepath)
#     # split the path to get rid of ./OEBPS/ or ./ops/
#     if filepath.count("/") > 1:
#         file_folder = filepath.split("/",2)[2] + "/"
#     else:
#         file_folder = ""

#     return(filepath,file_folder)


