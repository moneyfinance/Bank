let signup = document.querySelector(".signup");
let login = document.querySelector(".login");
let slider = document.querySelector(".slider");
let formSection = document.querySelector(".form-section");
var first = true;
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
// let sendOtpButton = document.querySelector(".clkbtn");
// const upbtn = document.querySelector("#upbtn");
// upbtn.addEventListener("click", verify_register);
// let otpInputs = document.querySelectorAll(".otp-inputs");
//alok123
//@Alok123

async function verify_register() {

    const sendOtpButton = document.querySelector("#upbtn");
    const otpInputs = document.querySelector(".otp-inputs");
    const phoneNumberInput = document.getElementById("phn_no");
    const errorfeild = document.getElementById("error_feild");
    const fnameInput = document.getElementById("fname").value;
    const lnameInput = document.getElementById("lname").value;
    const otp1Input = document.getElementById("otp1").value;
    // const otp2Input = document.getElementById("otp2").value;
    // const otp3Input = document.getElementById("otp3").value;
    // const otp4Input = document.getElementById("otp4").value;
    const phone_number = phoneNumberInput.value.trim();
    if(fnameInput === ""){
        errorfeild.textContent = "Enter Your First Name";
        return ;
    }
    if(lnameInput === ""){
        lnameInput = "";
    }
    if (/^\d{10}$/.test(phone_number)) {
        // Do something with the valid phone number
    } else {
        errorfeild.textContent = "Enter valid 10 digit mobile number";
        phoneNumberInput.focus();
        return;
    }
    // if(phone_number === ""){
    //     errorfeild.textContent = "Enter Mobile Number";
    //     return ;
    // }
    // alert(phone_number.length);
    // if(phone_number.length > 10 || phone_number.length < 10){
    //     errorfeild.textContent = "Enter valid 10 digi mobile number";
    //     return;
    // }
    // alert(phone_number)

    // Make API call to send OTP and handle response
    if(first){
        try {
            const response = await fetch("http://127.0.0.1:8000/send_otp/", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken 
                    },
                    body: JSON.stringify({
                        phone_number: phone_number,
                        // Add other data you want to send
                    }),
                // ... Add required headers and data for sending OTP
            });

            if (response.status === 200) {
                errorfeild.textContent = "Otp send Successfullly";
                sendOtpButton.textContent = "Register"; // Change button text
                otpInputs.style.display = "inline-block";
                first = false;
            } else {
                // Handle error case
                errorfeild.textContent = "Failed to send otp";
                console.log("Failed to send OTP");
            }
        } catch (error) {
            console.error(error);
        }
    }
    else{
        if(otp1Input === ""){
            errorfeild.textContent = "Enter correct otp";
            return ;
        }
        try {
            alert("enter successfully");
            await fetch("http://127.0.0.1:8000/verify/", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    // Include any additional headers as needed
                },
                body: JSON.stringify({
                    phone_number : phone_number,
                    otp : otp1Input,
                    first_name : fnameInput,
                    last_name : lnameInput,
                }),
            })
            .then(response => {
                if(response.ok){
                    return response.json();
                }
                else{
                    console.error('Error:',response.statusText);
                }
            })
            .then(data =>{
                console.log(data.id);
                fetch("http://127.0.0.1:8000/user/" + data.id,{
                    method : 'GET',
                })
                .then(response =>{
                    if(response.ok){
                        window.location.href = response.url;
                    }
                    else{
                        console.error(response.statusText);
                    }
                })
                .catch(error =>{
                    console.error(error);
                })
            })
            .catch(error =>{
                console.error('error:',error);
            });

        } catch (error) {
            console.error('Error:', error);
        }


    }
};

