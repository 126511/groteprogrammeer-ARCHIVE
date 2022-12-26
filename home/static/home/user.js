function closemsg() {
    $('#msg').hide();
  }

  $('#msg').ready( function() {
    var msgtype = $('#msg').attr('value')
    if (msgtype == 1) {
      $('#msg').css('background-color', 'var(--success)');
    } else if (msgtype == 0) {
      $('#msg').css('background-color', 'var(--accent1)');
    } else {
      $('#msg').css('background-color', 'var(--error)')
    }
  })

//Triggers on every mouse move
$(document).mousemove(function() {
  
  //Is the user hovering on the navbar?
  if ($('#verticalnav').is(':hover') || $('#expandednav').is(':hover')) {
    ExpandNav();
  } else {
    CloseNav();
  }
});

//Expand the navbar
function ExpandNav() {
if ($('#expandednav').is(':hidden') && $('#expandednav').transition('is animating') == false) {
  $('#expandednav').transition('slide right');
  $('#verticalnav').css('box-shadow', '0 0px 0px');
}
}

//Close the navbar
function CloseNav() {
if ($('#expandednav').is(':visible') && $('#expandednav').transition('is animating') == false) {
  $('#expandednav').transition('slide right');
  $('#verticalnav').css('box-shadow', 'var(--shadow-2)');
}
}