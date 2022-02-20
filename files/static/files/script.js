var qobj = '{ "mcquestions" : [ { "options" : ["Copy", "Fork", "Insert", "Repl"], "questions" : [false, true, false, false], "ans" : "Fork betekent dat jij de Repl die wij voor je hebben gemaakt kopieert, zodat je hem zelf kan aanpassen.", "title" : "Welke term drukt het kopieren van een stuk code uit zodat jij het voor jezelf kan aanpassen?"} ],"ocquestions" : [{"ans" : "compiler","explanation" : "Je kan de compiler een beetje zien als Google Translate voor programmeren. Je stopt er een bepaalde taal in (in dit geval C), dit noem je de source code. De compiler vertaalt dat tot machine code: uitsluitend bestaand uit binaire taal. Dit begrijpt de computer wel en kan het gaan uitvoeren.","title" : "Hoe heet de vertaler die van source code machine code maakt?" }],"usedterms" : ["Github"]}'

// Builds the question card from JSON
function buildmcquestion(qnum) {
    $('.multiplechoice').eq(qnum).append(`<h1 class="questiontitle">${qobj.mcquestions[qnum].title}</h1>`);
    qobj.mcquestions[qnum].options.forEach(element => {
        $('.multiplechoice').eq(qnum).append(`<div class="ui radio checkbox"><input type="radio" name="mcquestion${qnum}"><label id="checkboxtext">${element}</label></div><br>`)
    });
    $('.multiplechoice').eq(qnum).append(`
        <button class="ui button check" id="checkanswer">Check</button>
        <button class="ui button retry" id="retryanswer" style="display: none;">Opnieuw</button>
        <button class="ui button show" id="showanswer" style="display: none;">Antwoord</button>
    `);
    $('.multiplechoice').eq(qnum).append(`<div class="correctanswer">${qobj.mcquestions[qnum].ans}</div>`);

};

// Builds the open question card
function buildocquestion(qnum) {
    console.log("hmmm");
    $('.openquestion').eq(qnum).append(`<h1 class="questiontitle" name="ocquestion${qnum}">${qobj.ocquestions[qnum].title}</h1>`);
    $('.openquestion').eq(qnum).append('<div class="ui input" style="margin-bottom: 8px;"><input type="text" placeholder="Antwoord" id="ocanswer"></div><br>');
    $('.openquestion').eq(qnum).append(`
        <button class="ui button checkoc" id="checkanswer">Check</button>
        <button class="ui button retryoc" id="retryanswer" style="display: none;">Opnieuw</button>
        <button class="ui button showoc" id="showanswer" style="display: none;">Antwoord</button>
    `);
    $('.openquestion').eq(qnum).append(`<div class="correctanswer">${qobj.ocquestions[qnum].explanation}</div>`);
};

function getcorrect(qnum) {
    for (i in Object.keys(qobj.mcquestions[qnum].questions)) {
        if (qobj.mcquestions[qnum].questions[i] === true) {
            return i;
        };
    };
};

