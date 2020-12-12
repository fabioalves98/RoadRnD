#FLOW EXAMPLE

(Client)    - Clink login link
(App)       -/oauth/authorize client_id && redirect_url
(Client)/Web page    - Login with one option
(Client)/Web page   - POST /oauth/login -> login success
(Auth)   - Redirect to the redirect_url with authorization code
(App)       - GET /oauth/token authorization_code && client_id && redirect_url
            - return { 
                        "access_token": access_token,
                        "token_type": "Bearer"
                    }
(Other services) - GET /validate_token/<auth_token>
                 - return 200 - "OK" if token is valid



#EXAMPLE

http://localhost:5005/oauth/authorize?client_id=12345&redirect_url=app

http://localhost:5005/oauth/token?client_id=12345&redirect_url=app&authorization_code=gAAAAABf1OVdE-7MrQY26BaQcp13syVEDv5YV48497UdwZ-RkSjHP7Vi1ILUMMR6UQt9OTC6X1G83708ZPjg5WyFO1AtvNrBBOH1ooAvbJGqt6eag6JJynTFXZOvm4x7K1FdU6LYrD2Y

http://localhost:5005/validate_token/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDc4NzQzMTIsImlhdCI6MTYwNzc4NzkwNywic3ViIjoiMTIzNDUifQ.1dsDNKth7J6hjR7MVhHyQmbDxFbOaoNwLZy7XZ7Gpsg