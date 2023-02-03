import os
import zope.interface

deleteOffCreation = True

if deleteOffCreation:
    os.path.getctime()
else:
    os.path.getmtime()
