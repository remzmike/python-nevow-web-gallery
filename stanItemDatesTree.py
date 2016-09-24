from __future__ import division
import math
from vlib.vdict import ksort, rreverse
from mx.DateTime import Month
from nevow.tags import *
from nevow import url


def stanItemDatesTree(items, perpage, hrefprefix=''):

    #hack function, make result mutable type (a list) for inner function to work, double hack
    result = []
    def kwrite(s,buf=result):
      buf.append(s)

    prevyear = None
    prevmonth = None
    prevday = None

    itemtree = {}
    # {'2003':{'12':{'25':(item,page)}}}
    
    i = 0
    for item in items:
      i = i + 1
      if item.date.year!=prevyear:
        itemtree[item.date.year] = {}
        prevyear=item.date.year
        prevmonth=None
        prevday=None
      if item.date.month!=prevmonth:
        itemtree[item.date.year][item.date.month] = {}
        prevmonth=item.date.month
        prevday=None
        monthname = item.date.strftime('&nbsp;&nbsp;%B')
      if item.date.day!=prevday:        
        page = int(math.ceil(i/perpage))
        subindex = ((i-1)%perpage)+1
        itemtree[item.date.year][item.date.month][item.date.day] = (item,page,subindex)
        prevday=item.date.day
      
    kwrite('<div class="right">')
    kwrite('  <div class="menu">')
    kwrite('    <div class="menuitems">')

    for year in rreverse(ksort(itemtree)):
      kwrite('      <div class="menuitem alignleft">')
      kwrite('        <b>%d</b>' % (year))
      kwrite('      </div>')
      for month in ksort(itemtree[year]):        
        kwrite('      <div class="menuitem alignleft">')
        kwrite('        %s ' % (Month[month]))
        daycount = len(itemtree[year][month])
        i = 0
        for day in ksort(itemtree[year][month]):          
          i = i + 1
          item,page,subindex = itemtree[year][month][day]
          #href='%d/%d/%d'%(year,month,day)
          href='%d#%d'%(page,subindex)
          name='%d'%(day)
          kwrite('<a href="%s%s">%s</a>' % (hrefprefix,href,name))

          if i!=daycount:
            kwrite(', ')          
        kwrite('      </div>')
                        
    kwrite('    </div>')
    kwrite('  </div>')
    kwrite('</div>')
    
    return xml('\n'.join(result))