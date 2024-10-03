import re
from epub_functions import getinputfile,open_and_get,findFilePath,clean_and_close


# this script searches the files for asides and auto numbers them. There are two basic patterns: 
# 1)
#   <aside aria-label="Sidebar_ID-XXX" class="quote">
# or
# 2)
#   <aside aria-labelledby="idea-XXX" class="idea">
#      <h2 id="idea-XXX" class="idea">


### Set inputs
epubFile=None
# epubFile="/Volumes/test files/Working/test.epub"

newFileEnding= "_asides"

# set pattern for searches
pattern_list = [
  # set patterns:
  # pattern-type , pattern-id, pattern-class 
    [1, "facts XXX", "facts"],
    [1, "people XXX", "people"],
    # [1, "watery XXX", "watery"],
    # [1, "Copy That XXX", "copy"],
    [2, "people-XXX", "people"],
    [2, "sidebar-1-XXX", "sidebar-1"],
    [2, "sidebar-2-XXX", "sidebar-2"],
    [2, "question-XXX", "question"],
    [2, "tilt-XXX", "tilt"],
]

# Function to replace -XXX with increment
def replace_aside_ids(content, base_id, base_class, pattern_number, counter):
    if pattern_number == 1:
        # Pattern 1
        pattern = re.compile(rf'<aside aria-label="{base_id}" class="{base_class}">')
        base_label = f"{base_class} "

    # elif pattern_number == 2:
    #     # Pattern 2
    #     pattern = re.compile(rf'<aside aria-labelledby="{base_id}" class="{base_class}">\n*\t*\s*<h2 (id="{base_id}" class="{base_class}"|class="{base_class}" id="{base_id}")>')
    #     base_label = f"{base_id[:-3]}"

    elif pattern_number == 2:
        # Pattern 2
        pattern = re.compile(rf'<aside aria-labelledby="{base_id}" class=".*?">\n*\t*\s*<h2 (id="{base_id}" class="{base_class}"|class=".*?" id="{base_id}")>')
        base_label = f"{base_id[:-3]}"

    # Function to replace each match with an incremented ID
    def replacer(match):
        nonlocal counter
        new_id = f"{base_label}{counter}"
        replacement = match.group(0).replace(base_id, new_id)
        counter += 1
        return replacement

    # Perform the substitution
    new_content = pattern.sub(replacer, content)

    return new_content, counter +1


###### START
epubFile= getinputfile(epubFile)

###### START ######
Exportfolder,epubfiles = open_and_get(epubFile)
# filepath,file_folder = findFilePath(Exportfolder)

# Initialize counters for each pattern number
initial_counters = {1: 1, 2: 1}

# Search all files for pagebreak and replace with new string plus increment
# for filename in epubfiles:
#     with open(filename, 'r') as inp:
#         data = inp.read()
        
#         for pattern_list_item in pattern_list:
#             pattern_number = pattern_list_item[0]
#             base_id = pattern_list_item[1]
#             base_class = pattern_list_item[2]
            
#             # Use and update the counter for the current pattern number
#             data, counters[pattern_number] = replace_aside_ids(data, base_id, base_class, pattern_number, counters[pattern_number])
        
#         with open(filename, 'w') as output:
#             output.write(data)

for filename in epubfiles:
    # Create a new counter dictionary for each file, starting from initial_counters
    counters = initial_counters.copy()

    with open(filename, 'r') as inp:
        data = inp.read()
        
        for pattern_list_item in pattern_list:
            pattern_number = pattern_list_item[0]
            base_id = pattern_list_item[1]
            base_class = pattern_list_item[2]
            
            # Use and update the counter for the current pattern number
            data, counters[pattern_number] = replace_aside_ids(data, base_id, base_class, pattern_number, counters[pattern_number])
        
        # Write the updated data back to the file
        with open(filename, 'w') as output:
            output.write(data)

clean_and_close(Exportfolder,newFileEnding)

