from __future__ import division
import os
from nevow import rend
from nevow import loaders
from nevow import url
from nevow.tags import *
from nevow.rend import NotFound
from nevow.inevow import IRequest
from twisted.web import static
from stanItemDatesTree import stanItemDatesTree
from news import News
from gallery import Gallery
import math
import random

# TODO : get all todos from the webware project
# TODO : implement search index

# - ACK.PY -
    # definitely going to have prev/next
    # definitely going to have an index of all imagedesc's on site
    # might have keywords
    # definitely going to use CSS for layout, not tables
    # last news section on front page
    # last gallery section on front page
    # hilighted quotes at the top of pages...
    # news pages have links to chronologically near galleries
    
# - NEWS/INDEX.PSP -

# TODO : spell-checking hilights incorrect words, can add words to custom dictionary

# TODO : restructured text or textile, etc

  # TODO : (dunno)(later?)
  #        perpage determined by amount of text in news entries
  #        dont display 10 items, display X characters
  #        also allow that number of chars to be specified on url, and this is how you show just ONE entry.
  #        number entries in reverse... so that the first entry chronologically is #1

# - GALLERY/INDEX.PSP -

# RC_Jeep and afterbath amp's
# image alt's required, pah!


'''
<!--

sitewide news here


Latest Updates

Latest News

Latest Galleries


[technobabble]

(Conventions)

Where possible choices have been made to cater to low speed connections
as best as possible. This is primarily evident in the gallery selection
pages' "get samples..." functionality. This machination fetches a random
selection of thumbnails from a gallery randomly when, and only when, you
click the link to do so. The sample images are otherwise not downloaded.

(Requirements)

These pages require a browser capable of handling very old technologies 
like HTML, CSS and Javascript. The latest versions of Internet Explorer 
and FireFox/Mozilla will do. If this makes you whine, don't let me hear you.

(Powered By)

-Mk

-->
'''

'''
nevow pros
  stan - can get something like this for webware, or stan itself perhaps
  fun urls - apache redirects, though they are even more annoying
  twisted - well, twisted is the only real async server system to base it on
            honestly i feel twisted suffers
            if twisted feels like nevow i am right
            many nevow problems are "because twisted does [this-and-that]"
  desktop deployment - i think this should be possible, jml did it
nevow cons
  fun urls - grr, no dirs, files, addSlash madness, relative url madness
  locate madness
  chronological madness, this function named this is run after compile, this is not, can't access this there or here
  query string, what's that?
  you must use our defined alternative web development methods, you can't make your own  
'''

PERPAGE = 4
GALLERY = Gallery('D:\\Web\\galleria\\media\\gallery')
GALLERY.loadsections()  
NEWSLIST = []
for root, dirnames, filenames in os.walk('D:\\Web\\galleria\\media\\news',False):
  for filename in filenames:
    NEWSLIST.append(News.FromFile(os.path.join(root,filename)))    
for section in GALLERY.sections:
  section.loaddesc()
  section.loadimages()
  for image in section.images:
    image.loaddesc()

class RawPage(rend.Page):

  addSlash = True
  
  def render_title(self, ctx, data):
    return 'Galleria'
    
  def render_content(self, ctx, data):
    return 'No Content'
  
  docFactory = loaders.stan(
    [
      xml('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'),
      html[
        head[
          title[directive('title')],
          link(rel='stylesheet', href='/static/style.css', type='text/css')
        ],
        body[
          directive('content')
        ]
      ]
    ]
  )

