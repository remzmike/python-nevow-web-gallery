import os
from mx.DateTime import DateTime, DateTimeFrom, Age, Month

class News:

  def __init__(self,date=None,content=None):
    self.date = date
    self.content = content
  
  def FromFile(cls,filepath):
    result = News()
    result.loadfromfile(filepath)
    return result
  FromFile = classmethod(FromFile)
  
  def loadfromfile(self,filepath):
    filename = os.path.basename(filepath)
    self.date = DateTimeFrom(os.path.splitext(filename)[0])
    self.content = file(filepath,'r').read()
    
  def datestring(self):
    return self.date.strftime('%A, %B %d, %Y')
    
  def datestringshort(self):
    return self.date.strftime('%m-%d-%Y')

  def agestring(self):
    age = Age(self.date,DateTime(1999,2,19))
    
    fstring = '%s years, %s months, %s days'
    fvars = (age.years,age.months,age.days)
    if age.months==0:
      fstring = '%s years, %s days'
      fvars = (age.years,age.days)
    if age.days==0:
      fstring = '%s years, %s months'
      fvars = (age.years,age.months)
    if age.months==0 and age.days==0:
      fstring = '%s years old! Happy birthday!'
      fvars = (age.years)    
    return fstring%(fvars)

  def contentfiltered(self):
    s = self.content
    s = s.replace('<p>','<br><br>')
    s = s.replace('</p>','<br><br>')
    # TODO : spellchecking of some sort...
    # TODO : long word mutilation...
    splat = s.split(' ')
    for word in splat:
      if len(word)>50:
        #newword = ''
        #i=0
        #for letter in word:
        #  i=i+1
        #  newword=newword+letter
        #  if i%50==0:
        #    newword=newword+'<br>'          
        #s = s.replace(word,newword)
        # ... i ended up putting a <br> in the middle of a <br> which was in the content, <b<br>r>, so this is a problem
        s = s.replace(word,word[:50]+'...')
    return s
