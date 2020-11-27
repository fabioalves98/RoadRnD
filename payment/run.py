  
from payment_service import getAppContext

app = getAppContext()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)