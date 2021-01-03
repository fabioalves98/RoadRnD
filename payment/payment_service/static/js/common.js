var pay_id_url = window.location.pathname.split("/");
var payment_id = pay_id_url.pop() || pay_id_url.pop();
console.log(payment_id);
localStorage.setItem("payment_id", payment_id);

const button = document.getElementById('proceed-button');
button.addEventListener('click', presentPaymentChoicePopup);


const button_prof = document.getElementById('profile-button');
button_prof.addEventListener('click', gotoProfile);

async function gotoProfile(){
    let client_id = document.getElementById('client-id').innerHTML;
    window.location.pathname = "/profile/" + client_id;
}



async function presentPaymentChoicePopup() {

    const alert = document.createElement('ion-alert');
    alert.setAttribute('mode', 'ios');
    alert.cssClass = 'my-custom-class';
    alert.header = 'Choose the payment method';
    alert.buttons = [
        {
            text: 'RoadRnd Funds',
            // cssClass: 'secondary',
            handler: () => {
                // go through
                gotDataFunds();
            }
        }, {
            text: 'MasterCard',
            handler: () => {
                // Present credit  card alert
                presentCreditCardPopup();
            }
        },
        {
            text: 'Cancel',
            handler: () => {
                // alert("Payment method = Card")
            }
        }
    ];


    document.body.appendChild(alert);
    await alert.present();
}

function presentCreditCardPopup() {
    const alert = document.createElement('ion-alert');
    alert.cssClass = 'my-custom-class';
    alert.setAttribute('mode', 'ios');
    alert.header = 'Insert your credit card information';
    alert.inputs = [
        {
            placeholder: 'Name',
            name: "name"
        },
        {

            placeholder: 'Card number',
            name: "card-number"
        },
        {
            placeholder: 'Expiration date',
            type: 'date',
            name: "expiration-date"
        },
        // input date without min nor max

        {
            placeholder: 'CCV',
            name: "ccv"
        },
    ];
    alert.buttons = [
        {
            text: 'Cancel',
            // cssClass: 'secondary',
            handler: () => {
                // Just close
            }
        },
        {
            text: 'Confirm',
            type: "submit",
            handler: (data) => {
                // Send info to server
                gotData(data);

            }
        }
    ];

    document.body.appendChild(alert);
    return alert.present();
}

function presentFinalPopup() {
    const alert = document.createElement('ion-alert');
    alert.cssClass = 'my-custom-class';
    alert.setAttribute('mode', 'ios');
    alert.header = 'Payment complete!';
    alert.subHeader = 'Your payment was successful and you will soon be redirected';
    // alert.message = 'This is an alert message.';
    alert.buttons = [{text: 'OK', handler: () => {
        console.log("here");
        finishPayment();
    }
    }];

    document.body.appendChild(alert);
    return alert.present();
}

function presentErrorPopup() {
    const alert = document.createElement('ion-alert');
    alert.setAttribute('mode', 'ios');
    alert.header = 'Something went wrong, please try again.';
    alert.subHeader = 'An error occured during the payment. Please try again later or contact us for more information!';
    // alert.message = 'This is an alert message.';
    alert.buttons = [{text: 'Confirm', handler: () => {
        console.log("here");
        finishPayment();
    }
    }];

    document.body.appendChild(alert);
    return alert.present();
}


function gotData(data) {
    var xhr = new XMLHttpRequest();
    var pay_id_url = window.location.pathname.split("/");
    var payment_id = pay_id_url.pop() || pay_id_url.pop()
    data.payment_id = payment_id;
    var data_json = JSON.stringify(data);
    xhr.open("POST", '/execute', true);

    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () { 
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            presentFinalPopup();
        }else if(this.readyState === XMLHttpRequest.DONE && this.status === 500){
            console.log(xhr.responseText);
            presentErrorPopup();
        }
    }
    xhr.send(data_json);
}

function finishPayment(){
    // var xhr = new XMLHttpRequest();
    var pay_id_url = window.location.pathname.split("/");
    var payment_id = pay_id_url.pop() || pay_id_url.pop()
    // xhr.open("GET", '/finish', true);
    // xhr.setRequestHeader("Content-Type", "application/json");
    // xhr.onreadystatechange = function () { 
    //     if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
    //         console.log("called");
    //     }else if(this.readyState === XMLHttpRequest.DONE && this.status === 500){
    //         console.log("called, error");
    //     }
    // }
    // xhr.send();
    window.location.pathname = "/finish/" + payment_id ;

}

function gotDataFunds() {
    var xhr = new XMLHttpRequest();
    var pay_id_url = window.location.pathname.split("/");
    var payment_id = pay_id_url.pop() || pay_id_url.pop()
    var data = {access_token: "xx", payment_id: payment_id }
    var data_json = JSON.stringify(data);
    console.log(data_json)
    xhr.open("POST", '/execute', true);

    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () { 
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            presentFinalPopup();
        }else if(this.readyState === XMLHttpRequest.DONE && this.status === 500){
            console.log(xhr.responseText);
            presentErrorPopup();
        }
    }
    xhr.send(data_json);
}


