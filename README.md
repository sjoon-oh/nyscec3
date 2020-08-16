# Toy Project, NYSCEC3

Project NYSCEC3 is the web-scraping project for YSCEC site, the online-learning site for Yonsei University students.

The NYSCEC and NYSCEC2 are quite alike each other, which use same database MongoDB and share the same purpose. The former project was substituted with this NYSCEC2, since there were some errors on the AWS Lightsail server. The only difference between the two is that NYSCEC uses *Selenium(Firefox)* to scrap the information, while the other just uses simple Python *requests* library to gather information. Both were designed to run on a personal-use server, especially AWS Lightsail. 

NYSCEC3 shares same algorithm, but designed to run using Github Action, a cron scheduler. Since it cannot use database, the previously gathered information is stored under a specific directory in JSON format.

Of course, if you have your personal server, you can run it using cron scheduler.

NYSCEC3 gathers infomation of each course, and notifies using SMTP. The demo is shown below.

<!--more-->

![demo](/demo.jpg)

It is relatively easy to connect **/my** page(logging in) with the browser. The browser automatically generates encrypted parameter **E2** using Javascript, but pure Python script cannot do that. The process will be introduced in detail at the next section. 

The full NYSCEC2 source contains private user ID and passwords, so the source will not be set as open repository. NYSCEC3 does not contain any personal information, thus a user should set some parameters before using. They are, 

- config.py: Your YSCEC ID and password information.
- smtp.py: Your SMTP service ID and password information.


## Requirements

There are three required libraries.

```bash
$ pip3 install requests
$ pip3 install bs4
$ pip3 install pyjsbn-rsa
```

Before running this project, make sure there are no dependency problems between urllib3 and the libraries stated above.

For Github workflow to set the libraries, the **requirements.txt** file should be included in a repository. If you want to use library version or list in your environment, use the command:

```bash
$ pip freeze > requirements.txt
```


## Database

Database must store only data for the course. For instance, the course contains its name, instances, and posts. Instances is the term that was set in the YSCEC response 'class' attribute.

```python
{
    'name': 'course_name', 
    'instance': ['inst1', 'inst2', ...],
    'posts': [
        'QnA, Post title 1',
        'QnA, Post title 2',
        ...
    ]
}
```

NYSCEC3 stores JSON file in a format shown above, and it automatically generates and updates them. If you want to alter the form, then modify *db3.py* file. 

### For NYSCEC2 Tips
This is how to control MongoDB service.

```bash
$ pip install pymongo
```

Commands are listed below:

```bash
$ service mongod start # start db
$ service mongod status # show status
$ service mongod stop # stop db
$ service mongod restart # restart db
```

When accessing to MongoDB console, 

```bash
$ mongo -u username -p 'your_password'
```

When you're new to MongoDB, first create user, in order to control MongoDB with pymongo library.

```bash
$ use admin
$ db.createUser( { user: "username", pwd: "your_password", roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] })
```

Now to add or remove elements from database through console, 

```bash
$ use nyscec
$ db.course_info.find({})
$ db.course_info.remove({}) # remove by giving conditons
$ db.course_info.update({}, {})
$ db.course_info.insert({}) # insert your element

```

# Log In

This section describes the log-in process using *request*. 

## Step 1.
The YSCEC site requires several steps to log in. The first step is to send a cookie to */passni/sso/spLogin.php*.

```python
# Start session
with requests.Session() as s:
    res = s.get(cf.NYSCEC_LOGIN_INDEX)
    # index page

    res = s.post(
        cf.NYSCEC_SPLOGIN, 
        cookies=res.cookies.get_dict())
```

This is the response from the server.

```html
...
<form id="frmSSO" name="frmSSO" method="post" action="https://infra.yonsei.ac.kr/sso/PmSSOService">

...
	<input type="hidden"   id="S1"         name="S1"         value="E34686758B086D4B..." />
	<input type="hidden"   id="loginUrl"   name="loginUrl"   value="https://yscec.yonsei.ac.kr/login/index.php" />
	<input type="hidden"   id="ssoGubun"   name="ssoGubun"   value="Login" />
	<input type="hidden"   id="refererUrl" name="refererUrl" value="https://yscec.yonsei.ac.kr/login/index.php" />
</form>
...
```