class BasicPage(RawPage):
  
  def render_title(self, ctx, data):
    path = ctx.locate(IRequest).prepath
    result = RawPage.render_title(self, ctx, data)
    if path!=['']:
      result += ' : '
      result += '/'.join(path)
    return result

  def render_content(self, ctx, data):
    return self.render_layout(ctx, data)
    
  def render_layout(self, ctx, data):
    return [
      
      div(_class='wrapper')[
        div(_class='content')[

          div(_class='left')[
            div(_class='menu')[
              div(_class='menuitems')[
#                div(_class='menuitem alignright')[
#                  a(href='/news')['News'],
#                  span(_class='f150')[xml('&nbsp;&#0187;')]
#                ],
                div(_class='menuitem alignright')[
                  a(href='/gallery')['Gallery'],
                  span(_class='f150')[xml('&nbsp;&#0187;')]
                ],
#                div(_class="menuitem alignright")[
#                  a(href='/search')['Search'],
#                  span(_class='f150')[xml('&nbsp;&#0187;')]
#                ],
                div(_class='menuitem alignright')[
                  a(href='/')['Home'],
                  span(_class='f150')[xml('&nbsp;&#0187;')]
                ]
              ]
            ]
          ],

          directive('rightmenu'),

          div(_class='top')[
            div(_class='topinner')[img(src='/static/name.gif')],
            div(_class='prevnext')[
              xml('&laquo; '), directive('prevlink'), ' | ', directive('nextlink'), xml(' &raquo;')
            ]
          ],
          
          directive('dynamic')

        ]
      ]
      
    ]
    
  def render_dynamic(self, ctx, data):
    return self.render_static(ctx, data)
    
  def render_static(self, ctx, data):
    return p['static content undefined in ',self.__class__.__name__]
  
  def link(self,name,url=None):
    if url==None:
      result = span(_class='disabledlink')[name]
    else:
      result = a(href=url)[name]
    return result
  
  def render_prevlink(self, ctx, data):
    return self.link('prev',self.prevurl())

  def render_nextlink(self, ctx, data):
    return self.link('next',self.nexturl())

  def prevurl(self):
    return None

  def nexturl(self):
    return None
  
  def render_rightmenu(self, ctx, data):
    return ''
    
class NewsPage(BasicPage):
  
  def __init__(self,pageno=None):
    BasicPage.__init__(self)    
    self.pagecount=None

    self.pagecount = len(NEWSLIST[::PERPAGE])
    
    if pageno==None:
      pageno = self.pagecount
    
    self.pageno = pageno

  def locateChild(self, request, segments):
    if len(segments)>2:
      return NotFound
    if segments[0]=='':
      pageno=None
      return NewsPage(), []
    else:
      try:
        pageno=int(segments[0])
        return NewsPage(pageno), []
      except ValueError:
        return NotFound

  def prevurl(self):
    result = None
    if self.pageno>1:
      result = '/news/'+str(self.pageno-1)
    return result
    
  def nexturl(self):
    result = None
    if self.pageno<self.pagecount:
      result = '/news/'+str(self.pageno+1)
    return result
    
  def render_rightmenu(self, ctx, data):
    return stanItemDatesTree(NEWSLIST,PERPAGE,'/news/')
    
  def render_static(self, ctx, data):
    i=(self.pageno-1)*PERPAGE
    j=i+PERPAGE
    
    newslistslice = NEWSLIST[i:j]
    newslistslice.reverse()
    
    shown = len(newslistslice)
    
    i = 0
    result = ''
    result += '<a name="0"></a>'
    for news in newslistslice:
      result += '<a name="%d"></a>'%(shown-i)
      result += '<div class="news">\n'
      result += '  <div class="newshead">\n'
      result += '    <div class="newsextra">'+news.agestring()+'</div>\n'
      result += '    <div class="newstitle">\n'
      result += news.datestring()
      result += ' <a href="#0">^</a>'
      result += '    </div>\n'
      result += '  </div>\n'
      result += '  <div class="newsbody">\n'
      result += news.contentfiltered()+'\n'
      result += '  </div>\n'
      result += '</div>\n'
      i = i + 1
    
    return xml(result)
  
class GalleryVisitPage(BasicPage):
  
  def __init__(self,sectionno=None):
    BasicPage.__init__(self)
    self.sectionno = sectionno

    if sectionno==None:
      sectionno = len(GALLERY.sections)
    
    self.sectionno = sectionno
    self.section = GALLERY.sections[self.sectionno-1]
    
  def locateChild(self, request, segments):
    if segments[0]=='':
      return GalleryVisitPage(), []
    else:
      try:
        sectionno = int(segments[0])
        if sectionno<1 or sectionno>len(GALLERY.sections):
          return NotFound
        return GalleryVisitPage(sectionno), []
      except ValueError:
        return NotFound

  def render_static(self,ctx,data):    
    
    gallpage = math.ceil(self.sectionno/PERPAGE)
    gallhash = (self.sectionno%PERPAGE)

    result = ''
    
    result += '<div class="galleryinfo">'
    result += '  <div class="galleryinfohead">'
    result += '    <div class="galleryinfoextra">'
    result += self.section.date.strftime('%A, %B %d, %Y')
    result += '    </div>'
    result += '    <div class="galleryinfotitle">'
    result += self.section.name
    result += '    </div>'
    result += '  </div>'
    result += '  <div class="galleryinfosubmenu">'
    result += '    <div class="galleryinfosubmenuitem">'
    result += '      &laquo; <a href="/gallery/%d#%d">galleries</a>' % (gallpage,gallhash)
    result += '    </div>'
    result += '  </div>'
    result += '  <div class="galleryinfobody">'
    result += self.section.desc
    result += '  </div>'
    result += '  <div class="thumbnails">'
    
    for image in self.section.images:      
      result += '<div class="thumbnail"><a href="/gallery/view/%d/%d"><img src="/thumbs/%s" width="100" height="100"></a></div>'%(self.section.no,image.no,image.getthumbfilename())
      
    result +=   '</div>'
    result += '</div>'    
    
    return xml(result)

