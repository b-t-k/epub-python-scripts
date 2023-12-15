# epub python scripts
 A series of scripts to facilitate epub creation from InDesign. I am *slowly* cleaning up the scripts to make them fit (mostly) for public use if anyone want to incorporate them into their workflow.
 
**NOTE** These scripts are here primarily as an example fo the sorts of things you can do with epub production and python. They may not work the way you expect them to but hopefully you can use them as an example that will work for your workflow.

 This first part simply deals with cleaning up the InDesign file.

***WARNING* I am *not* a programmer. I am sure that these scripts are filled with bad practices and even worse error checking.**

## Usage
Right now I have the script folder open in [Visual Studio Code](https://code.visualstudio.com/) and then run the  appropriate script from its python interface and then copy and paste the file path into the prompt.

*NOTE* to get the complete file path on a mac just right click on the file and hold down the option key. `Copy` will change to `Copy "filename" as Pathname`

## Clean Indesign
The scripts consist of three parts.
1. epub_functions: this holds all the function to open, close, and run search and replaces
2. list_clean_indesign.py: This hold all the regexes that I want to replace
3. Run_clean_indesign.py: this holds all the loops and executes the process

### The Process
(For a simple fiction title)
#### InDesign File
- Run Laura Brady's fabulous pagestaker script. (You can get this on her site [https://laurabrady.ca/blog/building-a-page-list](https://laurabrady.ca/blog/building-a-page-list)).
- Export any graphics or type as graphics i.e. the titlepage block.
- Anchor any images to the text and add styes (see next point)
- Go through and assign standardized export styles (this is important as the scripts makes certain choices based on style names)
- Double check all `<i>` vs `<em>`, `<b>` vs `<strong>` etc.
- Make a table of contents style
- **Remember** before exporting to make 'stakedPageNumbers' visible in the Conditional Text palette so the page numbers are exported. I can't tell you how many times I forget to do this...

##### Export as reflowable epub
- Add the cover
- set Multilevel toc to your style
- Text: Check "Remove Forced Line Breaks"
- HTML andCSS: un check "Preserve Local Overrides"

### Epub
- rightclick the epub (on a Mac) and hold the option key down to get path
- run `Run_clean_indesign.py` and paste the path in at the prompt.
The script should create a new epub with *_rev* at the end of it having cleaned out all the crud that Indesign likes to add and prepped it according to my preferences. See list_clean_indesign.py for the specific search and replaces performed.

### Notes
- I put the word BREAK in the InDesign file where context breaks (editorial breaks) occur and the script replaces them with `<hr/>`'s
- The figure replacement isn't 100% because InDesign makes some funky choices based on where you anchor the image to the caption text. I am always playing with it.

## Extract alt text
I have two scripts for this purpose. Since I use `<figure> `and `<figcaption>` exclusively the first (Run_extract_alttext_with_caption.py) searches for figure and extracts the alt text and accompanying caption. Occasionally when working on others' files they don't use `<figure`s so I rewrote it slightly to search for the `<img>` tag and use that (Run_extract_altext)—it obviously does not extract captions.

If there is no alt text present it outputs 'PRESENTATION' in the alt text field. This is because in my import alt text script (coming soon) if the string PRESENTATION is in the alt text field then it writes `alt="" role="presentation"` into the `<img>`.

The script produces a xlsl file in the same folder as the original file and named using the dc:title element.

The scripts are run the same way as clean_indesign.

## Libraries
These are the python libraries used in the scripts so far: 
- os, re, zipfile 
- shutil (clean up folders)

I *believe* they are all part of the default python install.

Additionally to use the extract_alttext scripts you need:
- lxml (seach for title)
- bs4 (parse xml files using BeautifulSoup)
- xlsxwriter (write to xlsx files)

## The Process Continued
### Initial Clean Up
After I have cleaned the file up via the script I open it in Sigil ([https://sigil-ebook.com/](https://sigil-ebook.com/)) to do another quick edit.
1. go through and add split file markers then spilt the files
2. rename the files according to a standard template (so you can autoomate the next section)
3. Fix any oddities with the heads (`<h1>`'s etc.) so they are at the appropriate position
3. run (from here: [https://www.mobileread.com/forums/showthread.php?t=265237](https://www.mobileread.com/forums/showthread.php?t=265237)) the PageList plugin to build the page list
4. save the file

### Run Clean Script
*NOTE: I am still working on cleaning up the 'clean' script for wider consumption so that is still to come.*

At this point I close the file and run a second script that goes through and reformats the files according to my standards using the file names and style names.

I generally toss the css and replace it with my own standard css and modify it from there rather than deal with InDesign's overly verbose and complex css choices.

It produces an epub with proper structure and aria-roles based on the filenames as well as adds in a digital rights page. Making it completely accessibe is then just a matter of fixing a few items and updateing the .opf file

**NOTE** Line 70 in Run_clean_indesign is `os.system("se clean .")`. This invokes a tool from [Standard Ebooks](https://standardebooks.org/contribute)' toolset that cleans up the code. I am planning on replacing it with something more common becasue it has a bad habit of lowercasing css which is fine for me but can cause problems if that isn't part of your standard workflow. And if you want to contribute to creating well-formed public domain ebooks, I encourage you to volunteer. I guarantee you will learn some things.

## Final Point
I maintain a local website based on markdown notes and the fantastic [mkdocs](https://www.mkdocs.org/) in a docker container that has ALL my defaults in it so I can cut and paste code as necessary. I *strongly* urge you to do something similar as well because consistency is key to making this kind of workflow be successful.

![Screenshot of markdown-based website](/images/notescreenshot.png)