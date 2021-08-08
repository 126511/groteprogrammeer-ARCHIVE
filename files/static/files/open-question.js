function open_disable_field(id) {
    document.getElementById(`${id}_input`).disabled = true;
    
}

function open_enable_field(id) {
    document.getElementById(`${id}_input`).disabled = false;
}

function open_check(id) {
    if (document.getElementById(`${id}_input`).value === document.getElementById(`${id}_answer`).innerHTML) {
        q = document.getElementById(`${id}`);
        q.style.backgroundColor = "green";
        document.getElementById(`${id}_check`).style.display = "none";
        document.getElementById(`${id}_explanation`).style.display = "block";
        open_disable_field(id);
    }
    else {
        document.getElementById(`${id}`).style.backgroundColor = "red";
        document.getElementById(`${id}_check`).style.display = "none";
        document.getElementById(`${id}_retry`).style.display = "inline-block";
        document.getElementById(`${id}_show_answer`).style.display = "inline-block";
        open_disable_field(id);
    }
}

function open_retry(id) {
    open_enable_field(id);
    document.getElementById(`${id}_input`).value = "";
    document.getElementById(`${id}`).style.backgroundColor = "grey";
    document.getElementById(`${id}_check`).style.display = "inline-block";
    document.getElementById(`${id}_retry`).style.display = "none";
    document.getElementById(`${id}_show_answer`).style.display = "none";
}

function open_show_answer(id) {
    open_disable_field(id);
    document.getElementById(`${id}_retry`).style.display = "none";
    document.getElementById(`${id}_explanation`).style.display = "block";
    document.getElementById(`${id}_answer`).style.display = "inline-block";
    document.getElementById(`${id}_show_answer`).style.display = "none";

}