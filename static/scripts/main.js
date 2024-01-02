
document.addEventListener('DOMContentLoaded', function () {
    const linkToUserBtn = document.getElementById('linkToUserBtn');
    linkToUserBtn.addEventListener('click', showLinkToUserDialog);
});


function showAddDeviceForm() {
    // Show the add device form
    document.querySelector('.add-device-form').style.display = 'block';
    document.querySelector('.close_btn').style.display = 'block';
    document.querySelector('.add_btn').style.display = 'none';
}

function hideAddDeviceForm(){
    document.querySelector('.add-device-form').style.display = 'none'
    document.querySelector('.add_btn').style.display = 'block';
    document.querySelector('.close_btn').style.display = 'none';
}

function showAddUserForm() {
    // Show the add device form
    document.querySelector('.add-user-form').style.display = 'block';
    document.querySelector('.close_user_btn').style.display = 'block';
    document.querySelector('.add_user_btn').style.display = 'none';
}

function hideAddUserForm(){
    document.querySelector('.add-user-form').style.display = 'none'
    document.querySelector('.add_user_btn').style.display = 'block';
    document.querySelector('.close_user_btn').style.display = 'none';
}


function addDevice(event) {
    event.preventDefault();

    // Get input values
    const plateNumber = document.getElementById('platenumber').value;
    const uniqueId = document.getElementById('uniqueid').value;
    const devicePhone = document.getElementById('devicephone').value;
    const simCarrier = document.getElementById('simcarrier').value;
    const category = document.getElementById('category').value;
    const renewalCost = document.getElementById('renewalcost').value;
   
    // Prepare the data to send to Flask in Json
    const data = {
        plateNumber: plateNumber,
        uniqueId: uniqueId,
        devicePhone: devicePhone,
        simCarrier: simCarrier,
        category: category,
        renewalCost: renewalCost
    };

    fetch('/add_device', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(result => {
        // Handle the result if needed
        console.log(result);
        document.querySelector('.add-device-form').style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error.message);
    });
}


function addUsers(event) {
    event.preventDefault();

    // Get input values
    const u_name = document.getElementById('u_name').value;
    const u_email = document.getElementById('u_email').value;
    const u_phone = document.getElementById('u_phone').value;
    //add expiration time from backend.
    
    
   
    // Prepare the data to send to Flask in Json
    const data = {
        name: u_name,
        email: u_email,
        phone: u_phone,
    };
    

    fetch('/reg_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(result => {
        // Handle the result if needed
        console.log(result);
        document.querySelector('.add-user-form').style.display = 'none';
        document.querySelector('.close_user_btn').style.display = 'none';
        document.querySelector('.add_user_btn').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error.message);
    });
}


function showLinkToUserDialog(event) {
    const deviceId = event.target.getAttribute('data-device-id');

    const email = prompt('Enter the email address of the user:');
    if (email) {
        checkUserExistence(email, deviceId)
    }
}

function checkUserExistence(email, deviceId){
    fetch('/check_user_existence', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email: email})
    } )
    .then(response => response.json())
    .then(data => {
        if (data.exists) {
            const verificationCode = prompt('Enter Confirmation Code')
            if (verificationCode && verificationCode === data.verification_code){
                link_device_to_user(email, deviceId)
            }
        }
    })

}

function link_device_to_user(email, deviceId){
    fetch('/link_device'),{
        
    }
}