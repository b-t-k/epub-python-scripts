import os, re
from bs4 import BeautifulSoup
from slugify import slugify
from epub_functions import getfilelocation,getinputfile,open_and_get,clean_and_close

#########################
#  Open glossary.xhtml and list terms. Then search all .xhmtl files for term. Restyle term and write term + filename to list. 
#  Open glossary.xhtml, restyle and add return links.
# - Substitutes in <dt> and <dd> and removes em dashes between in favour of css

### NOTE!
# - Remove links from the beginning of <li> in glossary.xhtml e.g <a id="_idTextAnchor616"/>, this includes <page refs> as well. 
# - Best to move them to the end of the line.

#########################
## Set parameters
########################

### Set inputs
epubFile=None
epubFile="/Volumes/Orca/Working/ W2025 non-fiction/Game Changers/GameChangers_rev.epub"

newFileEnding= "_gloss"

### Choose List to define start and finish of glossary words in body files
# glossary_link_code = ['<b class="glossary-term">', '</b>']
glossary_link_code = ['<span class="glossary-term">', '</span>']
# glossary_link_code = ['<em class="bold-italic">', '</em>']
# glossary_link_code = ['<i class="bold-italic">', '</i>']
# glossary_link_code = ['<span class="bold-italic">', '</span>']
# glossary_link_code = ['<em class="GlossaryBoldItalic">', '</em>']
# glossary_link_code = ['<em class="bold-italic"><em class="bold-italic"><strong>', '</strong</em>']
# glossary_link_code = ['<span class="Bold Italic">', '</span>']
# glossary_link_code = ['<span class="sc">', '</span>']

### Define start and finish of glossary term in glossary itself
search_item = "b"
# search_item = 'dt'
# search_item = 'strong', {'class' : 'Bold'}
# search_item = 'span', {'class' : 'glossary'}
# search_item = 'b', {'class' : 'glossary'}

### Set  format of glossary
glossary_item_code = ['<p class="glossary"><b>', '</b>', '</p>']
# glossary_item_code = ['<li class="glossary"><b>', '</b>', '</li>']
# glossary_item_code = ['<dt class="glossary">', '</dt><dd>','</dd>']
# glossary_item_code = ['<li class="glossary"><em class="bold-italic">', '</em>', '</li>']
# glossary_item_code = ['<li class="glossary"><b>', '</b>', '</li>']
# glossary_item_code = ['<li class="glossary"><span class="glossary-term">', '</span>', '</li>']
# glossary_item_code = ['<li class="GlossaryBody"><span class="GlossaryWords">', '</span>', '</li>']
# glossary_item_code = ['<li class="glossary"><b class="glossary">', '</b>', '</li>']
# glossary_item_code = ['<p class="Glossary"><strong class="Bold">', '</strong>', '</p>']
# glossary_item_code = ['<p class="glossary"><span class="glossary-word">', '</span>', '</p>']

##############################
### FUNCTION to search restyle glossary terms in body files

def glossaryregex(data,glossterm,file,glossary_link_code):
    ### remove spaces from glossterm

    term_id=slugify(glossterm)
    # print(glossterm + " -> " +term_id)

    #escape glossterm to find terms in parentheses
    glossterm_orig = glossterm
    # glossterm = re.escape(glossterm)

    ### Note: Search within glossterm for optional letter 's' (s?), optional comma, optional space (,?\s?), or option letters 'es' (es?) or combinations there-of  

    ## cheat to replace words in parantheses because you can't escape characters in f-strings prior to python 3.12
    p1="("
    p2=")"
    name1="\("
    name2="\)"

    search_text = str(fr'{glossary_link_code[0]}({glossterm.replace(p1, name1).replace(p2, name2).replace(" ", "(?: |&#160;)")}(s?|s\s?|es?|es\s?|\s|,?|.?|,\s?)){glossary_link_code[1]}'    )
    
    replace_text = f'<a aria-label="go to glossary" href="glossary.xhtml#{term_id}" id="{term_id}" class="glossary-term">\\1</a>'

    ### Create empty tuple
    glossarylink=()
    
    ### Count number of substitutions
    checkterm=re.subn(search_text, replace_text, data, flags=re.IGNORECASE)
    ## if not zero then add term and filename to tuple
    if checkterm[1] != 0:
        glossarylink=(glossterm_orig,file)
    
    ### Run regex to sub
    newdata = re.sub(search_text, replace_text, data, flags=re.IGNORECASE)
    # print(file + " | " + glossterm + " | " + term_id)
    
    return(newdata, glossarylink)


####################
## Start 
###################

epubFile= getinputfile(epubFile)
Exportfolder,epubfiles = open_and_get(epubFile)

glossary = getfilelocation(Exportfolder,"glossary.xhtml")

### Make empty list to store Glossary terms in glossary
glossterms=[]

