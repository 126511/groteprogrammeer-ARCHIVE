// Animates the expansion of the login card
function ExpandLogin() {
    $('.class_login').transition('slide down');
    }

// Closes the logincard by clicking outside the logincard, fires when the user clicks
$(document).click( function(event) {

// If the target of the click was not the login card and the login card is visible and not animating --> close the login card
if (!$(event.target).closest('.class_login').length && !$('.class_login').transition('is animating') && $('.class_login').is(':visible')) {
    $('.class_login').transition('slide down');
}
})

// Hide the message once the 'x' is clicked
function closemsg() {
$('#msg').hide();
}

// Change the close button on the message
$(document).on('mouseenter','#closemsg', function() {
$('#closemsg i').removeClass('outline');
})

// Change the close button on the message
$(document).on('mouseleave', '#closemsg', function() {
$('#closemsg i').addClass('outline');
})

// Change the color of the message according to the message type
$('#msg').ready( function() {

// Get the value attribute of #msg and store it, which is the value passed from the backend
var msgtype = $('#msg').attr('value')

// Color the message according to the value of msgtype
if (msgtype == 1) {
    $('#msg').css('background-color', 'var(--success)');
} else if (msgtype == 0) {
    $('#msg').css('background-color', 'var(--accent1)');
} else {
    $('#msg').css('background-color', 'var(--error)')
}
})