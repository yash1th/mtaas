function handleFiles() {

$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "C:\Users\Nitesh\Downloads\joli2\joli\js\credentials.csv"",
        dataType: "csv",
        success: function (data) { processData(data); }
    });
});
}

function processData(allText) {
var allTextLines = allText.split(/\r\n|\n/);
var headers = allTextLines[0].split(',');
var lines = [];

for (var i = 1; i < allTextLines.length; i++) {
    var data = allTextLines[i].split(',');
    if (data.length == headers.length) {

        var tarr = [];
        for (var j = 0; j < headers.length; j++) {
            tarr.push(headers[j] + ":" + data[j]);
        }
        lines.push(tarr);
    }
}
console.log(lines);
drawOutput(lines);
}

function drawOutput(lines) {
//Clear previous data
document.getElementById("output").innerHTML = "";
var table = document.createElement("table");
for (var i = 0; i < lines.length; i++) {
    var row = table.insertRow(-1);
    for (var j = 0; j < lines[i].length; j++) {
        var firstNameCell = row.insertCell(-1);
        firstNameCell.appendChild(document.createTextNode(lines[i][j]));
    }
}
document.getElementById("output").appendChild(table);
}