// Fires when the DOM has finished loading
$(document).ready( function() {
    
    $('.navbtn').eq(1).css({"background-color": "var(--accent1)", "color": "white"});

    // Parse the string so the program understands the JSON
    qobj = JSON.parse(qobj);

    // Loops through available multiple choice questions in JSON object
    for (i in Object.keys(qobj.mcquestions)) {
        buildmcquestion(i);
    };

    // Does the same for open questions
    for (i in Object.keys(qobj.ocquestions)) {
        buildocquestion(i);
    }

    // Copy function, deselects everything, then selects the target, copies, then deselects
    $('code').click( function(e) {
        var range = document.createRange()
        range.selectNode(this);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand("copy");
        window.getSelection().removeAllRanges();

        // Animation for copying
        $(this).append(`<div class="copymsg" style="top:${e.pageY - 48}px; left:${e.pageX}px">Gekopieerd!</div>`)
        $(this).children('.copymsg').transition({animation : 'fade up', duration : '3s', onComplete : function() {
            $(this).remove();
        } }).animate({top: e.pageY - 96, duration : 3000});
    });

    // Replaces terms in the lesson so the buttons work
    $('#lesson').children('p').each( function() {
        var htmltext = $(this).html().toString();

        // Loop through the declared terms
        for (i in Object.keys(qobj.usedterms)) {
            
            // Search for the term, store the location
            var n = htmltext.indexOf(qobj.usedterms[i]);

            // Convert term to lowercase and add dashes, making it a slug I think
            var convertterm = qobj.usedterms[i].replace(/\s+/g, '-').toLowerCase();

            // Store the length of the term
            var termlength = qobj.usedterms[i].length;

            // Check wether the term exists, keep looping until all terms have been found
            while (n != -1) {

                // Insert the button html on the right place
                htmltext = htmltext.substr(0, n) + `<button class="terms" onclick="get_html('${convertterm}')">${qobj.usedterms[i]}</button>` + htmltext.substr(n + termlength);
                $(this).html(htmltext);

                // Look for the term again behind the one just found
                n = htmltext.indexOf(qobj.usedterms[i], n + termlength + 54);
            };
        };
    });

    // Checks if the user answered correctly
    $('.checkoc').click( function() {
        var qnum = getqnum($(this).siblings('.questiontitle').attr('name'));

        if ($(this).siblings('.input').children('input').val() === qobj.ocquestions[qnum].ans) {
            $(this).parent().css('background-color', 'var(--success)');
            $(this).siblings('.showoc').hide();
            $(this).siblings('.retryoc').hide();
            $(this).siblings('.correctanswer').show();
        } else {
            $(this).parent().css('background-color', 'var(--error)');
            $(this).siblings('.showoc').show();
            $(this).siblings('.retryoc').show();
        };
        $(this).hide();
        $(this).siblings('.input').children('input').prop('disabled', true);
    });
    
    // Retry button
    $('.retryoc').click( function() {

        $(this).siblings('.input').children('input').val('');
        $(this).siblings('.input').children('input').prop('disabled', false);
        $(this).hide();
        $(this).siblings('.checkoc').show();
    })

    // Shows the answer to the user
    $('.showoc').click( function() {
        
        var qnum = getqnum($(this).siblings('.questiontitle').attr('name'));
        
        $('#ocanswer').val(qobj.ocquestions[qnum].ans);
        $(this).siblings('.input').children('input').prop('disabled', true);
        $(this).hide();
        $(this).siblings('.check').hide();
        $(this).siblings('.retryoc').hide();
        $(this).parent().css('background-color', 'var(--accent1)');
        $(this).siblings('.correctanswer').show();
    });

    $('.check').click( function() {
        
        // Create a variable which knows which question the user is checking
        var qnum = getqnum($(this).siblings('.radio').eq(0).children('input').attr('name'));

        // Create a variable that holds wether the user answered correctly
        var correct = false;

        // Loop through the available answers
        for (i in Object.keys(qobj.mcquestions[qnum].questions)) {
            
            // Check wether the user has checked the answer and if so, wether the answer the user checked is correct
            if ( $(this).siblings('.radio').eq(i).children('input').is(':checked') && qobj.mcquestions[qnum].questions[i] === true ) {
                correct = true
            }
            $(this).siblings('.radio').eq(i).children('input').prop('disabled', true)
        };
        
        // If the variable is true, the user has answered correctly
        if (correct === true) {
            $(this).siblings('.correctanswer').show();
            $(this).siblings('.show').hide();
            $(this).parent().css('background-color', 'var(--success)');
            $(this).siblings('.radio').eq( getcorrect(qnum) ).children('input').prop('disabled', false);
            $(this).siblings('.radio').eq( getcorrect(qnum) ).children('label').css('font-weight', 'bold');
        } else {
            $(this).siblings('.retry').show();
            $(this).siblings('.show').show();
            $(this).parent().css('background-color', 'var(--error)');
        }
        $(this).hide();
    });
    
    // Retry button, resets the question so the user can answer again
    $('.retry').click( function() {
        var qnum = getqnum($(this).siblings('.radio').eq(0).children('input').attr('name'));

        for (i in Object.keys(qobj.mcquestions[qnum].questions)) {
            $(this).siblings('.radio').eq(i).children('input').prop('disabled', false)
        };
        $(this).hide();
        $(this).siblings('.check').show();

    });

    // Show button, shows the correct answer and disables user input
    $('.show').click( function() {
        var qnum = getqnum($(this).siblings('.radio').eq(0).children('input').attr('name'));

        for (i in Object.keys(qobj.mcquestions[qnum].questions)) {
            $(this).siblings('.radio').eq(i).children('input').prop('disabled', true);
            $(this).siblings('.radio').eq(i).children('input').prop('checked', false);
        };
        $(this).hide();
        $(this).siblings('.check').hide();
        $(this).siblings('.retry').hide();
        $(this).siblings('.correctanswer').show();
        $(this).parent().css('background-color', 'var(--accent1)');
        $(this).siblings('.radio').eq( getcorrect(qnum) ).children('input').prop('disabled', false);
        $(this).siblings('.radio').eq( getcorrect(qnum) ).children('label').css('font-weight', 'bold');
        $(this).siblings('.radio').eq(i).children('input').prop('checked', true);
    });
});

// Simple function which shortens qnum
function getqnum(qnum) {
    qnum = qnum.slice(-1);
    return qnum
}

// ------------------------- To Import The Lessons-----------------------------------------------
// ------------------------- Needs To Change ----------------------------------------------------

function getdocs(term) {
    const docs = document.getElementById("docs").value;
    o = JSON.parse(`${docs}`)
    const text = o[`${term}`]
    document.querySelector("#documentation").innerHTML = text

    const documentation = document.getElementById("sidebar")
    documentation.style.display = "block";
    const lesson = document.getElementById("lesson")
    lesson.style.width = "70%";
    lesson.style.marginRight = "0px";
}
function gaweg() {
    const d = document.getElementById("sidebar");
    d.style.display = "none";
    const l = document.getElementById("lesson");
    l.style.width = "70%";
    l.style.marginRight = "auto";
}

function get_html(url) {
    fetch(`/docs/${url}`).then(function (response) {
        const r = response.text()
        return r
    }).then(function (html) {
        console.log(html)
        document.getElementById("documentation").innerHTML = html;
        document.getElementById("link2docs").href = `/docs/link/${url}`;
    }).catch(function (err) {
        console.warn('Something went wrong.', err);
    });

    const documentation = document.getElementById("sidebar")
    documentation.style.display = "block";
    const lesson = document.getElementById("lesson")
    lesson.style.width = "70%";
    lesson.style.marginRight = "0px";
}