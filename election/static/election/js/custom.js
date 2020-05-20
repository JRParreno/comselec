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
    html += '<button id="remove" class="btn btn-danger" data-toggle="tooltip" data-placement="bottom" title="Delete">';
    html += '<i class="fas fa-trash-alt"></i></button>';
    html += '</td></tr>';
    inputFields.push(numInput)
    document.getElementById("saveBtn").disabled=false;
    $('#add-table').append(html);
  });

  $(document).on('click', '#remove', function(){
    $(this).closest('tr').remove();
    if (inputFields.length) {
      document.getElementById("saveBtn").disabled=true;
    }
  });
});


let boardFields= [];
var boardInput = 0
let dropDownCollege = [];
$( "#boardMember" )
  .change(function() {
    var html = "";
    $( "#boardMember option:selected" ).each(function() {
      if($( this ).text() != '') {
        boardInput++;
        collegeName = 
        collegeVal = "'"+$( this ).filter(":selected").val()+"'"
        html += '<tr>';
        html += '<td class="align-middle">';
        html += '<div class="form-group">';
        html += '<input type="text" class="form-control" name="inputName" ';
        html += 'aria-describedby="campusInputs" placeholder="Enter name" required>';
        html += '</div></td>';
        html += '<td>'+ $( this ).text()
        html += '<input type="hidden" name="collegeId" value='+collegeVal+'>';
        html += '</td>'
        html += '<td>';
        html += '<button href="#" id="remove" class="btn btn-danger" data-toggle="tooltip" data-placement="bottom" title="Delete" ';
        html += '>'
        html += '<i class="fas fa-trash-alt"></i></button>';
        html += '</td></tr>';
        document.getElementById("saveBtn").disabled=false;
        $('select').val('');
        $('#add-table').append(html);
      }
    });
    
  })
  .trigger( "change" );

var ciscInput = 0
$( "#addVoter" )
  .change(function() {
    var html = "";
    $( "#addVoter option:selected" ).each(function() {
      if($( this ).text() != '') {
        collegeName = 
        collegeVal = "'"+$( this ).filter(":selected").val()+"'"
        var obj = JSON.parse($(this).val())
        positionId = "'" + obj["id"]+ "'"
        html += '<tr>';
        html += '<td class="align-middle">';
        html += '<div class="form-group">';
        html += '<input type="text" class="form-control" name="voterInputs" ';
        html += 'aria-describedby="voterInputs" placeholder="Enter name" required>';
        html += '</div></td>';
        html += '<td><input type="text" name="studentNumber" class="form-control" pattern="[0-9]{4}[-][0-9]{6}" title="student number format 2015-XXXXXX" required/>';
        html += '</td>'
        html += '<td>'+ $( this ).text();
        html += '<input type="hidden" name="positionId" value="'+obj["id"]+'">';
        html += '</td>'
        html += '<td>';
        html += '<button href="#" id="removePosition" class="btn btn-danger" data-toggle="tooltip" data-placement="bottom" title="Delete" ';
        html += 'onclick="getPosition('+positionId+')">'
        html += '<i class="fas fa-trash-alt"></i></button>';
        html += '</td></tr>';
        setOptionPosition($( this ).text());
        document.getElementById("saveVoter").disabled=false;
        $('#addVoter').val(''); 
        $( this ).remove(); 
        $('#add-table').append(html);
      }
    });
    
  })
  .trigger( "change" );


$("#saveVoter").click(function(e){
  var valid = this.form.checkValidity();
  if(valid){
    event.preventDefault();   //stops the "normal" form request
    removeSmallText(); //function to remove current small tag
    checkStudentNumberExist(); //check student number exists  
  }
  

});

function validate(exists){
  var form = document.querySelector('form');
  var duplicate = checkStudentNumberDuplicate(); //check duplication of inputs
  if(!exists && !duplicate){
    checkForm(form);//checking form to submit
  }
}


function checkStudentNumberDuplicate(){
var frm = document.querySelector('form');
var inputs = frm.querySelectorAll('input[name=studentNumber]');
var valid = false;
var html = '';
  //set to focus of input click remove border red
  for(var j = 0; j < inputs.length; j++) {
      inputs[j].addEventListener('focus', function() {
          this.style.removeProperty('border');;
      });
  }

  var classArr = [];
  //iterate if user input duplicate student number
  for (var i = 0; i < inputs.length; i++) {
    if(classArr.indexOf(inputs[i].value) != -1){
      inputs[i].style.borderColor = "red";
      var text = '';
      if($(inputs[i]).next().is('small')){
        text = "& ";
      }
      html += '<small name="studentDuplicate" style="color: red;">error student number must be unique '+text+'</small>'
      $(inputs[i]).after(html);
      valid = true;
    } else {
      classArr.push(inputs[i].value);
    }
  }
  return valid;
}


