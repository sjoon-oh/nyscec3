# [Toy Project NYSCEC]
# 0.1.2va, 20.07.31. First launched.
# written by acoustikue(SukJoon Oh)
#                                 __  _ __            
#    ____ __________  __  _______/ /_(_) /____  _____ 
#   / __ `/ ___/ __ \/ / / / ___/ __/ / //_/ / / / _ \
#  / /_/ / /__/ /_/ / /_/ (__  ) /_/ / ,< / /_/ /  __/
#  \__,_/\___/\____/\__,_/____/\__/_/_/|_|\__,_/\___/ 
#                                                     
# Visual Studio Code
# 
# Legal stuff:
#   This simple code follows MIT license. 
# 
# MIT License
# Copyright (c) 2020 SukJoon Oh(acoustikue)

import requests
from bs4 import BeautifulSoup # parser
import json

# 
# user defined
import config as cf
import log
#import db
import db3

import stmp as mail


# outside of the scope
course_info = []

# Start session
with requests.Session() as s:

    #
    # Step 1. Generate cookie.
    res = s.get(cf.NYSCEC_LOGIN_INDEX) 

    #
    # Step 2. Use cookie to get S1 parameter
    res = s.post(
        cf.NYSCEC_SPLOGIN, 
        cookies=res.cookies.get_dict())

    #
    # Step 3. Request keyModulus and key Exponent
    soup = BeautifulSoup(res.text, 'html.parser')
    request_payload = {
        "app_id": "yscec",
        "retUrl": cf.NYSCEC_BASE,
        "failUrl": cf.NYSCEC_LOGIN_INDEX,
        "baseUrl": cf.NYSCEC_BASE,
        "S1": str(soup.find('input', id='S1').get('value')),
        "loginUrl": cf.NYSCEC_LOGIN_INDEX,
        "ssoGubun": "Login",
        "refererUrl": cf.NYSCEC_LOGIN_INDEX
    }

    res = s.post(
        cf.NYSCEC_PMSSO_SERVICE, 
        request_payload)

    #
    # Step 4. Second reqeust to index page
    del soup
    soup = BeautifulSoup(res.text, 'html.parser')
    
    request_payload = {
        "app_id": "yscec",
        "retUrl": cf.NYSCEC_BASE,
        "failUrl": cf.NYSCEC_LOGIN_INDEX,
        "baseUrl": cf.NYSCEC_BASE,
        "loginUrl": cf.NYSCEC_LOGIN_INDEX,
        "ssoChallenge": str(soup.find('input', id='ssoChallenge').get('value')),
        "loginType": str(soup.find('input', id='loginType').get('value')),
        "returnCode": str(soup.find('input', id='returnCode').get('value')),
        "returnMessage": str(soup.find('input', id='returnMessage').get('value')),
        "keyModulus": str(soup.find('input', id='keyModulus').get('value')),
        "keyExponent": str(soup.find('input', id='keyExponent').get('value')),
        "ssoGubun": "Login",
        "refererUrl": cf.NYSCEC_LOGIN_INDEX
    }

    # POST, /index.php
    res = s.post(
        cf.NYSCEC_LOGIN_INDEX, 
        request_payload
        )

    #
    # Step 5. Extract sessKey and Generate E2.
    #   This is the translation of client javascript
    # pip install pyjsbn-rsa
    del soup
    soup = BeautifulSoup(res.text, 'html.parser')

    # find sesskey parameter
    import re
    match = re.findall(r'"sesskey":"(.*?)"', str(soup.find('script', type='text/javascript')))

    # Generate E2 value
    jsonObj = {
        'userid': cf.NYSCEC_LOGIN_PARAM['username'], 
        'userpw': cf.NYSCEC_LOGIN_PARAM['password'], 
        'ssoChallenge': request_payload['ssoChallenge']
        }

    from jsbn import RSAKey
    rsa = RSAKey()
    rsa.setPublic(
        request_payload['keyModulus'],
        request_payload['keyExponent']
        )

    E2 = rsa.encrypt(json.dumps(jsonObj))
    
    request_payload = {
        "app_id": "yscec",
        "retUrl": cf.NYSCEC_BASE,
        "failUrl": cf.NYSCEC_LOGIN_INDEX,
        "baseUrl": cf.NYSCEC_BASE,
        "loginUrl": cf.NYSCEC_LOGIN_INDEX,
        "loginType": "invokeID",
        "ssoGubun": "Login",
        "refererUrl": cf.NYSCEC_LOGIN_INDEX,
        "E2": E2,
        "username": cf.NYSCEC_LOGIN_PARAM['username'],
        "password": cf.NYSCEC_LOGIN_PARAM['password']
    }   

    res = s.post(
        'https://yscec.yonsei.ac.kr/lib/ajax/service.php?sesskey={0}&info=core_fetch_notifications'.format(match), 
        json='[{\"index\": 0, \"methodname\": \"core_fetch_notifications\", \"args\": {\"contextid\": 1}}]'
        # "[{\"index\": 0, \"methodname\": \"core_fetch_notifications\", \"args\": {\"contextid\": 1}}]"
        )    
    res = s.post(
        cf.NYSCEC_PMSSOAUTH_SERVICE, 
        request_payload)

    #
    # Step 6. Find E3, E4, S2, CLTID
    del soup
    soup = BeautifulSoup(res.text, 'html.parser')

    request_payload = {
        "app_id": "yscec",
        "retUrl": cf.NYSCEC_BASE,
        "failUrl": cf.NYSCEC_LOGIN_INDEX,
        "baseUrl": cf.NYSCEC_BASE,
        "loginUrl": cf.NYSCEC_LOGIN_INDEX,
        "E3": str(soup.find('input', id='E3').get('value')),
        "E4": str(soup.find('input', id='E4').get('value')),
        "S2": str(soup.find('input', id='S2').get('value')),
        "CLTID": str(soup.find('input', id='CLTID').get('value')),
        "refererUrl": cf.NYSCEC_LOGIN_INDEX,
        "username": cf.NYSCEC_LOGIN_PARAM['username'],
        "password": cf.NYSCEC_LOGIN_PARAM['password']
    }

    res = s.post(
        cf.NYSCEC_SPLOGIN_DATA,
        request_payload)
    res = s.get(cf.NYSCEC_SPLOGIN_PROCESS)
    res = s.get(cf.NYSCEC_MY)
    
    del request_payload
    del E2
    del match

    #
    # Login process finished

    #
    # parsing process

    # Gather hrefs to visit
    del soup
    soup = BeautifulSoup(res.text, 'html.parser')
    soup = BeautifulSoup(str(soup.findAll("h2", {"class": "title"})), 'html.parser')

    for course in soup.findAll('a'):
        course_info.append(
            {
                'name': course.attrs['title'],
                'base_href': course.attrs['href'], # delete
                'instances': [],
                'forum': [], # delete
                'posts': []
            }
        )

    # Gather instances and sub hrefs for each course    
    for course in course_info:
        res = s.get(course['base_href']) # base href
        soup = BeautifulSoup(res.text, 'html.parser')

        post_forum = soup.findAll("div", {"class": "activityinstance"})

        for instance in post_forum:
            if instance in course['instances']: pass
            else:
                course['instances'].append(instance.text)                
                sub_href = BeautifulSoup(
                        str(instance), 'html.parser'
                    ).find('a', class_="").attrs['href']

                if cf.NYSCEC_INSTANCE_TYPE_1[0] in sub_href:
                    course['forum'].append({'name': instance.text, 'href': sub_href})
                
                del sub_href

        del post_forum
        del course['base_href']

    #
    # Gather sub-forums' links
    for course in course_info:
        for forum in course['forum']:
            res = s.get(forum['href']) # Visit a forum
            
            soup = BeautifulSoup(res.text, 'html.parser')
            soup = BeautifulSoup(
                str(soup.findAll("h1", {"class": "thread-post-title"})), 'html.parser')

            # Update to course['posts']
            for post in soup.findAll("a", {}):
                form = '[{0}] {1}'.format(forum['name'], post.text)
                if form in course['posts']: pass
                else:
                    course['posts'].append(form)
                del form
                
            # scrap only titles.
            # does not need to show all the details, 
            # since the newly updated ones will always be right at the top.

            # https://yscec.yonsei.ac.kr/mod/jinotechboard/view.php?id=1554258
            # For test
        del course['forum']
            
    # End of fetch
    del soup
    del res

#
# Query
updated_info = []

for target in course_info:
    new = db3.generate_notification_item(target)

    if new != None:
        updated_info.append(new)

    del new
del course_info


if len(updated_info) != 0:
    mail.send_mail('New updates.', 'New updates.', updated_info)
