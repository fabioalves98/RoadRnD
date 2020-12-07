#FLOW EXAMPLE

(Client)    - Clink login link
(App)       - GET /oauth/authorize client_id && redirect_url -> return html page with facebook and google  buttons
(Client)    - Login with one option
(Client)    - POST /oauth/login -> login success
(Service)   - Redirect o redirect_url with authorization code
(App)       - GET /oauth/token authorization_code && client_id && redirect_url
            - return { 
                        "access_token": access_token,
                        "token_type": "Bearer"
                    }