function removeSmallText(){
   //remove all by tag name 'small'
    var element = document.getElementsByTagName("small"), index;
    for (index = element.length - 1; index >= 0; index--) {
      element[index].parentNode.removeChild(element[index]);
    }
}

function checkStudentNumberExist(){
  var exists = false;
  //check the validation of form will return false if no input
  var studentNumber = document.getElementsByName('studentNumber')
  studentNumbers  = [].map.call(studentNumber, function( input ) {
        return input.value;
  });
  //checking if student number exists  
      //ajax request for student number if exists
      $.ajax({
        url: '/validate/voter/',
        type: "POST",
        data: {
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        
        success: function (data) {
          var obj = JSON.parse(data)
          if(obj.length != 0){
            var students = document.getElementsByName('studentNumber')
            //compare user inputs to student already save
            $.each(JSON.parse(data), function (key, value){
              //loop each with key and value
              if(studentNumbers.indexOf(value.fields.student_number) > -1){
                for (var i = 0; i < students.length; i++) {
                  if(students[i].value == value.fields.student_number){
                    var html = '';
                    //change border to red if duplicate or exists
                    //append small text
                    students[i].style.borderColor = "red";
                    html += '<small name="studentDuplicate" style="color: red;">student number already exists </small>' 
                    $(students[i]).after(html);
                    exists = true;
                  } else {
                    //remove border
                if(students[i].style.borderColor == "red"){
                  students[i].style.removeProperty('border');  
                } 
                  }
                }
              }
            }); 
          }
          validate(exists);//validate first existing number
        }
      });
    }


function checkStudentNumber(form){ //check student number for login and update
  var input = document.getElementById('studentNumber')
  var error = document.getElementById('error')
  var student = input.value;
  var voterForm = document.getElementById('sscVoter');
  var valid = voterForm.checkValidity();
  var check = false;
  if(valid){
    event.preventDefault();
  $.ajax({
        url: '/check/student_number/voter/',
        type: "POST",
        data: {
          'studentNumber' :student,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
          if(data.is_taken){
            $('#error').attr('hidden', false); //student number exists true
            return false;  
          } else {
            $('#error').attr('hidden', true); //false no student number
            form.checkBtn.disabled = true;
            form.submit();
            return true;
          }
        }
      });
  }

}

//check button click if twice
function checkForm(form) // Submit button clicked
  {
    //
    // check form input values
    //

    form.checkBtn.disabled = true;
    form.checkBtn.value = "Please wait...";
    form.submit();
    return true;
  }

//


let tempPosition = [];
let basePosition = [];

  function setOptionPosition(positionName){
  
  //get the selected option
  $('#addVoter option').each(function(){
    if($(this).text() != ""){
      var setJson = JSON.stringify($(this).val());
      var text = $(this).val();
      var obj = JSON.parse(text);
        if (positionName == obj["name"]) {
          tempPosition.push($(this).val());
      }
    }
  });
}
  
//remove specific position input
  $(document).on('click', '#removePosition', function(){
    $(this).closest('tr').remove();
    if (tempPosition.length == 0) {
      document.getElementById("saveVoter").disabled=true;
    }
  });

//update option select dropdown
function getPosition(id){
   $('#addVoter').empty()  
  //remove temp positions
  for (var i = 0; i < tempPosition.length; i++) {
      var obj = JSON.parse(tempPosition[i])
      if (obj["id"] == id) {
        tempPosition.splice(i, 1);
        break;
    }
  }

  $('#addVoter').append($('<option>', {
      text: ""
    }));

  for (var i =  0; i < basePosition.length ; i++) {
    if(jQuery.inArray(basePosition[i], tempPosition) == -1){
      var obj = JSON.parse(basePosition[i]);
    $('#addVoter').append($('<option>', {
      value: basePosition[i],
      text: obj["name"]
    }));
    }
  }
}


$(document).ready(function(){
  $('#addVoter option').each(function(){
    if($(this).text() != ""){
      basePosition.push($(this).val());
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
  modal.find('.text-name').text('Candidate Name: ' + recipient)
}); 


$('#staticDeleteDisqualify').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  var url = button.data('url')
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('#delete-dis-modal').attr('action', url)
  modal.find('.text-name').text('Candidate Name: ' + recipient)
}); 

$('#staticDisqualify').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  var url = button.data('url')
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('#disqualify-modal').attr('action', url)
  modal.find('.text-name').text('Candidate Name: ' + recipient)
}); 

