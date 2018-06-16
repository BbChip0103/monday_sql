$(document).ready(function(){
	//validate letter
	$(".loginForm").validate({
		rules: {
			mobile:{
				required: true,
				minlength: 10,
				remote: {
					type: 'post',
					url: 'login/is_exist_phone_number'
				}
			},
			password:{
				required: true,
				minlength: 5
			}
		},
		//For custom messages
		messages: {
			mobile: {
				required : "필수로 입력하세요",
				minlength : "010XXXXXXXX 형식으로 입력하세요.",
				remote : "등록되지 않은 핸드폰번호입니다"
			},
			password: {
				required : "필수로 입력하세요",
				minlength : "{0}글자 이상이어야 합니다"
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
});
