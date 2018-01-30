import time

from selenium import webdriver

driver = webdriver.Chrome()

urlFile = open('urls.txt')
error_file = open("Errors.txt", "w")
profile_data = open("ProfileData.txt", "w")

baseURL = "https://discussions.udacity.com/c/standalone-courses/ud851-emea/l/new/"
driver.get(baseURL)
time.sleep(1) 

username=driver.find_element_by_id("email")
username.send_keys("YourEmail")
pwd=driver.find_element_by_id("password")
pwd.send_keys("YourPassword\n")
time.sleep(9)


profileStr = "link;username;fullname;joinDate;views;trustLevel;topicsViewed;postsRead;given;topicsCreated;postsCreated;received"
profile_data.write(profileStr+'\n')

j=0
for ll in urlFile:
    
    print("----------------------")
    l1=ll[0:-1]
    print(l1)
    if(l1.find("discobot")>-1):
        continue
    j+=1 
    try:
        driver.get(l1)
        time.sleep(2) 
        username= driver.find_element_by_class_name("username").text 
        print("username: "+username)
        fullname= driver.find_element_by_class_name("full-name").text 
        print("fullname: "+fullname)
            
    #get join date
        secondary = driver.find_element_by_class_name("secondary")
        htmlT = secondary.get_attribute('innerHTML')
        pos = str(htmlT).find("<span class=\"relative-date date\"")
        joinDate = ""
        if(pos>-1):
            s2 = str(htmlT)[pos+40:-1]
            s2=s2.strip()
            pos2 = s2.find("data-time")
            joinDate = s2[:pos2-2].strip()
        print("joinDate: "+joinDate)
   #get views
        pos = str(htmlT).find("<dt>Views</dt>")
        views = ""
        if(pos>-1):
            s2 = str(htmlT)[pos+18:-1]
            s2=s2.strip()
            pos2 = s2.find("</dd>")
            views = s2[:pos2].strip()
        
        print("views: "+views)
    #get trust level
        pos = str(htmlT).find("<dd class=\"trust-level\">")
        trustLevel = ""
        if(pos>-1):
            s2 = str(htmlT)[pos+24:-1]
            s2=s2.strip()
            pos2 = s2.find("</dd>")
            trustLevel = s2[:pos2].strip()
        print("trustLevel: "+trustLevel)
        topicsViewedId = 0
        postsReadId=0
        givenId = 0
        topicsCreatedId = 0
        postsCreatedId = 0
        receivedId = 0
        
    # get stats        
        elems = driver.find_elements_by_class_name("label")
        i=0
        for elem in elems:
            link1 = str(elem.text)
            if(link1.find("topics viewed")>-1):
                topicsViewedId=i
            if(link1.find("posts read")>-1):
                postsReadId=i
            if(link1.find("given")>-1):
                givenId=i
            if(link1.find("topics created")>-1):
                topicsCreatedId=i
            if(link1.find("posts created")>-1):
                postsCreatedId=i
            if(link1.find("received")>-1):
                receivedId=i
            i+=1
            
        i=0
        topicsViewed = ""
        postsRead=""
        given =""
        topicsCreated = ""
        postsCreated = ""
        received = ""
    
        elems = driver.find_elements_by_class_name("value")
        for elem in elems:
            link1 = str(elem.text)
            if(i==topicsViewedId):
                e2 = elem.find_element_by_class_name("number").get_attribute('title')   
                topicsViewed=e2
                if(str(e2).strip()==""):
                    topicsViewed=link1
    
            if(i==postsReadId):
                try:
                    e2 = elem.find_element_by_class_name("number").get_attribute('title')   
                    postsRead=e2
                    if(str(e2).strip()==""):
                        postsRead=link1
                    
                except:    
                    postsRead=link1
                    
            if(i==givenId):
                try:
                    e2 = elem.find_element_by_class_name("number").get_attribute('title')   
                    given=e2
                    if(str(e2).strip()==""):
                        given=link1
                except:    
                    given=link1
    
            if(i==topicsCreatedId):
                try:
                    e2 = elem.find_element_by_class_name("number").get_attribute('title')   
                    topicsCreated=e2
                    if(str(e2).strip()==""):
                        topicsCreated=link1
                except:    
                    topicsCreated=link1
            if(i==postsCreatedId):
                try:
                    e2 = elem.find_element_by_class_name("number").get_attribute('title')   
                    postsCreated=e2
                    if(str(e2).strip()==""):
                        postsCreated=link1
                except:    
                    postsCreated=link1
            if(i==receivedId):
                try:
                    e2 = elem.find_element_by_class_name("number").get_attribute('title')   
                    received=e2
                    if(str(e2).strip()==""):
                        received=link1
                except:    
                    received=link1
            i+=1
    
        print("topicsViewed: " +topicsViewed)
        print("postsRead: " +postsRead)
        print("given: " +given)
        print("topicsCreated: " +topicsCreated)
        print("postsCreated: " +postsCreated)
        print("received: " +received)
        
        
        profileStr = l1 + ';'+username + ';'+fullname + ';'+joinDate + ';'+views + ';'+trustLevel + \
        ';'+topicsViewed + ';'+postsRead + ';'+given + ';'+topicsCreated + ';'+postsCreated + ';'+received + '\n'
        profileStr=profileStr.replace("\n"," ")
        profileStr=profileStr.replace("\r"," ")
        profile_data.write(profileStr+'\n')
    except:
       error_file.write(l1+'\n')
       


urlFile.close()
profile_data.close()
error_file.close()



