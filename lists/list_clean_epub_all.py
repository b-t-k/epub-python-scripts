## Clean epub-Fiction Files

from titlecase import titlecase

# List of simple deletions or replacements
list_delete=[
    ## replace all sections to generic chapter (the rest will be fixed  by filename)
    ['<\?xml.*?>\n<!.*?>','<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>'],
    ['<html .*?>','<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en-US" xml:lang="en-US">'],
    ['<title>.*?</title>','<title>Chapter XXX</title>'],
    ['<body?.*?>','<body epub:type="bodymatter">\n<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">'],
    ['</body>','</section>\n</body>'],
    ['<div class="(chapter|copyright|coverpage|titlepage|box|box.*?)">',''],

    # fix for new indesign divs at end of chapter
     ['<div epub:type="pagebreak" (.*?)"></div>\n</section>',lambda x: '<div epub:type="pagebreak" ' + x.group(1) + '"/>\n</section>'],
    ['</div>\n</section>','</section>'],
    
    # fix odd spans around u's in hi-lo books
    ['</b><b>u</b><b>','u'],
    ['</i><i>u</i><i>','u'],
    ['</em><em>u</em><em>','u'],
    ['<span class="U">u</span>','u'],

    # get rid of redundant tags
    ['</i><i>|</b><b>|</em><em>',''],
    ['</i> <i>|</b> <b>|</em> <em>',' '],
]

