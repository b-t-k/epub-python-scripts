## Clean epub-Fiction Files

from datetime import datetime

opf_file2=[
    ['(?s)<metadata(.*?)>.*?</metadata>',lambda x:'<metadata ' + x.group(1) + '>\n' + """
    <dc:title id="title">The_TITLE</dc:title>
    <meta property="file-as" refines="#title">TITLE, The</meta>
    <meta property="title-type" refines="#title">main</meta>
    <dc:title id="subtitle">THE_SUBTITLE</dc:title>
    <meta property="title-type" refines="#subtitle">subtitle</meta>
    <dc:title id="fulltitle">The_TITLE: THE_SUBTITLE</dc:title>
    <meta property="file-as" refines="#fulltitle">TITLE: THE_SUBTITLE, The</meta>
    <meta property="title-type" refines="#fulltitle">extended</meta>
    <meta property="belongs-to-collection" id="id-1">SERIES_TITLE</meta>
    <meta refines="#id-1" property="collection-type">series</meta>
    <meta refines="#id-1" property="group-position">1</meta>
    <dc:creator id="creator1">AUTHOR_FIRST_AUTHOR_LAST</dc:creator>
    <meta refines="#creator1" property="role" scheme="marc:relators">aut</meta>
    <meta refines="#creator1" property="file-as">AUTHOR_LAST, AUTHOR_FIRST</meta>
    <dc:creator id="illustrator1">ILLUS_FIRST_ILLUS_LAST</dc:creator>
    <meta refines="#illustrator1" property="role" scheme="marc:relators">ill</meta>
    <meta refines="#illustrator1" property="file-as">ILLUS_LAST, ILLUS_FIRST</meta>
    <dc:identifier id="epubISBN">9780000000000</dc:identifier>
    <dc:identifier id="bookid">urn:isbn:9780000000000</dc:identifier>
    <dc:source id="printISBN">9780000000000</dc:source>
    <meta property="pageBreakSource">urn:isbn:9780000000000</meta>
    <dc:publisher>PUBLISHER</dc:publisher>
    <dc:language>en-US</dc:language>
    <dc:date>2024-MO-DA</dc:date>
    <dc:rights>Copyright © Text INSERT_YEAR AUTHOR_NAME, Illustrations INSERT_YEAR ILLUS_NAME</dc:rights>
    <dc:description>THIS_IS_THE_DESCRIPTION</dc:description>
    <meta property="schema:accessMode">textual</meta>
    <meta property="schema:accessMode">visual</meta>
    <meta property="schema:accessModeSufficient">textual</meta>
    <meta property="schema:accessibilityFeature">displayTransformability</meta>
    <meta property="schema:accessibilityFeature">pageBreakMarkers</meta>
    <meta property="schema:accessibilityFeature">readingOrder</meta>
    <meta property="schema:accessibilityFeature">structuralNavigation</meta>
    <meta property="schema:accessibilityFeature">ARIA</meta>
    <meta property="schema:accessibilityFeature">tableOfContents</meta>
    <meta property="schema:accessibilityFeature">alternativeText</meta>
    <meta property="schema:accessibilityHazard">none</meta>
    <meta property="schema:accessibilitySummary">A simple book with some images. This book contains various accessibility features. A digital rights page has been added and number of blank and/or ad pages in the print equivalent book have been removed or substituted from this digital EPUB. This publication conforms to WCAG 2.2 Level AA.</meta>
    <link rel="dcterms:conformsTo" href="http://www.idpf.org/epub/a11y/accessibility-20170105.html#wcag-aa"/>
    <meta property="a11y:certifiedBy">Benetech via eBOUND Canada</meta>
    <meta property="a11y:certifierCredential">https://bornaccessible.org/certification/gca-credential/</meta>
    <meta property="dcterms:modified">""" + datetime.today().strftime('%Y-%m-%d') + """</meta>
    <meta content="cover-image" name="cover"/>
    <meta property="ibooks:specified-fonts">true</meta>""" + '</metadata>'],

]


pages_list_fiction=[

    [['about-the-author.xhtml'],
     [['<title>.*?</title>','<title>About the Author</title>'],
     ['<body epub:type="bodymatter">','<body epub:type="backmatter">'],
     ['<section .*?>','<section epub:type="contributors" aria-label="About the Author" class="author">'],
     ['<meta charset="utf-8"/>',''],
     ['p class=".*?"','p class="no-indent"'],
     ['<figure class=".*?">[\n\r\t\s]*<img.*?src="(.*?)".*?/>',lambda x:'<figure class="author">\n<img class="author" src="' + x.group(1) + '" alt="A black and white photo of the author, ADD_NAME_HERE" />\n'],
     ],
    ],
]

# search and replace for nav.xhtml
list_nav=[
    # Set nav page defaults
    ['(.*?)\.html', lambda x:  x.group(1) + '.xhtml'],
    ['<meta.*?>', ''],
    ['<title>.*?</title>', '<title>Nav Contents</title>'],
    ['(?s)<style type="text/css">.*?</style>', ''],
    ['<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">', '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en-US" xml:lang="en-US">'],
    ['(?s)<nav epub:type="landmarks".*?</nav>',
    """
    <nav id="landmarks" epub:type="landmarks" aria-labelledby="nav_landmarks">
        <h1 id="nav_landmarks">Landmarks</h1>
        <ol>
        <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>
        <li><a epub:type="frontmatter" href="digitalrights.xhtml">Statement of Digital Rights</a></li>
        <li><a epub:type="bodymatter" href="chapter-01.xhtml">BOOK_TITLE</a></li>
        <li><a epub:type="backmatter" href="acknowledgments.xhtml">Acknowledgments</a></li>
        <li><a epub:type="contributors" href="about-the-author.xhtml">About the Author</a></li>
        <li><a epub:type="backmatter" href="morebooks.xhtml">More Books</a></li>
    </ol>
    </nav>
    """
    ], 

    ['<nav id="toc" epub:type="toc"><h2>Contents</h2>', '<nav id="toc" epub:type="toc" role="doc-toc" aria-labelledby="nav_contents">\n\t<h1 id="nav_contents">Contents</h1>'],

    ['(?s)<nav epub:type="toc" id="toc">.*?<h1>Table of Contents</h1>|<nav id="toc" epub:type="toc">\n\t+<h2>Contents</h2>',
     """
    <nav id="toc" epub:type="toc" role="doc-toc" aria-labelledby="nav_contents">
        <h1 id="nav_contents">Contents</h1>
     """],
    ['<nav id="toc" epub:type="toc"><h2>Contents</h2>',
     """
    <nav id="toc" epub:type="toc" role="doc-toc" aria-labelledby="nav_contents">
        <h1 id="nav_contents">Contents</h1>
     """],
     ['>\d+','>'],

    ## French version
#     ['(?s)<nav epub:type="landmarks".*?</nav>',
#     """
#     <nav id="landmarks" epub:type="landmarks" aria-labelledby="nav_landmarks">
# <h1 id="nav_landmarks">Repères</h1>
#   <ol>
#     <li><a epub:type="cover" href="cover.xhtml">Couverture</a></li>
#     <li><a epub:type="frontmatter" href="digitalrights.xhtml">Déclaration des droits numériques</a></li>
#     <li><a epub:type="bodymatter" href="chapter-01.xhtml">BOOK_TITLE</a></li>
#     <li><a href="about.xhtml">A propos de l’auteur</a></li>
#     <li><a epub:type="backmatter" href="autres.xhtml">Collection française</a></li>
#   </ol>
# </nav>
#     """
    # ],
]

