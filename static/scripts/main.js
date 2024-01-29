
document.addEventListener('DOMContentLoaded', function () {
    const linkToUserBtns = document.querySelectorAll('.linkToUserBtn');
    linkToUserBtns.forEach(button => {
        button.addEventListener('click', showLinkToUserDialog);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Show/hide custom date inputs based on user selection
    var dateRangeSelect = document.getElementById('dateRange');
    var customDateInputs = document.getElementById('customDateInputs');
    dateRangeSelect.addEventListener('change', function() {
        if (dateRangeSelect.value === 'custom') {
            customDateInputs.style.display = 'block';
        } else {
            customDateInputs.style.display = 'none';
        }
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

function showParkingReportForm(){
    var parkingReportButton = document.getElementById('parkingReport')
    parkingReportButton.disabled = true;
    document.querySelector('.reportform').style.display = 'block';
}

// Function to create a parking report for MartGlobal. 
function ParkingReport(event) {
    event.preventDefault();
    var parkingReportButton = document.getElementById('parkingReport')
    parkingReportButton.disabled = true;

    document.querySelector('.reportDisplay').style.display="block";
    var tableBody = document.getElementById("stopReport").getElementsByTagName("tbody")[0];
    tableBody.innerHTML = '';


    //get Selected devices
    var selectedDevices = Array.from(document.getElementById('selectedDevices').selectedOptions)
        .map(option => option.value);

    // Get selected date range
    var dateRange = document.getElementById('dateRange').value;

    // Get custom date inputs if date range is "custom"
    var fromDate = '';
    var toDate = '';
    if (dateRange === 'custom') {
        fromDate = document.getElementById('fromDate').value;
        toDate = document.getElementById('toDate').value;
        fromDate += 'T00:00:00+00:00';
        toDate += 'T23:59:59+00:00';
    } else if (dateRange === 'today') {
        var currentDate = new Date();
        fromDate = currentDate.toISOString().split('T')[0] + 'T00:00:00+00:00';
        toDate = currentDate.toISOString().split('T')[0] + 'T23:59:59+00:00';
    } else if (dateRange === 'yesterday') {
        var yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        fromDate = yesterday.toISOString().split('T')[0] + 'T00:00:00+00:00';
        toDate = yesterday.toISOString().split('T')[0] + 'T23:59:59+00:00';
    }

    // Perform validation checks
    if (selectedDevices.length === 0) {
        alert('Please select at least one device.');
        return; // Stop further execution
    }

    if (dateRange === 'custom' && (!fromDate || !toDate)) {
        alert('Please select both "From" and "To" dates for the custom date range.');
        return; // Stop further execution
    }

    // Prepare data to send to the backend
    var formData = {
        selectedDevices: selectedDevices,
        fromDate: fromDate,
        toDate: toDate
    };


    fetch('/report-parking',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })

    .then(response =>{
        if (!response.ok){
            throw new Error('HTTP errpr! Status: ${response.status}');
        }
        return response.json();
    })
    .then(data => {
        document.querySelector('.loading').style.display='none';

        var deviceName = document.getElementById('deviceName');
        var reportFrom = document.getElementById('reportFrom');
        var reportTo = document.getElementById('reportTo');
        deviceName.innerHTML = "Demo Bike";
        reportFrom.innerHTML = "29th Jan 2023";
        reportTo.innerHTML = "21st Jan 2023";
        var i = 1
        
        tableBody.innerHTML = '';
        data.forEach(item => {
            var row = tableBody.insertRow();
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            cell1.innerHTML = i
            cell2.innerHTML = item.startTime;
            cell3.innerHTML = item.endTime;
            cell4.innerHTML = item.address;
            cell5.innerHTML = item.duration;

            i++;
        });
        document.querySelector('.reportinfo').style.display='block';
        parkingReportButton.disabled = true;
    })

    .catch(error => {
        console.error('Error: ', error)
    })
    
}


function printReport() {
    // Clone the report display div
    var reportDisplayClone = document.getElementById('reportDisplay').cloneNode(true);

    // Create a new window or tab
    var printWindow = window.open('', '_blank');
    
    // Write the cloned div content to the new window or tab
    printWindow.document.write('<html><head><title>Print Report</title></head><body>');
    printWindow.document.write('<style>@media print { body { visibility: hidden; } .reportDisplay { visibility: visible; } }</style>');
    printWindow.document.write(reportDisplayClone.outerHTML);
    printWindow.document.write('</body></html>');

    // Print the content
    printWindow.document.close(); // Close the document opened with document.write
    printWindow.print();
}



