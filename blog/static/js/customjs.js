$(".scroll-down").click(function() {
    $('html,body').animate({
        scrollTop: $(".form-col").offset().top},
        'slow');
});


var postForm = $('.comment-form')
var postFormMethod = postForm.attr('method')
var postFormEndPoint = postForm.attr('action')
var endpoint = 'http://127.0.0.1:8000/api/blog/'
var dataUrl = $(".load-comments").attr("data-url")

var commentCount = $('.comment-count')
x = commentCount.text()
console.log(commentCount)
getComments(dataUrl)
 $(".load-comments").after("<div class='form-container'></div>")

function displaySubmitting(submitBtn, defaultText, doSubmit){
  if (doSubmit){
    submitBtn.addClass("disabled")
    submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
  } else{
    submitBtn.removeClass("disabled")
    submitBtn.html(defaultText)
  }
}

function generateForm(){
      var html_ = "<form method='POST' class='comment-form'>" +
        "<textarea class='form-control' placeholder='Your comment...' name='text'></textarea><br/>" +
        "<input type='hidden' name='csrfmiddlewaretoken' value='" + csrftoken + "'>" +
        "<button type='submit' class='save btn btn-default'>Save</button></form>"
      return html_
    }

function handleForm(formData){
  var postFormSubmitBtn = postForm.find("[type='submit']")
  var postFormSubmitBtnTxt = postFormSubmitBtn.text()
  var postFormData = postForm.serialize()
  var thisForm = $(this)
  displaySubmitting(postFormSubmitBtn, "", true)
  $.ajax({
    method: "POST",
    url: endpoint + "create/",
    data: formData + "&url=" + dataUrl,
    success: function(data){
      getComments(dataUrl)
      $(".load-comments").html('')

      var formHtml = generateForm()
      $(".form-container").html(formHtml)


      setTimeout(function(){
        displaySubmitting(postFormSubmitBtn, postFormSubmitBtnTxt, false)
      }, 2000)
    },
    error: function(error){
      console.log(error.responseJSON)
      alert('error')
      setTimeout(function(){
        displaySubmitting(postFormSubmitBtn, postFormSubmitBtnTxt, false)
      }, 2000)
    }
  })
}

$(document).on('submit', '.comment-form', function(e){
  e.preventDefault()
  var formData = $(this).serialize()
  console.log(formData)
  handleForm(formData)
  $('.abc').click(function(){
    object.approved_comments == true
  });
})

  function getComments(requestUrl){
    $.ajax({
      method: "GET",
      url: endpoint,
      data: {
        url: requestUrl,
      },
      success: function(data){
        console.log(data.length)
        if (data.length > 0){
          commentBody(data)
        }
        var formHtml = generateForm()
        $(".form-container").html(formHtml)

        var commentCount = $('.comment-count')
        commentCount.text(data.length)

        var com = $(".comment-count-list")
        com.text(data.length)

      },
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  }

function commentBody(data){
  $.each(data, function(index, object){
    $(".load-comments").append(object.text + "<br>")

    if(object.approved_comments == false){
    $(".load-comments").append("<br><a class='btn btn-default' href='http://127.0.0.1:8000/comment/" + object.id + "/remove/'>"+
  "<span class='glyphicon glyphicon-remove'>no</span></a><a class='btn btn-default'" +
  "href='http://127.0.0.1:8000/comment/" + object.id + "/approve/'><span class='glyphicon glyphicon-ok'>ok</span></a>")
        }

    if(object.user.is_superuser == true){
    $(".load-comments").append("<a href='http://127.0.0.1:8000/comment/" + object.id + "/remove/'><span class='glyphicon glyphicon-remove'></span></a>")
        }

    $(".load-comments").append("<p><small>Posted by: <strong>" + object.user.username + "</strong> on " + object.created_date + "</small></p><hr>")
  })
}
