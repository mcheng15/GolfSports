import re
import locale
locale.setlocale( locale.LC_ALL, 'english_USA' )

class Venue:
    def __init__(self):
        self.venues_list = []

    def addVenue(self, venue):
        newCourse = ConvertVenueToCourseClass(venue)
        self.venues_list.append(venue)

class Course(object):
    def __init__(self):
        self.name = None
        self.location = None
        self.par = None
        self.length = None

    def __eq__(self, other):
        return (self.name == other.name) & (self.location == other.location) & (self.par == other.par) & (self.length == other.length)

def ConvertVenueToCourseClass(strVenue):
    match = re.match(r'([^-\|]+)-*([^\|]*)[\|]*(.*)', strVenue)
    newCourse = Course()
    idx = 0
    for courseGroups in match.groups():
        if (courseGroups == None):
            continue
        if (idx == 0):
            newCourse.name = courseGroups.strip()
        elif (idx == 1):
            newCourse.location = courseGroups.strip()
        elif (idx == 2): #parse par value and length from
            length = courseGroups.strip()
            lengthGroups = re.match(r'Par (\d+) (\d*,*\d+).*$', length)
            lengthIdx = 0
            if(lengthGroups == None):
                continue
            for lengthSplit in lengthGroups.groups():
                if(lengthIdx == 0):
                    newCourse.par = locale.atoi(lengthSplit.strip())
                elif lengthIdx == 1:
                    newCourse.length = locale.atoi(lengthSplit.strip())
                lengthIdx+=1
        idx+=1
    return newCourse
