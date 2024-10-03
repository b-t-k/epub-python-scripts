## Clean InDesign epub Export Files
## Version 1.2

from titlecase import titlecase


# List of simple deletions or replacements
list_delete=[
    # convert  div class="aside" to aside and delete remainig divs except pagebreaks
    
    ['<div class="aside">(.*?)</div>',lambda x:'<aside class="aside">' + x.group(0) + '</aside>'],
    # ['<div( .*?)?>|</div>',''],
    
      ## remove extra tabs and line breaks from divs with page number (only using indesigns page navigation)
    ['(<div id="page\d+" role="doc-pagebreak" aria-label="\d+" epub:type="pagebreak")>(\n+\t+)</div>',lambda x: x.group(1) + "/>"],

    ## Delete divs that don't have page numbers in them
    ['<(div)(?! (epub:type="pagebreak"|id="page\d+"))[^>]*>|</(div)(?! (epub:type="pagebreak"|id="page\d+"))[^>]*>',''],

    ## delete cruft
    ['_idGenParaOverride-\d+| id="_idContainer\d+"| class="_idGenObjectAttribute-\d+"|_idGenCharOverride-\d+|_idGenObjectStyle-Disabled\s?| CharOverride-\d+|style=".*?"|_idGenObjectLayout-\d+|ParaOverride-\d+',''],

    # # delete languages  in xx-xx format
    ['xml:lang="\w+-\w+"|lang="\w+-\w+"',''],

    # clean up classes
    ['class="Basic-Paragraph\s?"',''],
    ['class="body-text\s*"|class="body\s*"',''],

    # clean up styling
    ['<i class="italic[s]?\s?"\s*(?=>)>','<i>'],
    ['<em class="emphasis\s?"\s*(?=>)>','<em>'],
    ['<b class="bold\s?"\s*(?=>)>','<b>'],
    ['<strong class="strong\s?"\s*(?=>)>','<strong>'],
    ['<small class="smallcaps\s*">','<small>'],

    # clean weird u grep style in echoes
    ['<span class="u-grep-style">u</span>','u'],
    ['<span class="longer-em-dash">—</span>','—'],

    # transform page breaks
    ['<p(?:\s)?(?:class=".*?")?>PAGEBREAK</p>','<hr/>'],
    ['<p(?:\s)?(?:class=".*?"\s*)?>\s*BREAK</p>','<hr class="break"/>'],
    #edge case where there are empty spans
    ['<p(?:\s)?(?:class=".*?"\s*)?><span>BREAK</span></p>','<hr class="break"/>'],

    # rename files
    ['toc.xhtml','nav.xhtml'],
    ['idGeneratedStyles.css','styles.css'],

# ]


# # #list of regex replacements
# list_replace=[

     # stray copyright spans
    ['<span \s*class="Minion-Pro-lining-numerals_Minion-Pro-All-Caps---85-"\s*>(.*?)</span>',lambda  x: x.group(1)],

    # strong with italics
    ['<span \s*class="strong-italics\s*"\s*>(.*?)</span>',lambda  x:'<i><strong>' + x.group(1) + '</strong></i>'],

    # strong with bold
    ['<span \s*class="strong-bold\s*"\s*>(.*?)</span>',lambda  x:'<b><strong>' + x.group(1) + '</strong></b>'],

    # # italics with strong
    ['<span \s*class="italics-strong\s*"\s*>(.*?)</span>',lambda  x:'<i><strong>' + x.group(1) + '</strong></i>'],

   # # italics with upper
    ['<span \s*class="upper-italics\s*"\s*>(.*?)</span>',lambda  x:'<i><span class="upper">' + x.group(1) + '</span></i>'],

   # # bold with upper
    ['<span \s*class="upper-bold\s*"\s*>(.*?)</span>',lambda  x:'<b><span class="upper">' + x.group(1) + '</span></b>'],

    ## special circumstances
    # em in italics
    ['</i> <em>(.*?)</em> <i>',lambda  x:' <em>' + x.group(1) + '</em> '],


   #clean up redundant styles
    ['</i>\s<i>',' '],
    ['</i><i>',''],
    ['</em>\s<em>',' '],
    ['</em><em>',''],

    # replace rorohiko pagestaker spans
    ['<span class="com-rorohiko-pagestaker-style.*?>','<span class="com-rorohiko-pagestaker-style">'],
    ['<span class=("com-rorohiko-pagestaker-style")>(\d+|[iv]{1,})</span>',lambda  x:"<span epub:type=\"pagebreak\" role=\"doc-pagebreak\" id=\"page" + x.group(2) + "\" aria-label=\" page " + x.group(2) + ". \"/>"],
    ['<span class="com-rorohiko-pagestaker-style"><a id=(.*?)</span>', lambda x:'<a id=' + x.group(1)],
    ['<span class="com-rorohiko-pagestaker-style">\s*</span>',''],

    # transform languages
    ['class="lang-(.*?)"',lambda  x:'xml:lang="' + x.group(1)+'"'],
    ['class="lang:(.*?)"',lambda  x:'xml:lang="' + x.group(1)+'"'],
    ['class="xml:(.*?)"',lambda  x:'xml:lang="' + x.group(1)+'"'],

    ## DEAL WITH FIGURES
    #remove excess roles
    [' role="presentation"',''],

    #replace img with figure if no figure and therefore follows </p> or <img ... /> 
     ['(?:(?<=<\/p>)|(?<=\/>))[\n\t+]+<img (?:class=".*?"\s)?src="(.*?)" alt=""\s*/>',lambda x:'\n<figure class="full">\n\t<img class="float" src="' + x.group(1) + '" alt="ALT_TEXT_HERE" />\n</figure>'],

    #replace img 
     ['\t+<img src="(.*?)" alt="" />',lambda x:'\n\t<img class="float" src="' + x.group(1) + '" alt="ALT_TEXT_HERE" />\n'],

    # move photo-credit (figcaption) into figcaption (photo-caption)
     ['<figcaption class="photo-caption".*?>(.*?)</figcaption>[\t\n\r\s]*<figcaption class="photo-credit".*?>(.*?)</figcaption>',lambda x: '<figcaption class="photo-caption">' + x.group(1) + ' <span class="photo-credit">' + x.group(2) + '</span></figcaption>'],
    
     # move photo-credit (span) into figcaption (photo-caption)
     ['<figcaption class="photo-caption".*?>(.*?)</figcaption>[\t\n\r\s]*<span class="photo-credit".*?>(.*?)</span>',lambda x: '<figcaption class="photo-caption">' + x.group(1) + ' <span class="photo-credit">' + x.group(2) + '</span></figcaption>'],

     # move photo credit (figcaption)above into figure TEST
     ['<figcaption class="photo-caption".*?>(.*?)</figcaption>[\t\n\r\s]*<figure\s?class="(.*?)"\s?>[\t\n\r\s]*<img (.*?)/>',lambda x: '<figure class="' + x.group(2) + '">\n\t<img ' + x.group(3) + '/>\n\t<figcaption class="photo-caption">' + x.group(1) + '</figcaption>'],

    # move figcaption (below) into figure
     ['</figure>[\t\n\r\s]*<figcaption class="(.*?)".*?>(.*?)</figcaption>',lambda x: '\n\t<figcaption class="' + x.group(1) + '">' + x.group(2) + '</figcaption>\n</figure>'],

    # RERUN move photo-credit (figcaption) into figcaption (photo-caption)
     ['<figcaption class="photo-caption".*?>(.*?)</figcaption>[\t\n\r]*<figcaption class="photo-credit".*?>(.*?)</figcaption>',lambda x: '<figcaption class="photo-caption">' + x.group(1) + ' <span class="photo-credit">' + x.group(2) + '</span></figcaption>'],
    
     # RERUN move photo-credit (span) into figcaption (photo-caption)
     ['<figcaption class="photo-caption".*?>(.*?)</figcaption>[\t\n\r]*<span class="photo-credit".*?>(.*?)</span>',lambda x: '<figcaption class="photo-caption">' + x.group(1) + ' <span class="photo-credit">' + x.group(2) + '</span></figcaption>'],


    # move photocredits with no caption into spans
    ['<figcaption class="photo-credit">(.*?)</figcaption>',lambda x: '<figcaption><span class="photo-credit">' + x.group(1)+ '</span></figcaption>'],


     # regex to find / in string and add thin spaces before and after (run twice)
    ['(<span class="photo-credit\s*">)(.*?)(\s*/\s*)(.*?)(</span>)',lambda x: x.group(1)+x.group(2)+" / "+x.group(4)+x.group(5)],
     
    # the old version with lookbehinds and a space in the class because the above one won't catch second instances
    ['(?<=<span class="photo-credit ">)(.*?[^ ][^<br/>])/([^ ].*?)(?=</span>)',lambda x: x.group(1)+ " / " + x.group(2)],

    # clean up extra spaces in <br/> and </a>
    ['<br  / >','<br/>'],
    ['< / a>','</a>'],



    ['(?s)<span lang="en-\w+" xml:lang="en-\w+">(.*?)</span>',lambda  x:x.group(1)],

    # Delete empty spans
    ['<span\s+>(.*?)</span>', lambda x: x.group(1)],

     # move space from inside span to outside (nor necessary anymore?)
    # ['<span(.*?)>(.*?)\s</span>', lambda x: '<span' + x.group(1) + '>' + x.group(2) + '</span> '],
 
     # move space to outside tag
    ['\s</(.*?)>', lambda x: '</' + x.group(1) + '> '],

    #standardize aside class and aria label
    ['<aside class="(.*?)">', lambda x: '<aside class="' + x.group(1) + '" aria-labelledby="Sidebar_ID-XXX">'],

    # experiment with title case of strong and upper
    ['<strong\s*>(.*?)</strong>',lambda x: '<strong>' + titlecase(x.group(1)) + '</strong>'],
    ['<span class="upper"\s*>(.*?)</span>',lambda x: '<span class="upper">' + titlecase(x.group(1)) + '</span>'],

]


opf_file=[

    ['id="toc" href="toc.xhtml"','id="nav" href="nav.xhtml"'],
    ['<item id="idGeneratedStyles.css" href="css/idGeneratedStyles.css" media-type="text/css"\s?/>','<item id="styles.css" href="css/styles.css" media-type="text/css" />'],

    # add digital rights to manifest
    # ['<item (.*?) href="(.*?)cover.xhtml"(.*?)\/>',lambda x:'<item ' + x.group(1) + ' href="' + x.group(2) + 'cover.xhtml"' + x.group(3) + '/>\n<item href="' + x.group(2) + 'digitalrights.xhtml" id="digitalrights" media-type="application/xhtml+xml"/>'],
    # ['<itemref idref="cover".*?/>','<itemref idref="cover"/>\n<itemref idref="digitalrights"/>'],
]