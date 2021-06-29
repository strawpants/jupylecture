# convenience tools for setting up lecture slides
# Roelof Rietbroek 2020

from IPython.display import Video,display_html,display_markdown,HTML,Markdown,display

import binascii

import os

import re

from lxml import etree as ET

import markdown


mdp=markdown.Markdown(extensions=['mdx_math'])


def hideCode():   
    """Hides the code section of a jupyter notebook cell and only keep the output
    see also https://www.markroepke.me/posts/2019/06/05/tips-for-slideshows-in-jupyter.html"""

    uid = binascii.hexlify(os.urandom(8)).decode()
    html = """<div id="%s"></div>
    <script type="text/javascript">
        $(function(){
            var p = $("#%s");
            if (p.length==0) return;
            while (!p.hasClass("cell")) {
                p=p.parent();
                if (p.prop("tagName") =="body") return;
            }
            var cell = p;
            cell.find(".input").addClass("hide-in-slideshow")
        });
    </script>""" % (uid, uid)
    display_html(html, raw=True)



class FlexSlide():
    """Class which setups the cell output as a flex container, which allows more flexible structuring (see also the rise.css file)"""
    def __init__(self,title):
        hideCode()

        self.mdhead="\n<div class=\"flxsld text_cell\" ><div class=\"flx100\">"+mdp.convert(title)+"</div>\n"
        self.mdfoot="\n</div>"
        self.payload=""  
    
    @staticmethod
    def formatClass(flxwidth=None,frag=False,absPos=False,xtrclass=None):
        """constructs the appropriate html class string"""

        if flxwidth or frag:
            cls="class=\""
        else:
            return ""

        if flxwidth:
            cls+=" %s"%flxwidth
        
        if frag:
            cls+=" fragment fade-in"
        
        if absPos:
            cls+=" flxabove"

        if xtrclass:
            cls+=f" {xtrclass}"
        return cls+"\""
    
    @staticmethod
    def formatStyle(width=None,top=None,left=None):
        """constructs the appropriate html style string"""

        if width or top or left:
            style="style=\""
        else:
            return ""

        if width:
            style+="width:%s;"%width
        
        if top:
            style+="top:%s;"%top
         
        if left:
            style+="left:%s;"%left

        return style+"\""


    def addimg(self,path,caption="",flxwidth=None,width=None,frag=False,top=None,left=None,alt=None):
        """Adds an image"""
        addcap=""
        
        if caption:
            addcap="<small>%s</small>"%caption
        md=""
        if type(path) == list:
            for pth in path:
                md+="<img src=\"%s\" alt=\"%s\" %s />%s"%(pth,alt,FlexSlide.formatStyle(width=width),addcap)
        else:
            md="<img src=\"%s\" alt=\"%s\" %s />%s"%(path,alt,FlexSlide.formatStyle(width=width),addcap)
        
        self.addmd(md,frag=frag,flxwidth=flxwidth,top=top,left=left)
            

    def addmd(self,mdcontent,frag=False,flxwidth=None,top=None,left=None,shape=None):
        cls=FlexSlide.formatClass(flxwidth,frag,absPos=top or left,xtrclass=shape)
        style=FlexSlide.formatStyle(top=top,left=left)
        htmlcontent=mdp.convert(mdcontent)
        self.payload+="\n<div %s %s>\n\n"%(cls,style)+htmlcontent+"</div>"


    def addVideo(self,path,flxwidth=None):
        self.addmd(Video(path)._repr_html_(),flxwidth=flxwidth)
     
    @staticmethod
    def formatItems(items,frag):
        """Format items in a list as html <ul>.. </ul>,possibly calling this function recursively to allow sublists"""
        html="<ul>"

        for item in items:
            if type(item) == list:
                #call this method recursively
                html+=FlexSlide.formatItems(item,frag)
                continue

            if frag:
                html+="<li class=\"fragment fade-in\">%s</li>"%item
            else:
                html+="<li>%s</li>"%item

        html+="</ul>"

        return html

    def addItems(self,items,frag=False,flxwidth=None,color=None):       
        
        html=FlexSlide.formatItems(items,frag)

        self.addmd(html,flxwidth=flxwidth,shape=color)

    def addSVG(self,svgname,width=None,height=None,flxwidth=None,frag=False):
        """Embed SVG as code in a code cell and fix relative links"""

        svgroot = ET.parse(svgname).getroot()
        if width:
            try:
                svgroot.attrib["width"]=width
                del svgroot.attrib["height"]
            except KeyError:
                pass
        elif height:
            try:
                svgroot.attrib["height"]=height
                del svgroot.attrib["width"]
            except KeyError:
                pass


        #change absolute embedded image links to relative links
        if "xlink" in svgroot.nsmap:
            hrefky="{"+svgroot.nsmap["xlink"]+"}href"
        
            for el in svgroot.findall(".//{*}image[@"+hrefky+"]"):
                el.attrib[hrefky]=re.sub("\S+/images/","images/",el.attrib[hrefky]) 

        self.addmd(ET.tostring(svgroot).decode('utf-8'),flxwidth=flxwidth,frag=frag)

    def addCircle(self,mdcontent=None,flxwidth=None,frag=None):
        """adds a circle, possibly with content"""
        self.addmd(mdcontent,flxwidth=flxwidth,frag=frag,shape="circ1")

    def _repr_markdown_(self):
        # print("\n".join([self.mdhead,self.payload,self.mdfoot]))

        return "\n".join([self.mdhead,self.payload,self.mdfoot])

    
    def display(self):
        display(self)
