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