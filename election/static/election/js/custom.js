function testFunction(id){
  $("#page-content").load("create");
}; 

let inputFields= [];
var numInput = 0
$(document).ready(function(){
  $(document).on('click', '#add', function(){
    var html = '';
    numInput++;
    html += '<tr>';
    html += '<td class="align-middle">';
    html += '<div class="form-group">';
    html += '<input type="text" class="form-control" name="inputName" ';
    html += 'aria-describedby="campusInputs" placeholder="Enter name" required>';
    html += '</div></td>';
    html += '<td>';
    html += '<a href="#" id="remove" class="btn btn-danger" data-toggle="tooltip" data-placement="bottom" title="Delete">';
    html += '<i class="fas fa-trash-alt"></i></a>';
    html += '</td></tr>';
    inputFields.push(numInput)
    document.getElementById("save").disabled=false;
    $('#add-table').append(html);
  });

  $(document).on('click', '#remove', function(){
    $(this).closest('tr').remove();
    if (inputFields.length) {
      document.getElementById("save").disabled=true;
    }
  });
});

$('#staticBackdrop').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  var url = button.data('url')
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('#update-modal').attr('action', url)
  modal.find('#inputText').attr('value', recipient)
  modal.find('.modal-body small').text('Current name: '+ recipient)
});     


$('#staticDelete').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  var url = button.data('url')
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('#delete-modal').attr('action', url)
  modal.find('.modal-body p').text(recipient)
});     

$(document).ready(function () {
var unsaved = false;
 $('#save').click(function() {
    unsaved = false;
});

var unsaved = false;
 $('#delete').click(function() {
    unsaved = false;
});

 $(window).bind('beforeunload', function() {
    if(unsaved){
        return "You have unsaved changes on this page. Do you want to leave this page and discard your changes or stay on this page?";
    }
});

// Monitor dynamic inputs
$(document).on('change', ':input', function(){ //triggers change in all input fields including text type
    unsaved = true;
});
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
    $("#sscForm").submit(function(){
      var electionType = document.getElementById('electionTypeId').value;
      var extra = document.getElementsByName("extras"),
      extras  = [].map.call(extra, function( input ) {
          return input.value;
      });
      var candidateName = document.getElementsByName('candidate_name'),
      candidateNames  = [].map.call(candidateName, function( input ) {
          return input.value;
      });
      var collegeId = document.getElementsByName("collegeId"),
      collegeIds  = [].map.call(collegeId, function( input ) {
          return input.value;
      });
    var getValue;
    var jsonFormId = [];
    $("option:selected").each(function() {
      jsonFormId.push($(this).val())
      //var getValue = $.parseJSON($(this).val())
  });
    for (i=0; i < collegeIds.length; i++) {
        jsonFormId.push(collegeIds[i])
    }
    var x = candidateNames.length;
    for (i = x - 1; i >= 0; i--) {
      if (candidateNames[i] == '') {
        candidateNames.splice(i, 1);
        jsonFormId.splice(i, 1);
      }
    }
    // var extras = new Object();
    //   extras.name = $('#partyName').val();
    //   extras.acronym = $('#partyAcronym').val();

        $.ajax({
        type:'POST',
        url:'/save/',
        data: {
          'ElectionType': electionType,
          'CandidateNames[]': candidateNames,
          'Ids[]': jsonFormId,
          'Extras[]': extras,
          csrfmiddlewaretoken : csrftoken
        },
        success:function(){
          window.location = '/save/';
        }
      });
    });

function formOnchange(value, id) {
  if ($.trim(value).length == 0) {
    document.getElementById(id).disabled=true;
    document.getElementById(id).value = '';
  } else {
    document.getElementById(id).disabled=false;
  }
}

  $( function() {
    $( "#sortable" ).sortable();
    
  } );