The response from the URI *passni/sso/spLogin.php* gives us the page with S1 parameter hard-coded in the hidden input. The response should be parsed to get the value. To prepare request payload, BeautifulSoup4 library was used. 

```python
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
```

## Step 2.

With the parameter prepared, it should be sent to */sso/PmSSOService*. 

```python
    res = s.post(
        cf.NYSCEC_PMSSO_SERVICE, 
        request_payload)
```

The response from */sso/PmSSOService* is looks like this:

```html
...
<form id="ssoLoginForm" name="ssoLoginForm" method="post" action="https://yscec.yonsei.ac.kr/login/index.php">
	<input type="hidden" id="app_id"       name="app_id"        value="yscec" />
	<input type="hidden" id="retUrl"       name="retUrl"        value="https://yscec.yonsei.ac.kr" />
	<input type="hidden" id="failUrl"      name="failUrl"       value="https://yscec.yonsei.ac.kr/login/index.php" />
	<input type="hidden" id="baseUrl"      name="baseUrl"       value="https://yscec.yonsei.ac.kr" />
	<input type="hidden" id="loginUrl"     name="loginUrl"      value="https://yscec.yonsei.ac.kr/login/index.php" />
	<input type="hidden" id="ssoChallenge" name="ssoChallenge"  value="740B4482B9..." />
	<input type="hidden" id="loginType"    name="loginType"     value="invokeID" />
	
	<input type="hidden" id="returnCode"    name="returnCode"     value="" />
	<input type="hidden" id="returnMessage" name="returnMessage"  value="" />
	
	<input type="hidden" id="keyModulus"    name="keyModulus"     value="bed5a9620e8d3e2e54..." />
	<input type="hidden" id="keyExponent"   name="keyExponent"    value="10001" />
	
	
	<input type="hidden" id="ssoGubun" name="ssoGubun" value="Login" />
	
	<input type="hidden" id="refererUrl" name="refererUrl" value="https://yscec.yonsei.ac.kr/login/index.php" />
</form>
...

```

These are the parameters that should be conveyed to the next request. The parameter *ssoChallenge* changes at every request. The other important ones like *keyModulus* and *keyExponent* seem to have the same value, but please check again at your browser before implementing the code below. Again, prepare *request_payload* and make the next request.


```python
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
```

As it can be assumed, the *keyModulus* and *keyExponent* should be stored for the next step, since YSCEC gives us Javascript code to generate encrypted text using a user's ID and password. 


## Step 3. 

The request should be made for index page, again.

```python
    res = s.post(
        cf.NYSCEC_LOGIN_INDEX, 
        request_payload
        )
```

The response looks like this:

```html
...
<form id="ssoLoginForm" name="ssoLoginForm" method="post" action="https://infra.yonsei.ac.kr/sso/PmSSOAuthService" onsubmit="return fSubmitSSOLoginForm(this);">
    <input type="hidden" id="app_id"       name="app_id"        value="yscec" />
    <input type="hidden" id="retUrl"       name="retUrl"        value="https://yscec.yonsei.ac.kr" />
    <input type="hidden" id="failUrl"      name="failUrl"       value="https://yscec.yonsei.ac.kr/login/index.php" />
    <input type="hidden" id="baseUrl"      name="baseUrl"       value="https://yscec.yonsei.ac.kr" />
    <input type="hidden" id="loginUrl"     name="loginUrl"      value="https://yscec.yonsei.ac.kr/login/index.php" />
    <input type="hidden" id="loginType"    name="loginType"     value="invokeID" />
    <input type="hidden" id="ssoGubun"           name="ssoGubun"            value="Login" />
    <input type="hidden" id="refererUrl"    name="refererUrl"     value="https://yscec.yonsei.ac.kr/login/index.php" />
    <input type="hidden" id="E2"           name="E2"            value="" />
    ...
```

