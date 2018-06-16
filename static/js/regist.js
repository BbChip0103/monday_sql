$(".login-form").validate({
  rules: {
    university : {
      required: true
    },
    mobile:{
      required: true,
      minlength: 10,
      remote: {
        type: 'post',
        url: '/user/register/check_phone_number'
      }
    },
    username: {
      required: true,
      maxlength: 10
    },
    password: {
      required: true,
      minlength: 5
    },
    cpassword: {
      required: true,
      minlength: 5,
      equalTo: password
    },
    sex: {
      required : true
    }
  },
  //For custom messages
  messages: {
    university:{
      required: "필수로 입력하세요"
    },
    mobile: {
      required : "필수로 입력하세요",
      minlength : "최소 {0}글자이상이어야 합니다",
      remote : "존재하는 핸드폰번호입니다"
    },
    username: {
      required : "필수로입력하세요",
      maxlength : "최대 {0}글자이하이어야 합니다"
    },
    password: {
      required : "필수로입력하세요",
      minlength : "최소 {0}글자이상이어야 합니다"
    },
    cpassword: {
      required : "필수로입력하세요",
      minlength : "최소 {0}글자이상이어야 합니다",
      equalTo : "비밀번호가 일치하지 않습니다."
    },
    sex: {
      required : "필수로입력하세요"
    },
  },
  errorElement : 'div',
  errorPlacement: function(error, element) {
    var placement = $(element).data('error');
    if (placement) {
      $(placement).append(error)
    } else {
      error.insertAfter(element);
    }
  }
});
