
document.addEventListener('DOMContentLoaded', function () {
    const linkToUserBtns = document.querySelectorAll('.linkToUserBtn');
    linkToUserBtns.forEach(button => {
        button.addEventListener('click', showLinkToUserDialog);
    });
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
    fetch('/check_user', {
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
                console.log("verification passed")
                 userID = data.user_id
                link_device_to_user(userID, deviceId)
            }
            else {
                alert ('Verification Code incorrect, please try again')
            }
        }
        else {
            alert ('Email cant be found, Please enter a valid email')
        }
    })
    .catch(error => {
           alert(console.error('Error:', error));
        });

}

function link_device_to_user(userID, deviceId){
    fetch('/link_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({userid: userID, deviceid:deviceId})
    } )
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Device Linked Succesfully")
        }
        else {
            alert ('Something Went Wrong')
        }
    })
    .catch(error => {
           alert(console.error('Error:', error));
        });

}


// Function to create a parking report for MartGlobal. 
function ParkingReport() {

    document.querySelector('.reportDisplay').style.display="block";
    document.querySelector('.Report').style.display='none';
    var tableBody = document.getElementById("stopReport").getElementsByTagName("tbody")[0];
    tableBody.innerHTML = '';

    fetch('/report-parking',{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })

    .then(response =>{
        if (!response.ok){
            throw new Error('HTTP errpr! Status: ${response.status}');
        }
        return response.json();
    })
    .then(data => {
        document.querySelector('.loading').style.display='none';
        document.querySelector('.Report').style.display='block';
        
        data.forEach(item => {
            var row = tableBody.insertRow();
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);

            cell1.innerHTML = item.startTime;
            cell2.innerHTML = item.endTime;
            cell3.innerHTML = item.address;
            cell4.innerHTML = item.duration;
        });

    })

    .catch(error => {
        console.error('Error: ', error)
    })
    
}