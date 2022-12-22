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