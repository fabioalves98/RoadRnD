#FLOW EXAMPLE

(Client)    - Clink login link
(App)       -/oauth/authorize client_id && redirect_url
(Client)/Web page    - Login with one option
(Client)/Web page   - POST /oauth/login -> login success
(Auth)   - Redirect to the redirect_url with authorization code and user information
(App)       - GET /oauth/token authorization_code && client_id && redirect_url
            - return { 
                        "access_token": access_token,
                        "token_type": "Bearer"
                    }
(Other services) - GET /validate_token/<auth_token>
                 - return 200 - "OK" if token is valid



#EXAMPLE

http://localhost:5005/oauth/authorize?client_id=RoadRnD&redirect_url=http://www.roadrnd.com&user_key=D1234D

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


http://localhost:5005/oauth/token?client_id=RoadRnD&redirect_url=http://www.roadrnd.com&authorization_code=gAAAAABf7fnCIE-sDXX1jJAvuXOspilhSaytU-m4j7bzGShX0bvgEDLESJ6-cs8WFxxc_KhYaI4N7RpE_tNp0RSHbKpPjUsqobvkzyY92L5SbtzXjTHqaYUaq-0crn72oLHQdgCKncfQcyjpa0lTpcrazacHo6SutAsuL0wixJzNlU0uZ2M5Fd0JK2QekvVbq0_xVaf33jQNoFY9jflkV9M-GzNO8KT7Jg==

http://localhost:5005/validate_token/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDk1MTc5MjUsImlhdCI6MTYwOTQzMTUyMCwic3ViIjoiUm9hZFJuRCJ9.GofTGLvnm6iz-lBO9y6XoIyfSh13vgrUgjNaI9OSuKk