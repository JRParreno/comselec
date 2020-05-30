//check button click if twice
function checkForm(form) // Submit button clicked
  {
    //
    // check form input values
    //

    form.checkBtn.disabled = true;
    form.checkBtn.value = "Please wait...";
    form.submit();
    return false;
  }

$("#loginPoll").click(function(e){
  var valid = this.form.checkValidity();
  if(valid){
    event.preventDefault();   //stops the "normal" form request
    removeSmallText();
    checkStudentNumberExist(); //check student number exists  
  }
});

function removeSmallText(){
   //remove all by tag name 'small'
    var element = document.getElementsByTagName("small"), index;
    for (index = element.length - 1; index >= 0; index--) {
      element[index].parentNode.removeChild(element[index]);
    }
    var element1 = document.getElementsByClassName("voter-info"), index;
    for (index = element1.length - 1; index >= 0; index--) {
      element1[index].parentNode.removeChild(element1[index]);
    }
}

function checkStudentNumberExist(){
  //check the validation of form will return false if no input
  var students = document.getElementsByName('student_number')
  var voter_name = document.getElementsByName('voter_name')
  var selected_cisc = document.getElementsByName('selected')
  var election = document.getElementsByName('election_id')
  //checking if student number exists  
      //ajax request for student number if exists
      var obj = JSON.parse(selected_cisc[0].value)
      
      $.ajax({
        url: '/validate/voter/check/cisc',
        type: "POST",
        data: {
			'student_number': students[0].value,
			'voter_name': voter_name[0].value,
			'college_id': obj.id,
      'election_id': election[0].value,
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        
        success: function (data) {
        	checkStudentInfo(data);
        }
      });

    }

function checkStudentInfo(data){
	var exists = false;
	var html = '';
  var election = document.getElementsByName('election_id')
        if(data.check.length > 0){
          	if(data.vote.length > 0){
                for (var i = 0; i < data.vote.length; i++) {             
                if(data.vote[i].election = election[0].value){
                  html += '<small name="studentDuplicate" class="font-weight-bold" style="color: red;">error student already voted!</small>' 
                  $('#errorLogin').append(html);
                  exists = true;
                  break;
                }
              }
            }
        } else {
            html += '<small name="studentDuplicate" class="font-weight-bold" style="color: red;">error please check your credentials!</small>' 
            $('#errorLogin').append(html);
            exists = true;
        }
      validate(exists);//validate first existing number
}

function validate(exists){
  var form = document.querySelector('form');
  var students = document.getElementsByName('student_number')
  var ajaxVoter = document.getElementsByName('ajax_voter')
  if(!exists){
    //checkForm(form);//checking form to submit
    $.ajax({
        url: '/election/voter_login/get_voter/' + ajaxVoter[0].value,
        type: "POST",
        data: {
          'student_number': students[0].value,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        
        success: function (data) {
          var obj = JSON.parse(data)
          	var html = ''
          	html += '<li class="list-group-item voter-info" style="color: #212529"><span class="font-weight-bold">Student Name:'
  			html += '</span> '+obj.student_name+'</li>'
  			html += '<li class="list-group-item voter-info" style="color: #212529"><span class="font-weight-bold">Student Number:'
  			html += '</span> '+obj.student_number+'</li>'
  			html += '<li class="list-group-item voter-info" style="color: #212529"><span class="font-weight-bold">Position:'
  			html += '</span> '+obj.position+'</li>'
  			html += '<li class="list-group-item voter-info" style="color: #212529"><span class="font-weight-bold">College:'
  			html += '</span> '+obj.college+'</li>'
  			
  			$('.list-group').append(html)
          // for (var i = 0; i < ob.length; i++) {
          // 	Things[i]
          // }
        }
      });

    $("#staticBackdrop").modal();
  	
  }
}

$('#loginBtn').click(function(){
	var form = document.querySelector('form');
	checkForm(form);
});

