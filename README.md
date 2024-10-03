# epub python scripts
 A series of scripts to facilitate epub creation from InDesign. I am *slowly* cleaning up the scripts to make them fit (mostly) for public use if anyone want to incorporate them into their workflow.
 
**NOTE** These scripts are here primarily as an example fo the sorts of things you can do with epub production and python. They may not work the way you expect them to but hopefully you can use them as an example that will work for your workflow.

***WARNING* I am *not* a programmer. I am sure that these scripts are filled with bad practices and even worse error checking.**

## Usage
Right now I have the script folder open in [Visual Studio Code](https://code.visualstudio.com/) and then run the  appropriate script from its python interface and then either drag the file into the terminal window or copy and paste the file path into the prompt.

*NOTE* to get the complete file path on a mac just right click on the file and hold down the option key. `Copy` will change to `Copy "filename" as Pathname`

*NOTE* The python files start with something like:
```
epubFile = None
# epubFile = "/Volumes/test files/Working/test.epub"
```
The line commented out beginning `# epubFile =` is there so I can rerun the script over and over again when debugging. Just uncomment it and add the path of your test file.

## Libraries
These are the python libraries used in the scripts so far: 
- os, re, zipfile, datetime, titlecase, pathlib 
- shutil (clean up folders)

I *believe* they are all part of the default python install.

Additionally to use the extract_alttext scripts you need:
- lxml (seach for title)
- bs4 (parse xml files using BeautifulSoup)
- xlsxwriter (write to xlsx files)

## Clean Indesign
The scripts consist of three parts.
1. epub_functions: this holds all the function to open, close, and run search and replaces
2. list_clean_indesign.py: This hold all the regexes for items I want to replace
3. Run_clean_indesign.py: this holds all the loops and executes the process

### The Process
(For a simple fiction title)

#### InDesign File
- Run Laura Brady's fabulous pagestaker script. (You can get this on her site [https://laurabrady.ca/blog/building-a-page-list](https://laurabrady.ca/blog/building-a-page-list)).  
**NOTE:** I currently don't use InDesign's new page list options since it necessitates that pages don't shift and I find that when remediating old books there is almost always page shifting.
- Anchor any images to the text and add styles (see next point)
- Go through and assign standardized export styles (this is important as the scripts makes certain choices based on style names). My list can be found in teh excel file: Indesign export styles.xlsx
- Double check all `<i>` vs `<em>`, `<b>` vs `<strong>` etc.
- Make a table of contents style
- **Remember** before exporting to make 'stakedPageNumbers' visible in the *Conditional Text* palette so the page numbers are exported. I can't tell you how many times I forget to do this...

##### Export as reflowable epub
- Add the cover
- set Multilevel toc to your style
- Text: Check "Remove Forced Line Breaks"
- HTML and CSS: uncheck "Preserve Local Overrides"

### Epub
- right-click the epub (on a Mac) and hold the option key down to get path
- run `Run_clean_indesign.py` and paste the path in at the prompt.
The script should create a new epub with *_rev* at the end of it having cleaned out all the crud that Indesign likes to add and prepped it according to my preferences. See list_clean_indesign.py for the specific search and replaces performed.

*NOTE* when the running the script multiple times it doesn't check to see if the resulting file already exists—it just overwrites it.

### Notes
- I put the word BREAK in all caps in the InDesign file where context breaks (editorial breaks) occur and the script replaces them with `<hr class="break"/>`'s
- The figure replacement isn't 100% because InDesign makes some funky choices based on where you anchor the image to the caption text. I am always playing with it and generally have to run another regex in the final cleanup to position the `<figcaption>` correctly within the `<figure>`

## Alt Text
### Extract alt text
The script `Run_alttext_extract_with_caption.py` is set up to use `<figure> `and `<figcaption>` but will generally work with `div`s and `img`. Without figcaptions it obviously does not extract captions.

If there is no alt text present it outputs 'PRESENTATION' in the alt text field. This is because in my import alt text script (coming soon) if the string PRESENTATION is in the alt text field then it writes `alt="" role="presentation"` into the `<img>`.

The script produces a xlsx file in the same folder as the original file and named using the dc:title element.

### Update Alt text
Run_alttext_update.py opens with two input requests. First the epub file and second the xlsx file in the format produced by `Run_alttext_extract_with_caption.py`. It should loop though and replace alt text with new alt text and indicate if it didn't find an image. If you enter PRESENTATION in the alt text field it will set it to `role="presentation"` and leave the alt text blank.

The scripts are run the same way as clean_indesign.

## The Process Continued
### Initial Clean Up
After I have cleaned the file up via the script I open it in Sigil ([https://sigil-ebook.com/](https://sigil-ebook.com/)) to do another quick edit.
1. go through and add split file markers then spilt the files
2. rename the files according to a standard template (so you can autoomate the next section)
3. Fix any oddities with the heads (`<h1>`'s etc.) so they are at the appropriate position
3. run (from here: [https://www.mobileread.com/forums/showthread.php?t=265237](https://www.mobileread.com/forums/showthread.php?t=265237)) the PageList plugin to build the page list
4. save the file

## Run Clean Scripts
***NOTE:** I am still working on cleaning up the 'clean' scripst for wider consumption so some of the code is specific to producing an [https://www.orcabook.com/](Orca) book. I haven't had time to test it without any Orca formatting.* 

At this point I close the file and run `Run_clean_fiction.py` or `Run_clean_nonfiction.py` that goes through and reformats the files according to my standards using the following file names pulling the changes from `/lists/list_clean_epub_fiction.py` or `lists/list_clean_epub_nonfiction.py`
- cover.xhtml
- halftitle.xhtml
- digitalrights.xhtml
- titlepage.xhtml
- copyright.xhtml
- dedication.xhtml
- opening.xhtml
- series.xhtml
- contents.xhtml
- prologue.xhtml
- introduction.xhtml
- chapter-01.xhtml, chapter-02.xhtml etc.
- epilogue.xhtml
- glossary.xhtml
- resources.xhtml
- index.xhtml
- acknowledgments.xhtml
- authors-note.xhtml
- endnotes.xhtml
- about-the-author.xhtml
- morebooks.xhtml
- excerpt.xhtml

This script tosses the exported css and replaces it with my own standard css and modify it from there rather than deal with InDesign's overly verbose and complex css choices.

It produces an epub with proper structure and aria-roles based on the filenames as well as adds in a digital rights page. Making it completely accessible is then just a matter of fixing a few items and updating the .opf file.

**NOTE** The function `clean_and_close` contains the command `os.system("se clean .")`. This invokes a tool from [Standard Ebooks](https://standardebooks.org/contribute)' toolset that cleans up the code. You can disable it in favour of using Sigil's *Mend and Prettify all HTML Files* if you want. Just add `clean_and_close(Exportfolder, skip_check=True)`. It might affect some of the regexes that are based on  the order of ids and classes though/

And if you want to contribute to creating well-formed public domain ebooks, I encourage you to volunteer for Standard Ebooks. I guarantee you will learn some things.

### Final clean up
Then it's just a matter of going through the epub and double checking everything. For a simple fiction book this usually takes minutes, for a complex non-fiction it might take half a day or so because I need to rebuild the css and format all the sections like the index and glossary...

## Other scripts
### Run_glossary_links.py
If the files are set up right, this script will loop though all the terms in your glossary and search the text for the glossed words (usually indicated by `<span class="glossary-term">`) creating links and backlinks for them.

It rarely works on the first pass but if you run it once then double check for the terms that fail you can usually get it perfect by the third try. The issue is often just plurals or malformed spans.

### Run_update_png_to_jpg.py
I find InDesign often chooses to export files as pngs rather than jpgs and in a non-fiction book this can balloon the file size considerably. 

In that case I crack open the epub and use Bridge/Photoshop to convert a bunch of them to jpgs. This script grabs the new folder of jpgs and swaps out the pngs with the same file name.

### Run_increment_aside-ID.py
This one is still a work in progress, but it works pretty good if you set up you exports correctly. Non-fiction books often have a lot of asides and those aside all need a unique `aria-label` or `aria-labelledby`. This script should go though them based on their class and number them:

```
<aside aria-labelledby="people-XXX" class="people">
  <h2 class="people" id="people-XXX">
```
becomes:

```
<aside aria-labelledby="people-1" class="people">
  <h2 class="people" id="people-1">
```

Or if the header is not unique:

```
<aside aria-label="Facts XXX" class="facts">
  <h2 class="facts">Fast Facts</h2>
```
becomes:
```
<aside aria-label="Facts 1" class="facts">
  <h2 class="facts">Fast Facts</h2>
```

## Final Point
I maintain a local website based on markdown notes and the fantastic [mkdocs](https://www.mkdocs.org/) in a docker container that has ALL my defaults in it so I can cut and paste code as necessary. I **strongly** urge you to do something similar as well because consistency is key to ensure this kind of workflow be successful.

![Screenshot of markdown-based website](/images/notescreenshot.png)