class GalleryViewPage(BasicPage):

  def __init__(self,sectionno=None,imageno=None):
    BasicPage.__init__(self)
    self.sectionno = sectionno
   
    if sectionno==None:
      sectionno = len(GALLERY.sections)
      
    self.sectionno = sectionno
    self.section = GALLERY.sections[self.sectionno-1]

    self.imagecount = len(self.section.images)
    
    if imageno==None:
      imageno = self.imagecount
    
    self.imageno = imageno
    self.image = self.section.images[self.imageno-1]
    
    if self.image.desc==None:
      self.image.desc='<span class="disabledtext">(no description)</span>'
    
  def locateChild(self, request, segments):
    if segments[0]=='':
      return GalleryViewPage(), []
    else:
      try:
        sectionno = int(segments[0])
        section = GALLERY.sections[sectionno-1]
        imageno = int(segments[1])
        imagecount = len(section.images)
        if sectionno<1 or sectionno>len(GALLERY.sections):
          print '*'*100+'AAA'
          return NotFound
        if imageno<1 or imageno>imagecount:
          print '*'*100+'BBB('+str(imageno)+':'+str(sectionno)+':'+str(len(section.images))+':'+section.name+':'+str(section.no)+')'
          return NotFound
        return GalleryViewPage(sectionno,imageno), []
      except ValueError:
        print '*'*100+'CCC'
        return NotFound
      except IndexError:
        print '*'*100+'DDD'
        return NotFound
  
  def prevurl(self):
    result = None
    if self.imageno>1:
      result = '/gallery/view/'+str(self.sectionno)+'/'+str(self.imageno-1)
    return result
    
  def nexturl(self):
    result = None
    if self.imageno<self.imagecount:
      result = '/gallery/view/'+str(self.sectionno)+'/'+str(self.imageno+1)
    return result

  def render_static(self, ctx, data):    
    result = ''    

    result += '<div class="galleryinfo">'
    result += '  <div class="galleryinfohead">'
    result += '    <div class="galleryinfoextra">'
    result += ''
    result += '    </div>'
    result += '    <div class="galleryinfotitle">'
    result += self.image.name
    result += '    </div>'
    result += '  </div>'
    result += '  <div class="galleryinfosubmenu">'
    result += '    <div class="galleryinfosubmenuitem">'
    result += '      &laquo; <a href="/gallery/visit/%d">thumbnails</a>' % (self.sectionno)
    result += '    </div>'
    result += '  </div>'
    result += '  <div class="galleryinfobody">'
    result += self.image.desc
    result += '  </div>'

    result += '  <div class="photo">'
    result += '    <img src="%s">' % (self.image.getfixedlink())
    #result += '<br><a href="%s">original</a>' % (self.image.getoriginallink())
    result += '  </div>'
    
    return xml(result)

