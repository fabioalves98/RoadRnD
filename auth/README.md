## FLOW EXAMPLE

(Client)    - Clink login link
(App)       -/oauth/authorize client_id && redirect_url
(Client)/Web page    - Login with one option
(Client)/Web page   - POST /oauth/login -> login success
(Auth) - Ask client to close the browser
<!-- (Auth)   - Redirect to the redirect_url with authorization code and user information -->
(App)       - GET /credentialsS
(App)       - GET /oauth/token authorization_code && client_id && redirect_url
            - return { 
                        "access_token": access_token,
                        "token_type": "Bearer"
                    }
(Other services) - GET /validate_token/<auth_token>
                 - return 200 - "OK" if token is valid



## EndPoints

### /oauth/authorize

http://localhost:5005/oauth/authorize?client_id=RoadRnD&redirect_url=http://www.roadrnd.com&user_key=D1234D

### /oauth/credentials

http://localhost:5005/oauth/credentials?user_key=D1234D

[
    {
        "auth_code":"gAAAAABf7f3lBZWoVTg31iwNjgzs5snK_1xHorVX4q8opKJGkuRbFK-v9rEtZwRlEOOWlwiz8JUEcDIheJ6KO-FCNkB_iiYr1RQCRUwCSeN3IXSRBVWww8-a3VHsW9sjPt1uE-UACtiso28_nDz-D85TkJJW4iImOdmzYZf_6-1eKi-U7GicXRQES9GsT7qEymZSnsTuRnrwKgk-KC-zpSyI5WAVQLomrg==", 
        "client_id": "110007873131418394975", 
        "image": "https://lh4.googleusercontent.com/-4ihUeHpLb2U/AAAAAAAAAAI/AAAAAAAAAAA/AMZuucmYx9NLZ64YoQp5ikkFfmenUd2bag/s96-c/photo.jpg", 
        "mail": "diogocostamarques98@gmail.com", 
        "user_key": "D1234D", 
        "user_name": "Diogo Marques"
    }
]


Local Storage items:

localStorage.getItem("user_name");
localStorage.getItem("client_id");
localStorage.getItem("auth_code");
localStorage.getItem("image");
localStorage.getItem("mail");

### /oauth/token

http://localhost:5005/oauth/token?client_id=RoadRnD&redirect_url=http://www.roadrnd.com&authorization_code=gAAAAABf-xOVbBizBBaSk41yOZcx_C4NLf5SrETAy5xqPzfK7BwDStqdrlITG3z5wVOVexhqoFqwUowrgrsmrXeD3sW9TCZ6vpe_0SBZg66PopHA_5hAjEGurIpuI_ejckAgVsNpz9lKOpZqaP3MTl8Ey9IsusGZSdQtwSS1sEIixIuVp0RY3uikjCPH0qJRC8THKJBsS_ChYT54cOF4VaB_kbz5nC4QEA==

### /validate_token/<access_token>

http://localhost:5005/validate_token/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDk1MTc5MjUsImlhdCI6MTYwOTQzMTUyMCwic3ViIjoiUm9hZFJuRCJ9.GofTGLvnm6iz-lBO9y6XoIyfSh13vgrUgjNaI9OSuKk