import requests, re, json, time, random
requests.packages.urllib3.disable_warnings()

# Created by Alex Beals
# Last updated: February 20, 2016

base_url = "https://polldaddy.com/poll/"
redirect = ""

useragents = []
current_useragent = ""

proxies = []
current_proxy = {"http":""}
current_proxy_num = -1


def get_all_useragents():
    f = open("/Users/cladeira/Python/stack/useragent.txt", "r")
    for line in f:
        useragents.append(line.rstrip('\n').rstrip('\r'))
    f.close()
    #print("agent "+ line)

def choose_useragent():
    k = random.randint(0, len(useragents)-1)
    current_useragent = useragents[k]
    print (current_useragent)

def get_all_proxies():
    f = open("/Users/cladeira/Python/stack/proxy.txt", "r")
    for line in f:
        proxies.append(line.rstrip('\n').rstrip('\r'))
    f.close()
    #print("proxy "+ line)

def choose_proxy():
    k = random.randint(0, len(proxies)-1)
    current_num = k
    current_proxy["http"] = proxies[k]


def vote_once(form, value,num):
    c = requests.Session()
    #Chooses useragent randomly
    #choose_useragent()

    k = random.randint(0, len(useragents)-1)
    current_useragent = useragents[k]
    #print (current_useragent)

    redirect = {"Referer": base_url + str(form) + "/", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "User-Agent": current_useragent, "Upgrade-Insecure-Requests":"1", "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "en-US,en;q=0.8"}



    # Chooses proxy randomly
    choose_proxy()
    try:
        #print("URL: "+ base_url + str(form) + "/")
        init = c.get(base_url + str(form) + "/", headers=redirect, verify=False, proxies=current_proxy)
        #f = open("demofile2.txt", "a")
        #print("Headers:\n")
        #print(init.headers)
        cookie = init.headers.get('Set-Cookie')
        cookie = cookie.split(";")[0]
        #print("Cookie: " + cookie)
        #f.write(init.text)
        #f.close()
    except:
        print("error with proxy")
        #proxies.remove(current_proxy_num)
        return None




    # Search for the data-vote JSON object
    data = re.search("data-vote=\"(.*?)\"",init.text).group(1).replace('&quot;','"')
    data = json.loads(data)
    #print(data)
    # Search for the hidden form value
    pz = re.search("type='hidden' name='pz' value='(.*?)'",init.text).group(1)
    # Build the GET url to vote

    #### NEW
    try:
        #send = c.get('https://poll.fm/n/6d338f954f1b6050e0ead034faa53969/11306089?1676744599770')
        #send = c.get('https://poll.fm/n/6d338f954f1b6050e0ead034faa53969/11306089?1676744599772')
        #send = c.get('https://poll.fm/n/6d338f954f1b6050e0ead034faa53969/11306089?1676953872895')
        send = c.get('https://poll.fm/n/6d338f954f1b6050e0ead034faa53969/11306089?'+str(num))
        print('https://poll.fm/n/6d338f954f1b6050e0ead034faa53969/11306089?'+str(num))
        print("Cookie:")
        text = send.text.split(";")[0].split('=')[1].split('\'')[1] 
        print(text)
    except:
        print("Didnt work here!")

    
    request = "https://polls.polldaddy.com/vote-js.php?va=" + str(data['at']) + "&pt=0&r=0&p=" + str(form) + "&a=" + str(value) + "%2C&o=&t=" + str(data['t']) + "&token=" + str(data['n'])+"&n="+text + "&pz="  + str(pz)+"&url=https://notableusa.wordpress.com/illinois-4/"
    #print("REQUEST: ")
    print(request)
    redirect["cookie"]=cookie

    redirect = {"Authority": "polls.polldaddy.fm",
                "method": "GET",
                "path": "/vote-js.php?va=" + str(data['at']) + "&pt=0&r=0&p=" + str(form) + "&a=" + str(value) + "%2C&o=&t=" + str(data['t']) + "&token=" + str(data['n'])+"&n="+text + "&pz=" + str(pz),
                "scheme":"https",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "User-Agent": current_useragent,
                "referer": "https://poll.fm/11306089",
                "Upgrade-Insecure-Requests":"1",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "en-US,en;q=0.8"}
    
    
    #print("HEADER: ")
    #print(redirect)


    

    try:
        send = c.get(request, headers=redirect, verify=False, proxies=current_proxy)
        print("RESULT:")
        #print(send)
        data =send.text
        data = data.find("Thank you, we have already counted your vote")
        print(data)
        #print(send.content)
        #print("already registered" in data)
        #print(send.headers)
        
    except:
        print("error with proxy")
        #proxies.remove(current_proxy_num)
        return None

    return ("revoted" in send.url)

def vote(form, value, times, wait_min = None, wait_max = None):
    global redirect
    # For each voting attempt
    i = 1
    while i < times+1:
        b = vote_once(form, value,i)
        # If successful, print that out, else try waiting for 60 seconds (rate limiting)
        if not b:
            # Randomize timing if set
            if wait_min and wait_max:
                seconds = random.randint(wait_min, wait_max)
            else:
                seconds = 3

            #print "Voted (time number " + str(i) + ")!"
            time.sleep(seconds)
        else:
            print("Locked.  Sleeping for 60 seconds.")
            i-=1
            time.sleep(60)
        i += 1

# Initialize these to the specific form and how often you want to vote
poll_id = 11306089
answer_id = 51566433
number_of_votes = 5000
wait_min = None
wait_max = None

get_all_proxies()
get_all_useragents()
vote(poll_id, answer_id, number_of_votes, wait_min, wait_max)
