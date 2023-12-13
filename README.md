# epub python scripts
 A series of scripts to facilitate epub creation from InDesign. I am *slowly* cleaning up the scripts to make them fit (mostly) for public use if anyone want to incorporate them into their workflow.
 
**NOTE** These scripts are here primarily as an example fo the sorts of things you can do with epub production and python. They may not work the way you expect them to but hopefully you can use them as an example that will work for your workflow.

 This first part simply deals with cleaning up the InDesign file.

***WARNING* I am *not* a programmer. I am sure that these scripts are filled with bad practices and even worse error checking.**

## Usage
Right now I have the script folder open in [Visual Studio Code](https://code.visualstudio.com/) and then run the  appropriate script from its python interface and then copy and paste the file path into the prompt.

*NOTE* to get the complete file path on a mac just right click on the file and hold down the option key. `Copy` will change to `Copy "filename" as Pathname`

## Structure
The scripts consist of three parts.
1. epub_functions: this holds all the function to open, close, and run search and replaces
2. list_clean_indesign.py: This hold all the regexes that I want to replace
3. Run_clean_indesign.py: this holds all the loops and executes the process

## The Process
(For a simple fiction title)
### InDesign File
- Run Laura Brady's fabulous pagestaker script. (You can get this by contacting her via [https://epubsecrets.com/why-i-use-page-list-and-how.php](https://epubsecrets.com/why-i-use-page-list-and-how.php)).
- Export any graphics or type as graphics i.e. the titlepage block.
- Anchor any images to the text and add styes (see next point)
- Go through and assign standardized export styles (this is important as the scripts makes certain choices based on style names)
- Double check all `<i>` vs `<em>`, `<b>` vs `<strong>` etc.
- Make a table of contents style
- **Remember** before exporting to make 'stakedPageNumbers' visible in the Conditional Text palette so the page numbers are exported. I can't tell you how many times I forget to do this...

#### Export as reflowable epub
- Add the cover
- set Multilevel toc to your style
- Text: Check "Remove Forced Line Breaks"
- HTML andCSS: un check "Preserve Local Overrides"

### Epub
- rightclick the epub (on a Mac) and hold the option key down to get path
- run `Run_clean_indesign.py` and paste the path in at the prompt.
The script should create a new epub with *_rev* at the end of it having cleaned out all the crud that Indesign likes to add and prepped it according to my preferences. See list_clean_indesign.py for the specific search and replaces performed.

## Libraries
These are the python libraries used in the scripts so far: os, re, zipfile. I *believe* they are all part of the default python install.

## Notes
- I put the word BREAK in the InDesign file where context breaks (editorial breaks) occur and the script replaces them with `<hr/>`'s
- The figure replacement isn't 100% because InDesign makes some funky choices based on where you anchor the image to the caption text. I am always playing with it.

## The Process Continued
### Initial Clean Up
After I have cleaned the file up via the script I open it in Sigil ([https://sigil-ebook.com/](https://sigil-ebook.com/)) to do another quick edit.
1. go through and add split file markers then spilt the files
2. rename the files according to a standard template (so you can autoomate the next section)
3. Fix any oddities with the heads (`<h1>`'s etc.) so they are at the appropriate position
3. run (from here: [https://laurabrady.ca/blog/building-a-page-list](https://laurabrady.ca/blog/building-a-page-list)) the PageList plugin to build the page list
4. save the file

### Run Clean Script
*NOTE: I am still working on cleaning up the 'clean' script for wider consumption so that is still to come.*

At this point I close the file and run the second script that goes through and reformats the files according to my standards using the file names and style names.

I generally toss the css and replace it with my own standard css and modify it from there rather than deal with InDesign's overly verbose and complex css choices.

It produces an epub with proper structure and aria-roles based on the filenames as well as adds in a digital rights page. Making it completely accessibe is then just a matter of fixing a few items and updateing the .opf file

**NOTE** Line 70 in Run_clean_indesign is `os.system("se clean .")`. This invokes a tool from [Standard Ebooks](https://standardebooks.org/contribute)' toolset that cleans up the code. I am planning on replacing it with something more common becasue it has a bad habit of lowercasing css which is fine for me but can cause problems if that isn't part of your standard workflow. And if you want to contribute to creating well-formed public domain ebooks, I encourage you to volunteer. I guarantee you will learn some things.

## Final Point
I maintain a local website based on markdown notes and the fantastic mkdocs docker that has ALL my defaults in it so I can cut and paste code as necessary. I *strongly* urge you to do so as well because consistency is key to making this kind of workflow be successful.

![Screenshot of markdown-based website](/images/notescreenshot.png)