$('#staticUndisqualify').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  var url = button.data('url')
  var setJson = JSON.stringify(recipient);
  var obj = JSON.parse(setJson)
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('#undisqualify-modal').attr('action', url)
  modal.find('#delete-modal').attr('action', url)
  modal.find('#disqualify_name').attr('value', obj.name)
  modal.find('#disqualify_position').attr('value', obj.position)
  modal.find('#disqualify_id').attr('value', obj.id)
  modal.find('.text-name').text('Candidate Name: ' + obj.name)
});     


$('#staticBackdropVoter').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  var url = button.data('url')
  var setJson = JSON.stringify(recipient);
  var obj = JSON.parse(setJson)
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('#sscVoter').attr('action', url)
  modal.find('#partyName').attr('value', obj.first)
  modal.find('#acronym').attr('value', obj.second)
  modal.find('#first').text('Current name: '+ obj.first)
  modal.find('#second').text('Current student #: '+ obj.second)
}); 


$('#staticEditPartylist').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  var url = button.data('url')
  var setJson = JSON.stringify(recipient);
  var obj = JSON.parse(setJson)
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('#update-modal-partylist').attr('action', url)
  modal.find('#partyName').attr('value', obj.first)
  modal.find('#acronym').attr('value', obj.second)
  modal.find('#first').text('Current party: '+ obj.first)
  modal.find('#second').text('Current acronym: '+ obj.second)
}); 

$('#staticDeletePartylist').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  var url = button.data('url')
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('#delete-modal-partylist').attr('action', url)
  modal.find('.modal-body p').text('Party Name: ' + recipient)
});     


$(document).ready(function () {
var unsaved = false;
 $('.save').click(function() {
    unsaved = false;
});

var unsaved = false;
 $('.delete').click(function() {
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
  //   $("#sscForm").submit(function(){
  //     var flag = 0
  //     var electionType = document.getElementById('electionTypeId').value;
  //     var extra = document.getElementsByName("extras"),
  //     extras  = [].map.call(extra, function( input ) {
  //         return input.value;
  //     });
  //     var candidateName = document.getElementsByName('candidate_name'),
  //     candidateNames  = [].map.call(candidateName, function( input ) {
  //         return input.value;
  //     });
  //     var collegeId = document.getElementsByName("collegeId"),
  //     collegeIds  = [].map.call(collegeId, function( input ) {
  //         return input.value;
  //     });
   
  
  // var getValue;
  //   for (var i = 0; i < candidateNames.length; i++) {
  //     if(candidateNames[i] != ''){
  //       flag++;
  //       break;
  //     }
  //   }

  //     var jsonFormId = [];
  //   $("option:selected").each(function() {
  //     jsonFormId.push($(this).val())
  //     //var getValue = $.parseJSON($(this).val())
  // });

  //     for (i=0; i < collegeIds.length; i++) {
  //       jsonFormId.push(collegeIds[i])
  //   }
  //   var x = candidateNames.length;
  //   for (i = x - 1; i >= 0; i--) {
  //     if (candidateNames[i] == '') {
  //       candidateNames.splice(i, 1);
  //       jsonFormId.splice(i, 1);
  //     }
  //   }
    
    
  //       $.ajax({
  //       type:'POST',
  //       url:'/save/',
  //       data: {
  //         'ElectionType': electionType,
  //         'CandidateNames[]': candidateNames,
  //         'Ids[]': jsonFormId,
  //         'Extras[]': extras,
  //         csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
  //         action: 'post'
  //       },
  //       success:function(data){
  //         var partyName = data.partyName;
  //         var partyId = data.partyId;
  //         var url = "view/election/view_partylist"
  //         var origin_url = window.location.origin
  //        location.href = origin_url+"/"+url+"/"+partyName+"/"+partyId;
  //       }
  //     });
    
  // });

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

  $(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

