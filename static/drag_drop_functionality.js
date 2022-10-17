function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("Text", ev.target.getAttribute("data-date"));
}

function drop(ev) {
    var data = ev.dataTransfer.getData("Text");
    console.log(ev.dataTransfer);
    ev.target.value=data;
    //ev.target.appendChild(document.getElementById(data).cloneNode(true));
    ev.preventDefault();
}