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

http://localhost:5005/oauth/authorize?client_id=RoadRnD&redirect_url=http://www.roadrnd.com

Local Storage items:

localStorage.getItem("user_name");
localStorage.getItem("client_id");
localStorage.getItem("auth_code");
localStorage.getItem("image");
localStorage.getItem("mail");


http://localhost:5005/oauth/token?client_id=RoadRnD&redirect_url=http://www.roadrnd.com&authorization_code=gAAAAABf3j8tsk2J077ZI4yj3xCpZTcIvTbNn8lr7MjFujK9Sg5suLLEtIDw-DYeNaCLpGJDWp3ScD10Ys1j2gvpTmEcP2W0v3-grmL0t-gDSFw0GEjR2eCLd2ApDhk9_NgfZe2nrAKeuwjDeTLYIeWq3C9k32pR3FZHLmrGqC8UD7g5UpIwwyLASaxJC9Q9OPyzk1zXt_BB

http://localhost:5005/validate_token/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDg0ODcxMTMsImlhdCI6MTYwODQwMDcwOCwic3ViIjoiUm9hZFJuRCJ9.ZaxTIGnIl9CUqRazFMoWVgV7alLWBK9HVtHEBA3C8kA