#list of regex replacements
list_replace=[

    # test fix asides to prep for numbering
    ['<aside class="(.*?)" aria-labelledby="Sidebar_ID-XXX">\n*\t*\s*<h2 ',lambda x: '<aside class="' + x.group(1) + '" aria-labelledby="' + x.group(1) + '-XXX">\n\t\t<h2 id="' + x.group(1) + '-XXX" '],

    ['<aside class="(.*?)" aria-labelledby="Sidebar_ID-XXX">\n*\t*\s*<p',lambda x: '<aside class="' + x.group(1) + '" aria-label="' + x.group(1) + ' XXX">\n\t\t<p'],


    # move space from inside span to outside
    ['<span(.*?)>(.*?)\s</span>', lambda x: '<span' + x.group(1) + '>' + x.group(2) + '</span> '],
    ['(<span[^>]*>)\s+', lambda x: ' ' + x.group(1)],

    # move space from inside em to outside
    ['<em>(.*?)\s</em>', lambda x: '<em>' + x.group(1) + '</em> '],
    ['<em>\s+', ' <em>'],

    # move space from inside i to outside
    ['<i>(.*?)\s</i>', lambda x: '<i>' + x.group(1) + '</i> '],
    ['<i>\s+', ' <i>'],


### Fiction heads
### Tries to cover all cases and combinations of title, page markers  and heads etc.
    # rebuilt standard: chapter-page-title
    ['<title>Chapter XXX</title>[\s\t\n\r]*<link href="(.*?)"/>[\s\t\n\r]*</head>[\s\t\n\r]*<body epub:type="bodymatter">[\s\t\n\r]*<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">[\s\t\n\r]*<h1 class="chapter-title" id="(.*?)"><span epub:type="(.*?)"></span>\s*Chapter (.*?)</h1>',

    lambda x: '<title>Chapter ' + titlecase(x.group(4)) + '</title>\n\t<link href="' + x.group(1) + '"/>\n</head>\n<body epub:type="bodymatter">\n<section epub:type="chapter" role="doc-chapter" aria-labelledby="' + x.group(2) + '">\n\t<h1 class="chapter-title" id="' + x.group(2) + '"><span epub:type="' + x.group(3) + '"/>Chapter ' + titlecase(x.group(4)) + '</h1>'],

    # rebuilt standard: chapter-page-title
    ['<title>Chapter XXX</title>[\s\t\n\r]*<link href="(.*?)"/>[\s\t\n\r]*</head>[\s\t\n\r]*<body epub:type="bodymatter">[\s\t\n\r]*<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">[\s\t\n\r]*<h1 id="(.*?)" class="chapter-title"><span epub:type="(.*?)"></span>\s*Chapter (.*?)</h1>',

    lambda x: '<title>Chapter ' + titlecase(x.group(4)) + '</title>\n\t<link href="' + x.group(1) + '"/>\n</head>\n<body epub:type="bodymatter">\n<section epub:type="chapter" role="doc-chapter" aria-labelledby="' + x.group(2) + '">\n\t<h1 class="chapter-title" id="' + x.group(2) + '"><span epub:type="' + x.group(3) + '"/>Chapter ' + titlecase(x.group(4)) + '</h1>'],

    # when no-indent is before chapter
    ['<title>Chapter XXX</title>[\s\t\n\r]*<link href="(.*?)"/>[\s\t\n\r]*</head>[\s\t\n\r]*<body epub:type="bodymatter">[\s\t\n\r]*<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">[\s\t\n\r]*<p class="no-indent">(.*?)</p>[\s\t\n\r]*<h1 class="chapter-title" id="(.*?)">Chapter (.*?)</h1>',

    lambda x: '<title>Chapter ' + titlecase(x.group(4)) + '</title>\n\t<link href="' + x.group(1) + '"/>\n</head>\n<body epub:type="bodymatter">\n<section epub:type="chapter" role="doc-chapter" aria-labelledby="' + x.group(3) + '">\n\t<h1 class="chapter-title" id="' + x.group(3) + '">Chapter ' + titlecase(x.group(4)) + '</h1>\n\t<p class="no-indent">' + x.group(2) + '</p>'],


    # when page number is in first paragraph
    # includes optional order for id and class
    
    # The search pattern (no named groups for id)
    ['<title>Chapter XXX</title>[\s\t\n\r]*<link href="(.*?)"/>[\s\t\n\r]*</head>[\s\t\n\r]*<body epub:type="bodymatter">[\s\t\n\r]*<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">[\s\t\n\r]*<h1 (?:id="(.*?)" class="chapter-title"|class="chapter-title" id="(.*?)")>Chapter (.*?)</h1>',

    lambda x: ('<title>Chapter ' + titlecase(x.group(4)) + '</title>\n\t'
    '<link href="' + x.group(1) + '"/>\n</head>\n<body epub:type="bodymatter">\n'
    '<section epub:type="chapter" role="doc-chapter" aria-labelledby="' + (x.group(2) or x.group(3)) + '">\n\t'
    '<h1 class="chapter-title" id="' + (x.group(2) or x.group(3)) + '">Chapter ' + titlecase(x.group(4)) + '</h1>')],

    # when its been cleaned and has a chapter title
    ['<title>Chapter XXX</title>[\s\t\n\r]*<link href="(.*?)"/>[\s\t\n\r]*</head>[\s\t\n\r]*<body epub:type="bodymatter">[\s\t\n\r]*<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">[\s\t\n\r]*<h1 id="(.*?)" class="chapter-num">Chapter (\w+)(.*?)</h1>',
    
    lambda x: '<title>Chapter ' + titlecase(x.group(3)) + '</title>\n\t<link href="' + x.group(1) + '"/>\n</head>\n<body epub:type="bodymatter">\n<section epub:type="chapter" role="doc-chapter" aria-labelledby="' + x.group(2) + '">\n\t<h1 class="chapter-title" id="' + x.group(2) + '">Chapter ' + titlecase(x.group(3)) + x.group(4) + '</h1>'],

#   ## Non-fiction: redo head
    ['<title>.*?</title>[\s\t\n\r]*<link href="(.*?)"/>[\s\t\n\r]*</head>[\s\t\n\r]*<body epub:type="bodymatter">[\s\t\n\r]*<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">[\s\t\n\r]*<h1 id="(.*?)" class="chapter-num">(.*?)<span epub:type="(.*?)"></span>(.*?)</h1>[\s\t\n\r]*<h1 id=".*?" class="chapter-title">(.*?)</h1>',
      
    lambda x: '<title>Chapter ' + x.group(5) + '</title>\n\t\t<link href="' + x.group(1) + '"/>\n\t</head>\n\t<body epub:type="bodymatter">\n\t\t<section aria-labelledby="' + x.group(2) + '" role="doc-chapter" epub:type="chapter">\n\t\t\t<h1 class="chapter-num" id="' + x.group(2) + '">' + x.group(3) + '<span epub:type="' + x.group(4) + '"></span>' + x.group(5) + '<span class="chapter-title">' + titlecase(x.group(6)) + '</span></h1>'],

    # if no page span in H1
    ['<title>Chapter XXX</title>[\s\t\n\r]*<link href="(.*?)"/>[\s\t\n\r]*</head>[\s\t\n\r]*<body epub:type="bodymatter">[\s\t\n\r]*<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">[\s\t\n\r]*<h1 class="chapter-num" id="(.*?)"><span aria-label="(.*?)"></span>(.*?)</h1>[\s\t\n\r]*<h1 class="chapter-num" id=".*?">[\s\t\n\r]*<span class="chapter-title">(.*?)</span>[\s\t\n\r]*</h1>',
      
    lambda x: '<title>Chapter ' + x.group(4) + '</title>\n\t\t<link href="' + x.group(1) + '"/>\n\t</head>\n\t<body epub:type="bodymatter">\n\t\t<section aria-labelledby="' + x.group(2) + '" role="doc-chapter" epub:type="chapter">\n\t\t\t<h1 class="chapter-num" id="' + x.group(2) + '"><span aria-label="' + x.group(3) + '"></span>' + x.group(4) + '<span class="chapter-title">' + titlecase(x.group(5)) + '</span></h1>'],

    # if no page span in H1
    ['<title>Chapter XXX</title>[\s\t\n\r]*<link href="(.*?)"/>[\s\t\n\r]*</head>[\s\t\n\r]*<body epub:type="bodymatter">[\s\t\n\r]*<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">[\s\t\n\r]*<h1 class="chapter-num" id="(.*?)">(.*?)</h1>[\s\t\n\r]*<h1 class="chapter-num" id=".*?">[\s\t\n\r]*<span class="chapter-title">(.*?)</span>[\s\t\n\r]*</h1>',
      
    lambda x: '<title>Chapter ' + x.group(3) + '</title>\n\t\t<link href="' + x.group(1) + '"/>\n\t</head>\n\t<body epub:type="bodymatter">\n\t\t<section aria-labelledby="' + x.group(2) + '" role="doc-chapter" epub:type="chapter">\n\t\t\t<h1 class="chapter-num" id="' + x.group(2) + '">' + x.group(3) + '<span class="chapter-title">' + titlecase(x.group(4)) + '</span></h1>'],

    ### when using page divs from InDesign
    ['<title>Chapter XXX</title>[\s\t\n\r]*<link href="(.*?)"/>[\s\t\n\r]*</head>[\s\t\n\r]*<body epub:type="bodymatter">[\s\t\n\r]*<section epub:type="chapter" role="doc-chapter" aria-labelledby="ID_XX">[\s\t\n\r]*<div id="page(\d+)" role="doc-pagebreak" aria-label="\d+" epub:type="pagebreak"></div>[\s\t\n\r]*<h1 id="(.*?)" class="chapter-title">Chapter (.*?)</h1>',

    lambda x: '<title>Chapter ' + titlecase(x.group(4)) + '</title>\n\t<link href="' + x.group(1) + '"/>\n</head>\n<body epub:type="bodymatter">\n<section epub:type="chapter" role="doc-chapter" aria-labelledby="' + x.group(3) + '">\n\t<div id="page' + titlecase(x.group(2)) + '" role="doc-pagebreak" aria-label="' + titlecase(x.group(2)) + '" epub:type="pagebreak"></div>\n\t<h1 class="chapter-title" id="' + x.group(3) + '">Chapter ' + titlecase(x.group(4)) + '</h1>'],
]

