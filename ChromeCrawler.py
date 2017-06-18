import platform, sqlite3 ,getpass, psutil ,datetime

def fixDate(timestamp):
    #Chrome stores timestamps in the number of microseconds since Jan 1 1601.
    #To convert, we create a datetime object for Jan 1 1601...
    epoch_start = datetime.datetime(1601,1,1)
    #create an object for the number of microseconds in the timestamp
    delta = datetime.timedelta(microseconds=int(timestamp))
    #and return the sum of the two.
    return epoch_start + delta

def connect_db(type):

    print type
    username = getpass.getuser()
    if type.lower() == 'Linux'.lower():
        path = '/home/' + username + '/.config/google-chrome/Default/History/'
    elif type.lower() == 'Windows'.lower():
        path =  'C:\\Users\\' + username + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
    elif type.lower() == 'Darwin'.lower():
        path  = '/Users/' + username + '/Library/Application Support/Google/Chrome/Default/History'
    print path
    selectStatement = 'SELECT urls.url, urls.visit_count FROM urls;'
    selectTime = 'SELECT visits.visit_time FROM visits;'
    querystat = 'SELECT visits.visit_time, visits.visit_duration, urls.url , urls.visit_count FROM visits, urls WHERE visits.url=urls.id;'
    c = sqlite3.connect(path)
    for row in c.execute(querystat):
        if 'youtube' in row[2] and row[1] != 0:
            print "url:" +  str(row[2])
            print "visit_time:" + str((row[0]))
            print "visit_duration:" + str((row[1]))
            print "visit_count:" + str(row[3])

def platform_type():
    type = platform.system()
    print type
    PROCNAME = 'Google Chrome'
    for proc1 in psutil.process_iter():
        try:
            if proc1.name() == PROCNAME:
                print 'found'
                proc1.kill()
        except:
            print 'failed to find the chrome maybe its closed or psutils fails'
            pass
    connect_db(type)


if __name__ == "__main__":
    platform_type()




