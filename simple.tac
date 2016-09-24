from twisted.application import internet
from twisted.application import service

from nevow import appserver

from Pages import MainPage

application = service.Application('nevowtest')
internet.TCPServer(4003, appserver.NevowSite(MainPage())).setServiceParent(application)