## Common opf changes for both fiction and non-fiction
opf_file1=[
    # add english to package
    ['<package .*? unique-identifier="(.*?)" .*?>','<package version="3.0" unique-identifier="bookid" prefix="schema: http://schema.org/ rendition: http://www.idpf.org/vocab/rendition/# ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0/" xmlns="http://www.idpf.org/2007/opf" xml:lang="en-US">'
    ],

    # Fix cover-image id
     ['<item id=".*?" href="(.*?)" media-type="image/jpeg"(?=\sproperties="cover-image")', lambda x: '<item id="cover-image" href="' + x.group(1) + '" media-type="image/jpeg"'],

    # Fix internal manifest links (for old epub2)
     ['(.*?)\.html', lambda x:  x.group(1) + '.xhtml'],

    # Add digital rights to manifest and spine
    ['<item (.*?) href="(.*?)cover.xhtml"(.*?)\/>',lambda x:'<item ' + x.group(1) + ' href="' + x.group(2) + 'cover.xhtml"' + x.group(3) + '/>\n<item href="' + x.group(2) + 'digitalrights.xhtml" id="digitalrights" media-type="application/xhtml+xml"/>'],
    ['<itemref idref="cover".*?/>','<itemref idref="cover"/>\n<itemref idref="digitalrights"/>'],
]