We need *E2* parameter for the next request, but the value is empty. The *E2* is generated at the browser using Javascript function:

```javascript
function fSubmitSSOLoginForm(){

    var username = $('#username').val();
    var password = $('#password').val();
		
    if(username == ''){
        alert( "사용자 아이디를 입력하여 주십시요." );
        $('#username').focus();
        return false;
    }

    if(password == ''){
        alert( "비밀번호를 입력하여 주십시요." );
        $('#password').focus();
        return false;
    }
			
    var ssoChallenge= '740B4482B91B41...'; // This provided.

    var jsonObj = {'userid':username, 'userpw':password, 'ssoChallenge':ssoChallenge};
    var jsonStr = Object.toJSON( jsonObj );

    var rsa = new RSAKey();
    rsa.setPublic( 'bed5a9620e8...', '10001' );
    // These parameter, modulus and exponent was provided.

    document.ssoLoginForm.E2.value = rsa.encrypt( jsonStr );
    return true;
}
```

To generate E2, **pyjsbn** library was used for implementing RSA algorithm. The library shares similar interface with *jsbn*.


```python
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
```

Again, prepare the third *request_payload*, with *E2*. At this stage, a user's ID and password should also be provided in the parameter.

```python
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
```

## Step 4. 

The request should sent to */sso/PmSSOAuthService* this time.

```python
    res = s.post(
        cf.NYSCEC_PMSSOAUTH_SERVICE, 
        request_payload)
```

Then, the response contains another necessary parameters: *E3*, *E4*, *S2* and *CLTID*.

```html
<form id="ssoLoginForm" name="ssoLoginForm" method="post" action="https://yscec.yonsei.ac.kr/passni/sso/spLoginData.php">
	<input type="hidden" id="app_id"   name="app_id"   value="yscec" />
	<input type="hidden" id="retUrl"   name="retUrl"   value="https://yscec.yonsei.ac.kr" />
	<input type="hidden" id="failUrl"  name="failUrl"  value="https://yscec.yonsei.ac.kr/login/index.php" />
	<input type="hidden" id="baseUrl"  name="baseUrl"  value="https://yscec.yonsei.ac.kr" />
	<input type="hidden" id="loginUrl" name="loginUrl" value="https://yscec.yonsei.ac.kr/login/index.php" />
	
	<input type="hidden" id="E3"       name="E3"       value="55C8861F176FC..." />
	<input type="hidden" id="E4"       name="E4"       value="A2951418D85BF..." />
	<input type="hidden" id="S2"       name="S2"       value="17E901A3FF4B6..." />
	
	<input type="hidden" id="CLTID"    name="CLTID"    value="50A45BF3F8E1A9E881F30E4C9F8B" />
	
    <input type="hidden" id="ssoGubun" name="ssoGubun" value="Login" />
	
    <input type="hidden" id="refererUrl" name="refererUrl" value="https://yscec.yonsei.ac.kr/login/index.php" />
	
    <input type="hidden" id="username" name="username" value="your_student_id" />
	
    <input type="hidden" id="password" name="password" value="your_password" />
	
</form>
```

Again, prepare for the next *request_payload*:

```python
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
```

This is the final parameter for log-in process. After sending parameters to */passni/sso/spLoginData.php*, make one more request before getting into the main YSCEC page.

```python
    res = s.post(
        cf.NYSCEC_SPLOGIN_DATA,
        request_payload)

    res = s.get(cf.NYSCEC_SPLOGIN_PROCESS)
    # /passni/spLoginProcess.php
```

## Step 6.

After sending all of the parameters, make a request for the main page, */my*.

```python
    res = s.get(cf.NYSCEC_MY)
    # https://yscec.yonsei.ac.kr/my/
```

This will show your main page. Happy scraping!


## Update logs

2020.07.31. <b>Version: 0.1.0va</b>
- NYSCEC initiated, author(SukJoon Oh, acoustikue)

2020.08.
- Project updated to NYSCEC2.

2020.08.15.
- Altered some codes for NYSCEC3.
