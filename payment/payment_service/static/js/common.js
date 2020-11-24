const button = document.getElementById('proceed-button');
button.addEventListener('click', presentPaymentChoicePopup);

async function presentPaymentChoicePopup() {

    const alert = document.createElement('ion-alert');
    alert.setAttribute('mode', 'ios');
    alert.cssClass = 'my-custom-class';
    alert.header = 'Choose the payment method';
    alert.buttons = [
        {
            text: 'Roadnd Funds',
            // cssClass: 'secondary',
            handler: () => {
                // go through
                presentFinalPopup();
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
    alert.buttons = ['OK'];

    document.body.appendChild(alert);
    return alert.present();
}


function gotData(data) {
    var xhr = new XMLHttpRequest();
    var data_json = JSON.stringify(data);
    // TODO: Add payment id to the json here
    xhr.open("POST", '/execute', true);

    // Envia a informação do cabeçalho junto com a requisição.
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () { // Chama a função quando o estado mudar.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // Requisição finalizada. Faça o processamento aqui.
            presentFinalPopup();

        }
    }
    xhr.send(data_json);
}