class GalleryPage(BasicPage):
  
  def __init__(self,pageno=None):
    BasicPage.__init__(self)
    self.pagecount=None

    self.pagecount = len(GALLERY.sections[::PERPAGE])

    if pageno==None:
      pageno = self.pagecount
    
    self.pageno = pageno

  def locateChild(self, request, segments):
    if segments[0]=='visit':
      return GalleryVisitPage(), segments[1:]
    elif segments[0]=='view':
      return GalleryViewPage(), segments[1:]
    elif segments[0]=='':
      return GalleryPage(), []
    else:
      try:
        return GalleryPage(int(segments[0])), []
      except ValueError:
        return NotFound
    
  # basically the same in NewsPage
  def prevurl(self):
    result = None
    if self.pageno>1:
      result = '/gallery/'+str(self.pageno-1)
    return result
    
  def nexturl(self):
    result = None
    if self.pageno<self.pagecount:
      result = '/gallery/'+str(self.pageno+1)
    return result

  def render_rightmenu(self, ctx, data):
    return stanItemDatesTree(GALLERY.sections,PERPAGE,'/gallery/')
    
  def render_static(self, ctx, data):

    # RC_Jeep and afterbath amp's
    # image alt's required, pah!

    randomizer = random.Random()

    x=(self.pageno-1)*PERPAGE
    y=x+PERPAGE
    
    gallerysectionslice = GALLERY.sections[x:y]
    gallerysectionslice.reverse()
    
    shown = len(gallerysectionslice)
        
    i = 0
    result = ''
    for section in gallerysectionslice:  
      result += '<a name="%d"></a>'%(shown-i)
      result += '<div class="galleryinfo">'
      result += '  <div class="galleryinfohead">'
      result += '    <div class="galleryinfoextra">'
      result += section.date.strftime('%A, %B %d, %Y')
      result += '    </div>'
      result += '    <div class="galleryinfotitle">'
      result += section.name
      result += '    </div>'
      result += '  </div>'
      result += '  <div class="galleryinfosubmenu">'
      result += '    <div class="galleryinfosubmenuitem">'
      result += '      <a href="/gallery/visit/%d">visit this gallery</a> &raquo;' % (section.no)
      result += '    </div>'
      result += '    <div class="galleryinfosubmenuitem">'
      result += '      <div onclick="javascript:togglethumbs(this,%d);return false;" class="thumbstoggle">'%(i)
      result += '        <a href="javascript:void(0);"><img class="sw" src="/static/sw.gif">&nbsp;get&nbsp;samples...</a>'
      result += '      </div>'
      result += '    </div>'
      result += '  </div>'
      result += '  <div class="galleryinfobody">'
      result += section.desc
      result += '  </div>'
      result += '  <div class="thumbnails" id="thumbnails%d" style="display:none">'%(i)
        
      numsamples = 4
      if len(section.images)<numsamples:
        numthumbs=len(section.images)
      else:
        numthumbs=numsamples
      for image in randomizer.sample(section.images,numthumbs):    
        result += '<div class="thumbnail"><a href="/gallery/view/%d/%d"><img id="%s" src="/static/unavailable.gif" width="100" height="100"></a></div>'%(section.no,image.no,image.getthumbfilename())
      result +=   '</div>'
      result += '</div>'
      i = i + 1
    
    result += '''
    <script type="text/javascript">
      thumbstateslen = '''+str(i)+''';
      thumbstates = new Array(thumbstateslen);
      for (i=0;i<thumbstateslen;i++) {
        thumbstates[i]=false;
      }
      function togglethumbs(sender,id) {
        thumbnailsdiv = document.getElementById('thumbnails'+id);
        if (thumbstates[id]==false) {
          thumbnailsdiv.style.display = 'block';
          setthumbsources(thumbnailsdiv);
          thumbstates[id] = true;
        } else {
          thumbnailsdiv.style.display = 'none';
          sender.firstChild.innerHTML = sender.firstChild.innerHTML.replace('hide','show');
          thumbstates[id] = false;    
        }   
      }
      function setthumbsources(thumbnailsdiv) {
        divs = thumbnailsdiv.childNodes;
        for (i=0;i<divs.length;i++) {            
          imgnode = divs[i].firstChild.firstChild;
          imgnode.src = '/thumbs/'+imgnode.id;
        }
      }
    </script>
    '''
      
    return xml(result)

#class SearchPage(BasicPage):
#  pass  

class MainPage(BasicPage):

  child_gallery = GalleryPage()
  child_news = NewsPage()
#  child_search = SearchPage()

  child_static = static.File('static')
  child_thumbs = static.File('thumbs')  
  child_photos = static.File('D:/Web/galleria/media/gallery/')
  child_cache = static.File('cache') # stores resized photos
  
  def render_static(self, ctx, data):
    return xml(file('D:\\Web\\galleria\\media\index.txt').read())