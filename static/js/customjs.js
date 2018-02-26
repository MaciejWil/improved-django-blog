$(".scroll-down").click(function() {
    $('html,body').animate({
        scrollTop: $(".form-col").offset().top},
        'slow');
});


var postForm = $('.post-form')
var postFormMethod = postForm.attr('method')
var postFormEndPoint = postForm.attr('action')


function displaySubmitting(submitBtn, defaultText, doSubmit){
  if (doSubmit){
    submitBtn.addClass("disabled")
    submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
  } else{
    submitBtn.removeClass("disabled")
    submitBtn.html(defaultText)
  }

}

postForm.submit(function(event){
  event.preventDefault()

  var postFormSubmitBtn = postForm.find("[type='submit']")
  var postFormSubmitBtnTxt = postFormSubmitBtn.text()

  var postFormData = postForm.serialize()
  // console.log(postFormData)
  var thisForm = $(this)

  // var formText =

  displaySubmitting(postFormSubmitBtn, "", true)
  $.ajax({
    method: postFormMethod,
    url: postFormEndPoint,
    data: postFormData,
    success: function(data){
      console.log(data.comment)
      postForm[0].reset()
      $('.abc').text(data.comment)
      var submitSpan = $('.abc1')

      $.each(data, function(index, object){
       $(".abc").append(submitSpan.html("<a class='btn btn-default' href='{% url 'comment_remove' pk=comment.pk %}'><span class='glyphicon glyphicon-remove'>no</span></a><a class='btn btn-default' href='{% url 'comment_approve' pk=comment.pk %}'><span class='glyphicon glyphicon-ok'>ok</span></a>"))
   })


      setTimeout(function(){
        displaySubmitting(postFormSubmitBtn, postFormSubmitBtnTxt, false)
      }, 2000)


    },
    error: function(error){
      console.log(error.responseJSON)
      alert('error')
      // $.alert({
      //   title: 'Ooops',
      //   content: 'An error occured',
      //   theme: 'modern',
      // })
      setTimeout(function(){
        displaySubmitting(postFormSubmitBtn, postFormSubmitBtnTxt, false)
      }, 2000)
    }
  })
})



function getButtons(){
      $.ajax({
        url: "{% url 'comment_remove' pk=comment.pk %}",
        method: "GET",
        data: 'formData',
        success: function(data){
          var submitSpan = $('.abc')

            submitSpan.html("<a class='btn btn-default' href='{% url 'comment_remove' pk=comment.pk %}'><span class='glyphicon glyphicon-remove'>no</span></a><a class='btn btn-default' href='{% url 'comment_approve' pk=comment.pk %}'><span class='glyphicon glyphicon-ok'>ok</span></a>")


        },
        error: function(errorData){
          alert({
            title: "Oops!",
            content: "An error occurred",
            theme: "modern",
          })
        }
      })

  }
