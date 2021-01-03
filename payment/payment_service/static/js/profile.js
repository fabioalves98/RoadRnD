const button_prof = document.getElementById('back-button');
button_prof.addEventListener('click', gotoPayment);
console.log(localStorage.getItem("payment_id"));
async function gotoPayment(){
    // let client_id = document.getElementById('client-id').innerHTML;
    let payment_id = localStorage.getItem("payment_id");
    console.log(payment_id);
    window.location.pathname = "/approve/" + payment_id;
}