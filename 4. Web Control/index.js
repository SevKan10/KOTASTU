// async function changeStatus() // Lấy dữ liệu từ Blynk
// {
//     var getDataUrl = "https://sgp1.blynk.cloud/external/api/get?token=s4IEZXPS6DFlYAACZC_6z-rNmdU1erLH&v1";
    
//     try 
//     {
//         let getResponse = await fetch(getDataUrl);
//         if (getResponse.ok) 
//         {
//             let data = await getResponse.text(); 
//             console.log("Data received: " + data);
//             updateButtonStates(data.split(','));
//         } else {
//             console.error("Get error: " + getResponse.status);
//         }
//     } catch (error) 
//     {
//         console.error("Get fetch error: " + error);
//     }   
// }

function toggleDeviceState(device)
{ 
    var button = document.getElementById("device" + device);
    var currentState = button.innerHTML.toLowerCase();

    if (currentState === "turn on " + device) 
    {
        button.innerHTML = "Turn Off " + device;
        button.classList.remove("on");
        button.classList.add("off");
        var staOn = "On" + device;
        console.log(staOn);
        controlDevice(staOn);
    } else {
        button.innerHTML = "Turn On " + device;
        button.classList.remove("off");
        button.classList.add("on");
        var staOff = "Off" + device;
        console.log(staOff);
        controlDevice(staOff);
    }
}

function updateButtonStates(data) 
{ 
    for (let i = 1; i <= 8; i++) 
    {
        let button = document.getElementById("device" + i);
        if (button) 
        {
            let deviceState = "Off"; // Khởi tạo trạng thái mặc định
            for (let j = 0; j < data.length; j++) 
            {
                if (data[j] === "On" + i) 
                {
                    deviceState = "On";
                    break;
                } else if (data[j] === "Off" + i) 
                {
                    deviceState = "Off";
                    break;
                }
            }
            // Cập nhật trạng thái của nút tương ứng
            if (deviceState === "On") 
            {
                button.classList.remove("on");
                button.classList.add("off");
                button.innerHTML = "Turn Off " + i;
            } else if (deviceState === "Off") 
            {
                button.classList.remove("off");
                button.classList.add("on");
                button.innerHTML = "Turn On " + i;
            }  
        }
    }
}

setInterval(changeStatus, 1000);

function controlDevice(deviceNumber) 
{ 
    var xhr = new XMLHttpRequest(); 
    var url = "https://sgp1.blynk.cloud/external/api/update?token=s4IEZXPS6DFlYAACZC_6z-rNmdU1erLH&v0=" + deviceNumber;
    console.log("Send");
    xhr.open("GET", url, true);
    xhr.send();
}

function callNumberPhone() 
{ 
    var numberPhone = document.getElementById("numberPhone").value;
    console.log(numberPhone); 
    if (numberPhone.trim() === "" || !/^\d+$/.test(numberPhone)) 
    {
        alert("Please enter a valid numberPhone");
    } else {
        var xhr = new XMLHttpRequest();
        var url = "https://sgp1.blynk.cloud/external/api/update?token=s4IEZXPS6DFlYAACZC_6z-rNmdU1erLH&v2=" + numberPhone;
        xhr.open("GET", url, true);
        xhr.send();
        console.log("Send number Phone");
        alert("Calling to " + numberPhone);
    }
}

function setTimer() 
{ 
    var hourOn = document.getElementById("hourOn").value; 
    var minuteOn = document.getElementById("minuteOn").value;
    var hourOff = document.getElementById("hourOff").value;
    var minuteOff = document.getElementById("minuteOff").value;
    var deviceSelect = document.getElementById("selectDevice").value;
    var setTimeString =",ON," + hourOn + "," + minuteOn + "," + hourOff + "," + minuteOff + "," + deviceSelect + ","; 

    console.log(setTimeString); 
    var xhr = new XMLHttpRequest();
    var url = "https://sgp1.blynk.cloud/external/api/update?token=s4IEZXPS6DFlYAACZC_6z-rNmdU1erLH&v3=" + setTimeString;
    xhr.open("GET", url, true);
    xhr.send();
    console.log("Send timer"); 
    alert("Sent timer");

}

function stopDevice() 
{ 
    var deviceSelect = document.getElementById("selectDevice").value;

    console.log("STOP," + deviceSelect + ","); 
    var xhr = new XMLHttpRequest();
    var url = "https://sgp1.blynk.cloud/external/api/update?token=s4IEZXPS6DFlYAACZC_6z-rNmdU1erLH&v2=" + "STOP," + deviceSelect + ",";
    xhr.open("GET", url, true);
    xhr.send();
    console.log("Send stop"); 
    alert("Cleared timer");
}
//Code by SevKan