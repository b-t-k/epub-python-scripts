import os, re, shutil
from pathlib import Path
from epub_functions import get_file,getinputfile,clean_and_close, open_and_get

########################################################
###################################################
# Rename .png files to .jpg files based on a folder. It also deletes the old pngs and copies in the new jpg files. For use when bulk shinking images InDesign decided where better off as png and you want to switch them to jpgs
########################################################


# NOTE: Use inputFile for epubFile and new image folder
### get epub file
inputFile=None
# inputFile="/Volumes/Orca/Working/TESTING/Bus to the Badlands_rev-ads.epub"
epubFile = getinputfile(inputFile)

### get excel file
inputFile=None
# inputFile="/Volumes/Orca/Working/TESTING/Bus to the Badlands-alttext.xlsx"
jpgfolder = getinputfile(inputFile,"jpeg folder")

newFileEnding= "_updated"


################### FUNCTIONs ######################
###################################################
### Function to search for image and change file endings
def imagereplace(file_path,imgnames):

    # Read the content of the file
    with open(file_path, 'r') as file:
        data = file.read()

    # Replace each term.png with term.jpg
    for term in imgnames:
        data = data.replace(f"{term}.png", f"{term}.jpg")

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(data)


def imagereplace_opf(file_path,imgnames):

    # Read the content of the file
    with open(file_path, 'r') as file:
        data = file.read()

    # Replace each term.png with term.jpg
    for term in imgnames:
        data = data.replace(f"{term}.png", f"{term}.jpg")

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(data)
############################
###################################################
###################################################


#########################
## Set parameters
########################

# Get a list of files in the folder
# file_list = os.listdir(jpgfolder)
file_list = []

# Iterate over each file in the folder and strip ending from jpg files
for file in os.listdir(jpgfolder):
	# Check if the file ends with ".jpg"
	if file.endswith(".jpg"):
		file=Path(file).stem
		# Add the file to the list
		file_list.append(file)

###### START ######
Exportfolder,epubfiles = open_and_get(epubFile)

print("file count: " + str(len(epubfiles)))
filecount=len(epubfiles)

## get path and filename of  .opf and .css file 
opffile,_ = get_file(Exportfolder,"opf")

### get folder where image files are stored
### get the path of the folder
imagefolder,imagefolderpath = get_file(Exportfolder,"imagefolder")

## run function to open each xhtml file and loop though file list to perfomr sarch and replace
for filename in epubfiles:
    newdata = imagereplace(filename,file_list)        

## open opf file and replace png entries in manifest with jpg
filename = opffile
with open(filename, 'r') as inp:
    print(filename)
    # print(os.getcwd())
    data = inp.read()
    # print (data)

    for term in file_list:
        # data = data.replace(f"{term}.png", f"{term}.jpg")

    ## search for manifest and add series file name
        search_string = f'<item id="{term}.png" href="{imagefolder}{term}.png" media-type="{imagefolder}png"/>'

        replace_string= f'<item id="{term}.jpg" href="{imagefolder}{term}.jpg" media-type="{imagefolder}jpeg"/>'

        data = re.sub(search_string, replace_string, data)
        # search for other order
        search_string = f'<item href="{imagefolder}{term}.png" id="{term}.png" media-type="{imagefolder}png"/>'
        
        replace_string= f'<item id="{term}.jpg" href="{imagefolder}{term}.jpg" media-type="{imagefolder}jpeg"/>'

        data = re.sub(search_string, replace_string, data)

with open(filename, 'w') as output:
    output.write(data)
    output.close()


## remove old png files from image folder
for term in file_list:
    os.remove(imagefolderpath + "/" + term + ".png")

##add new jpg img files
if not os.path.exists(imagefolderpath):
    print("Destination Image Folder Does not exist")
    exit()

# Loop through all files in the source directory
for filename in os.listdir(jpgfolder):
    source_file = os.path.join(jpgfolder, filename)
    
    # Only copy if it's a file (not a directory) and ends in .jpg
    if os.path.isfile(source_file) and filename.lower().endswith('.jpg'):
        dest_file = os.path.join(imagefolderpath, filename)
        shutil.copy2(source_file, dest_file)
        # print(f"Copied {source_file} to {dest_file}")


clean_and_close(Exportfolder,newFileEnding)