########################
## Find glossary terms (in glossary)


### Use soup to open glossary.xhtml and find glossary terms
with open(glossary, 'r') as text:
    glossarytext = text.read()
    # print (glossarytext)
    soup = BeautifulSoup(glossarytext, "html.parser")
    # print (soup)

    for boldterm in soup.find_all(search_item): 
        ### for each term append to list
        for glossterm in boldterm.contents:
            # print(glossterm)
            ## strip out colons at the end of the terms (Brush's <dt>)
            glossterm= glossterm.replace('—','')

            # print(glossterm)
            glossterms.append(glossterm)

print(len(glossterms))
print(glossterms)

### Make empty list for links
linklist=[]

###############################
### Search files ###

### Search all files for glossary terms (in glossterms) and replace with new string then add add filename and term to linklist
for filename in epubfiles:
    with open(filename, 'r') as inp:
        data = inp.read()
        # print(filename)
        # print(glossary_link_code)
        for glossterm in glossterms:
            # print(glossterm)
            data,glossary_link = glossaryregex(data,glossterm,filename,glossary_link_code)
            # print(data)
            # print(glossary_link)

            ### If not empty add to linklist
            if len(glossary_link) != 0:
                linklist.append(glossary_link)
            # input()            
    
    with open(filename, 'w') as output:
        output.write(data)
        output.close()
        # print(data)

### sort link list
linklist.sort()
# print(linklist)
# print(linklist[2])

############################
### WRITE GLOSSARY.XHTML ###

# ### Open glossary.xhtml and read
# text = open(glossary, 'r')
# glossdata = text.read()

# ### Loop through stored terms and write chapter links from linklist to glossary.xhtml
# for glossterms in linklist:
#     glossterm=(glossterms[0])
#     # print(glossterm)

#     fname=os.path.split(glossterms[1])[1]
#     # print (fname)

#     term_id=slugify(glossterm)
#     # print(term_id)
#     linkpath=fname

#     #escape glossterm to find terms in parentheses
#     glossterm_orig = glossterm
#     glossterm = re.escape(glossterm)

#     search_text = glossary_item_code[0] + glossterm  + '—*' + glossary_item_code[1] + '(.*?)' + glossary_item_code[2]
#     # print(search_text)

#     replace_text = lambda  x:'<dt class="glossary" id="' + slugify(glossterm) + '">' + glossterm_orig + '</dt>\n<dd>' + x.group(1).strip('––|–') + '<a epub:type="backlink" href="' + fname + '#' + slugify(glossterm)+'">↩</a></dd>'

#     ### Run regex to subsititute
#     glossdata = re.sub(search_text, replace_text, glossdata)

#     # delete M-dash
#     search_text = "<dd>—"
#     replace_text ="<dd>"
#      ### Run regex to subsititute
#     glossdata = re.sub(search_text, replace_text, glossdata)
    
# with open(glossary, 'w') as output:
#     output.write(glossdata)
#     output.close()

# Open glossary.xhtml and read
with open(glossary, 'r') as text:
    glossdata = text.read()

# Loop through stored terms and write chapter links from linklist to glossary.xhtml
for glossterms in linklist:
    glossterm = glossterms[0]
    fname=os.path.split(glossterms[1])[1]

    term_id = slugify(glossterm)
    linkpath = fname

    # Escape glossterm to find terms in parentheses
    glossterm_orig = glossterm
    glossterm = re.escape(glossterm)

    search_text = glossary_item_code[0] + glossterm  + '—*' + glossary_item_code[1] + '(.*?)' + glossary_item_code[2]

    replace_text = lambda  x:'<dt class="glossary" id="' + term_id + '">' + glossterm_orig + '</dt>\n<dd>' + x.group(1).strip('––|–|—') + '<a epub:type="backlink" href="' + fname + '#' + term_id + '">↩</a></dd>'

    ### Run regex to subsititute
    glossdata = re.sub(search_text, replace_text, glossdata)

    # delete M-dash
    search_text = "<dd>—"
    replace_text ="<dd>"
     ### Run regex to subsititute
    glossdata = re.sub(search_text, replace_text, glossdata)
    
    # Load the glossary using soup and add <dl> and </dl>
    soup = BeautifulSoup(glossdata, 'html.parser')

    # Find the first <dt> element
    first_dt = soup.find('dt')

    # Insert the <dl> element before the first <dt> element
    dl = soup.new_tag('dl')
    first_dt.insert_before(dl)

    # Move all subsequent <dt> and <dd> elements inside the <dl> element
    for element in soup.find_all(['dt', 'dd']):
        dl.append(element.extract())

# Save the modified page
with open(glossary, 'w') as f:
    f.write(str(soup))

### function to recompress and rename epub
clean_and_close(Exportfolder,newFileEnding)