### Specific search and replaces based on file names
pages_list=[
    [['about-the-author.xhtml'],
     [['<title>.*?</title>','<title>About the Author</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="contributors" aria-label="About the Author" class="author">'],
     ['<meta charset="utf-8"/>',''],
     ['p class=".*?"','p class="no-indent"'],
     ['<figure class="author">[\n\r\t\s]*<img.*?src="(.*?)".*?/>',lambda x:'<figure class="author">\n<img class="author" src="' + x.group(1) + '" alt="A photo of the author, ADD_NAME_HERE" />\n'],
     ],
    ],
    [['acknowledgments.xhtml','acknowledgements.xhtml'],
     [['<title>.*?</title>','<title>Acknowledgements</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="acknowledgements" role="doc-acknowledgments" aria-labelledby="id_acknowledgements">'],
     ['<meta charset="utf-8"/>',''],
     ['class=".*?"','class="no-indent"'],
     ['<h1\s+(?:id="[^"]*"|class="[^"]*")*\s*class="([^"]*)"[^>]*>','<h1 class="chapter-title" id="id_acknowledgements">'],
     ],
    ],
    [['afterword.xhtml','afterword-\d+.xhtml'],
     [['<title>.*?</title>','<title>Appendix</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="afterword" role="doc-afterword" aria-labelledby="id_afterword">'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['appendix.xhtml'],
     [['<title>.*?</title>','<title>Appendix</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="appendix" role="doc-appendix" aria-labelledby="id_appendix">'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['authors-note.xhtml','authorsnote.xhtml'],
     [['<title>.*?</title>','<title>Author’s Note</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="afterword" role="doc-afterword" aria-labelledby="id_afterword">'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['backmatter.xhtml','bm.xhtml','bm1.xhtml'],
     [['<title>.*?</title>','<title>About the Author</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="contributors" aria-label="About the Author" class="author">'],
     ],
    ],
    [['conclusion.xhtml'],
     [['<title>.*?</title>','<title>Conclusion</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="conclusion" role="doc-conclusion" aria-labelledby="id_conclusion">'],
     ],
    ],
    [['contents.xhtml','content.xhtml'],
     [['<title>.*?</title>','<title>Contents</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="toc" role="doc-toc" aria-labelledby="id_contents">'],
     ],
    ],
    [['copy.xhtml','copyright.xhtml','copyrightpage.xhtml'],
     [['<title>.*?</title>','<title>Copyright Page</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="copyright-page" aria-label="Copyright">'],
     ['<meta charset="utf-8"/>',''],
     ['p class=".*?"','p class="copyright"'],
     ['<p>','<p class="copyright">'],
     ['www.orcabook.com|orcabook.com','<a href="https://orcabook.com">orcabook.com</a>'],
     ['orca book publishers','Orca Book Publishers'],
     ['All rights reserved.|All rights are reserved.','All rights are reserved, including those for text and data mining, AI training and similar technologies.'],
     ['(ISBN|EPUB|PDF|LCC|DCC|DDC|LCSH|LCGFT)',lambda x:'<small>' + x.group(1) + '</small>'],
     ['(isbn|\(epub\)|\(pdf\)|lcc|dcc|ddc|lcsh|lcgft)',lambda x:'<small>' + x.group(1) + '</small>'],
     ],
    ],
    [['cover.xhtml','cov.xhtml'],
     [['<title>.*?</title>','<title>Cover of BOOK_TITLE</title>'],
     ['<body epub:type="bodymatter">','<body>'],
     ['<section .*?>','<section aria-label="cover">'],
     ['<meta charset="utf-8"/>',''],
     ['<p.*?>|</p>',''],
     ['<img.*?src="(.*?)".*?/>',lambda x:'<figure class="cover-img">\n\t\n\t<img class="cover-image" role="doc-cover" epub:type="cover" src="' + x.group(1) + '" alt="ALT_TEXT_HERE" />\n</figure>'],
     ],
    ],
    [['dedication.xhtml','ded.xhtml','dedic.xhtml','dedicationpage.xhtml'],
     [['<title>.*?</title>','<title>Dedication</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="dedication" role="doc-dedication" aria-label="Dedication">'],['<meta charset="utf-8"/>',''],
     ['<p class=".*?">','<p class="dedication">'],
     ['<p>','<p class="dedication">'],
     ],
    ],
    [['endnotes.xhtml','footnotes.xhtml'],
     [['<title>.*?</title>','<title>Endnotes</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="endnotes" role="doc-endnotes" aria-labelledby="id_endnotes">\n\t<h1 id="id_endnotes">Endnotes</h1>'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['epigraph.xhtml','epi.xhtml'],
     [['<title>.*?</title>','<title>Epigraph</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="epigraph" role="doc-epigraph" aria-label="Epigraph">'],['<meta charset="utf-8"/>',''],
     ['<p class=".*?">','<p class="epigraph">'],
     ['<p>','<p class="epigraph">'],
     ],
    ],
    [['epilogue.xhtml','epilogue-\d+.xhtml'],
     [['<title>.*?</title>','<title>Epilogue</title>'],
     ['<section .*?>','<section epub:type="epilogue" role="doc-epilogue" aria-labelledby="epilogue_ID">'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['excerpt.xhtml','excerpt-01.xhtml'],
     [['<title>.*?</title>','<title>Excerpt from XXX</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['alt="ALT_TEXT_HERE"','alt="A black and white cover of ALT_TEXT_HERE"'],
     ['<section .*?>','<section aria-label="Excerpt XXX">'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['glossary.xhtml','gloss.xhtml'],
     [['<title>.*?</title>','<title>Glossary</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="glossary" role="doc-glossary" aria-labelledby="id_glossary">'],
     ],
    ],
    [['halftitle.xhtml','halftitlepage.xhtml'],
     [['<title>.*?</title>','<title>Half Title Page</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="halftitlepage" aria-label="Half Title Page">'],
     ],
    ],
    [['index.xhtml'],
     [['<title>.*?</title>','<title>Index</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<nav epub:type="index" role="doc-index" aria-labelledby="id_index">'],['</section>','</nav>'],
     ['<p class="index-first\s*">(.*?)</p>',lambda  x:'\t</ul>\n</section>\n<section aria-label="Letter XXX">\n\t<ul class="index">\n\t\t<p class="index-1">' + x.group(1) + '</p>'],
     ['<p class="index-(\d)\s*">(.*?)</p>',lambda  x:'<li class="index-' + x.group(1) + '">' + x.group(2) + '</li>'],
     ['</p>[ \t\r\n]*</ul>\n</section>\n','</p>\n'],
     ['</li>\s*(?!(<li|</ul>))<','</li>\n\t</ul>\n</section>\n<'],
     ['<b>bold</b>','<b>italic underline</b>'],
     ['<b\s*>','<b class="index">'],
     ],
    ],
    [['introduction.xhtml','intro.xhtml'],
     [['<title>.*?</title>','<title>Introduction</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="introduction" role="doc-introduction" aria-labelledby="id_introduction">'],
     ],
    ],
     [['opening.xhtml','opening-\d+.xhtml'],
     [['<title>.*?</title>','<title>Opening Image</title>'],
     ['<section .*?>','<section aria-label="Opening image chapter XXXX">'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['preface.xhtml'],
     [['<title>.*?</title>','<title>Preface</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="preface" role="doc-preface" aria-labelledby="id_preface">'],['<meta charset="utf-8"/>',''],
     ['<p class=".*?">','<p class="no-indent">'],
     ],
    ],
    [['prologue.xhtml'],
     [['<title>.*?</title>','<title>Prologue</title>'],
     ['<section .*?>','<section epub:type="prologue" role="doc-prologue" aria-labelledby="id_prologue">'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['praise.xhtml'],
     [['<title>.*?</title>','<title>Praise</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section aria-label="Praise for Other Books">'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['opening.xhtml'],
     [['<title>.*?</title>','<title>Opening Image</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section aria-label="Opening Image">'],
     ['<meta charset="utf-8"/>',''],
     ],
    ],
    [['preface.xhtml'],
     [['<title>.*?</title>','<title>Preface</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="preface" role="doc-preface" aria-labelledby="id_preface">'],['<meta charset="utf-8"/>',''],
     ['<p class=".*?">','<p class="no-indent">'],
     ],
    ],
    [['resources.xhtml','bibliography.xhtml'],
     [['<title>.*?</title>','<title>Resources</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="bibliography" role="doc-bibliography" aria-labelledby="id_resources">'],
    ['<p class="resources">(.*?)</p>',lambda  x:'<li class="resources">' + x.group(1) + '</li>'],
    ['</h2>[\t\r\s]*<li class="resources">','</h2>\n\t<ul>\n\t\t<li class="resources">'],
    ['</li>[\t\r\s]*(?=<h2|<p)','</li>\n\t</ul>'],
    ['<i>(.*?)</i>',lambda  x:'<cite>' + x.group(1) + '</cite>'],
     ],
    ],
    [['series.xhtml'],
     [['<title>.*?</title>','<title>More Books</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="seriespage" aria-label="Related Books">'],
     ['<p class=".*?">','<p class="center">'],
     ],
    ],
    [['titlepage.xhtml','title.xhtml','fulltitlepage.xhtml', 'fulltitle.xhtml'],
     [['<title>.*?</title>','<title>Title Page</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="frontmatter">'],
     ['<section .*?>','<section epub:type="titlepage" aria-label="Title Page">'],
#      ['[\s\t]*</section>','<figure class="title">\n\t<img alt="Logo: Orca SERIES_NAME" src="image/orca_NAME_logo.png"/>\n</figure>\n\n<figure class="title">\n\t<img alt="Orca Book Publishers" src="image/orca_book_publishers.png"/>\n</figure>\n</section>'],
     ],
    ],

    ### Redundant
    # [['moresoundings.xhtml','morecurrents.xhtml','moreanchor.xhtml'],
    #  [['<title>.*?</title>','<title>More XXX</title>'],
    #  ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
    #  ['<section .*?>','<section aria-label="More XXX">'],
    #  ['<meta charset="utf-8"/>',''],
    #  ['<p.*?>', '<p class="center">'],
    #  ['orcabook.com','<a href="https://orcabook.com">orcabook.com</a>'],
    #  ],
    # ],
    # [['morebooks.xhtml'],
    #  [['<title>.*?</title>','<title>More XXX</title>'],
    #  ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
    #  ['<section .*?>','<section aria-labelledby="more_id">'],
    #  ['<h1 class="adpage">','<h1 class="adpage" id="more_id">'],
    #  ['alt="ALT_TEXT_HERE"','alt="A black and white cover of ALT_TEXT_HERE"'],
    #  ['<meta charset="utf-8"/>',''],
    #  ],
    # ],
]


