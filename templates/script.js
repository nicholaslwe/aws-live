// initialize data array
var data = JSON.parse(localStorage.getItem("data")) || [];

// create function
function create() {

	var id = document.getElementById("id").value;
	var name = document.getElementById("name").value;
    var startDate = document.getElementById("startDate").value;
    var dateParts = startDate.split("-");
    var formattedDate = dateParts[2] + "/" + dateParts[1] + "/" + dateParts[0];

    var duration = document.getElementById("duration").value;
    var reason = document.getElementById("reason").value;
    
    if(id.length == 0){
        alert("Please enter an id!");
        return false;
    }else if(name.length == 0){
        alert("Please enter a name!");
        return false;
    }else if(startDate.length == 0){
        alert("Please select a date!");
        return false;
    }else if(duration.length <= 0){
        alert("Please select duration!");
        return false;
    }
    else if(reason.length == 0){
        alert("Please provide a reason!");
        return false;
    }

	var newData = { id: id, name: name, date: formattedDate, duration: duration, reason: reason };
	data.push(newData);
	localStorage.setItem("data", JSON.stringify(data));
	readAll();

    alert("Leave has been applied!");
}

// readAll function
function readAll() {
	var table = document.getElementById("data-table");
	var rows = "";

	data.forEach(function(d) {

		rows += "<tr>";
		rows += "<td>" + d.id + "</td>";
		rows += "<td>" + d.name + "</td>";
		rows += "<td>" + d.date + "</td>";
		rows += "<td>" + d.duration + "</td>";
		rows += "<td>" + d.reason + "</td>";
		rows += "<td><button onclick='update(\"" + d.id + "\")'>Update</button>";
		rows += " <button onclick='remove(\"" + d.id + "\")'>Delete</button></td>";
		rows += "</tr>";
	});

	table.innerHTML = rows;
}

// update function
function update(id) {
	var newName = prompt("Enter new name:");
    var newDate = prompt("Select new date:");
    var newDuration = prompt("Select new duration:");
    var newReason = prompt("Provide a new reason:");
	data.forEach(function(d) {
		if (d.id == id) {
			d.name = newName;
            d.date = newDate;
            d.duration = newDuration;
            d.reason = newReason;
		}
	});
	localStorage.setItem("data", JSON.stringify(data));
	readAll();
    alert("Leave has been updated!");
}

// remove function
function remove(id) {
	data = data.filter(function(d) {
		return d.id != id;
	});
	localStorage.setItem("data", JSON.stringify(data));
	readAll();
    alert("Leave has been removed!");
}
