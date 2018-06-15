//为id=input_name绑定光标离开事件
$('#input_name').on('blur', function () {
//向后端发送ajax请求
    $.ajax({
        url:{% url 'register_ajax' %},
//       /register_ajax/,   #}
        type:'POST',
        data:{'username':$('#input_name').val()},
        success:function (msg) {
//{#                将接收到的回复信息显示在span标签中#}
            $('#error_name').text(msg)
        }
    })
})