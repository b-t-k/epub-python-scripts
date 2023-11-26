
# List of simple deletions or replacements
list_delete=[
    ['<div( .*?)?>',''],
    ['<div .*?>',''],
    ['</div>',''],
    ['_idGenParaOverride-\d+',''],
    [' id="_idContainer\d+"',''],
    [' class="_idGenObjectAttribute-\d+"',''],
    ['_idGenCharOverride-\d+',''],
    ['_idGenObjectStyle-Disabled\s?',''],
    [' CharOverride-\d+',''],
    ['style=".*?"',''],

    ['<p class="para" lang="en-US">','<p>'],
    ['<p class="copyright" lang="en-US">','<p class="copyright">'],
    ['<p class="no-indent" lang="en-US">','<p class="no-indent">'],
    ['lang="en-CA" xml:lang="en-CA"',''],
    ['lang="en-US" xml:lang="en-US"',''],
    ['lang="en-GB" xml:lang="en-GB"',''],
    ['xml:lang="en-CA"|xml:lang="en-US"|xml:lang="en-GB"',''],
    ['ParaOverride-\d+',''],
    ['class="Basic-Paragraph "',''],
    ['<i class=".*?(?=>)>','<i>'],
    ['<em.*?(?=>)>','<em>'],

    ['<em> ',' <em>'],
    ['<i> ',' <i>'],
    ['<small class=".*?">','<small>'],
    ['class="body-text"',''],
    ['<figure id="_idContainer\d+" class="full">','<figure class="full">'],

    ['<p(?:\s)?(?:class=".*?")?>PAGEBREAK</p>','<hr/>'],
    ['<p(?:\s)?(?:class=".*?")?>BREAK</p>','<hr/>'],
]

#list of regex replacements
list_replace=[
    # replace rorohiko pagestaker spans
     ['<span class="com-rorohiko-pagestaker-style.*?>','<span class="com-rorohiko-pagestaker-style">'],
     
    ['<span class=("com-rorohiko-pagestaker-style")>(\d+|[iv]{1,})</span>',lambda  x:"<span epub:type=\"pagebreak\" role=\"doc-pagebreak\" id=\"page" + x.group(2) + "\" aria-label=\"page " + x.group(2) + "\"/>"],

    ['<span class="com-rorohiko-pagestaker-style"><a id=(.*?)</span>', lambda x:'<a id=' + x.group(1)],

    # get rid of extra spans
    ['(?s)<span lang="en-\w+" xml:lang="en-\w+">(.*?)</span>',lambda  x:x.group(1)],
    [' lang="en-CA" xml:lang="en-CA"',''],

### DEAL WITH FIGURES
    # clean up figure div
    ['<figure id="_idContainer\d+" class="Figure" >','<figure class="full">'],  

    #replace img with figure if no figure and follows </p> or <img ... /> 
     ['(?:(?<=<\/p>)|(?<=\/>))[\n\t+]+<img src="(.*?)" alt="" />',lambda x:'<figure class="full">\n\t<img class="float" src="' + x.group(1) + '" alt="ALT_TEXT_HERE" />\n</figure>'],

    #replace img 
     ['\t+<img src="(.*?)" alt="" />',lambda x:'\n\t<img class="float" src="' + x.group(1) + '" alt="ALT_TEXT_HERE" />\n'],

    # move photo credit (figcaption) into figcaption
     ['<figcaption class="photo-caption".*?>(.*?)</figcaption>\n\t+<figcaption class="photo-credit".*?>(.*?)</figcaption>',lambda x: '<figcaption class="photo-caption">' + x.group(1) + ' <span class="photo-credit">' + x.group(2) + '</span></figcaption>'],
    
     # move photo credit (span) into figcaption
     ['<figcaption class="photo-caption".*?>(.*?)</figcaption>\n\t+<span class="photo-credit".*?>(.*?)</span>',lambda x: '<figcaption class="photo-caption">' + x.group(1) + ' <span class="photo-credit">' + x.group(2) + '</span></figcaption>'],
    
    # move figcaption photo credit into span
     ['<figcaption class="photo-credit".*?>(.*?)</figcaption>',lambda x: '<figcaption class="photo-caption"><span class="photo-credit">' + x.group(1) + '</span></figcaption>'],
     
     # regex to find / in photo credit string and add thin spaces before and after (run twice)
    ['(?<=<span class="photo-credit">)(.*?[^ ][^<br/>])/([^ ].*?)(?=</span>)',lambda x: x.group(1)+ " / " + x.group(2)],
    ['(?<=<span class="photo-credit">)(.*?[^ ][^<br/>])/([^ ].*?)(?=</span>)',lambda x: x.group(1)+ " / " + x.group(2)],

    # clean up extra spaces in <br/>
    ['<br  / >','<br/>'],

     #put figcaption in figure
     ['</figure>(\n\t+)+<figcaption class="photo-caption">(.*?)</figcaption>',lambda x: '<figcaption class="photo-caption">' + x.group(2) + '</figcaption>\n</figure>'],

### Misc
     # move space from inside span to outside
     ['<span(.*?)>(.*?)\s</span>', lambda x: '<span' + x.group(1) + '>' + x.group(2) + '</span> '],

     # move space to outside span
     ['\s</(.*?)>', lambda x: '</' + x.group(1) + '> '],

     ['<aside class="(.*?)">', lambda x: '<aside class="' + x.group(1) + '" aria-labelledby="Sidebar_ID-XXX">'],
]
