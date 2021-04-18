function mc_disable_allbuttons(id) {
    a1 = document.getElementById(`${id}_1`);
    a2 = document.getElementById(`${id}_2`);
    a3 = document.getElementById(`${id}_3`);
    a4 = document.getElementById(`${id}_4`);

    if (a1.checked === false) {
        a1.disabled = true;
    }
    if (a2.checked === false) {
        a2.disabled = true;
    }
    if (a3.checked === false) {
        a3.disabled = true;
    }
    if (a4.checked === false) {
       a4.disabled = true;
    }
}

function mc_enable_allbuttons(id) {
    a1 = document.getElementById(`${id}_1`).disabled = false;
    a2 = document.getElementById(`${id}_2`).disabled = false;
    a3 = document.getElementById(`${id}_3`).disabled = false;
    a4 = document.getElementById(`${id}_4`).disabled = false;
}

function mc_check(id, correct) {
    if (document.getElementById(`${id}_${correct}`).checked) {
        q = document.getElementById(`${id}`);
        q.style.backgroundColor = "green";
        document.getElementById(`${id}_check`).style.display = "none";
        document.getElementById(`${id}_explanation`).style.display = "block";
        mc_disable_allbuttons(id);
    }
    else {
        document.getElementById(`${id}`).style.backgroundColor = "red";
        document.getElementById(`${id}_check`).style.display = "none";
        document.getElementById(`${id}_retry`).style.display = "inline-block";
        document.getElementById(`${id}_show_answer`).style.display = "inline-block";
        mc_disable_allbuttons(id);
    }
}

function mc_retry(id) {
    mc_enable_allbuttons(id);
    document.getElementById(`${id}_1`).checked = false;
    document.getElementById(`${id}_2`).checked = false;
    document.getElementById(`${id}_3`).checked = false;
    document.getElementById(`${id}_4`).checked = false;
    document.getElementById(`${id}`).style.backgroundColor = "grey";
    document.getElementById(`${id}_check`).style.display = "inline-block";
    document.getElementById(`${id}_retry`).style.display = "none";
    document.getElementById(`${id}_show_answer`).style.display = "none";
}

function mc_show_answer(id) {
    mc_disable_allbuttons(id);
    document.getElementById(`${id}_retry`).style.display = "none";
    document.getElementById(`${id}_explanation`).style.display = "block";
    document.getElementById(`${id}_show_answer`).style.display = "none";
    document.getElementById(`${id}_answer`).style.backgroundColor = "green";

}