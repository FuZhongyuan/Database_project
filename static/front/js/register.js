function captchaBtnClickEvent(event) {
  event.preventDefault();
  var $this = $(this);

  // 获取邮箱
  var email = $("input[name='email']").val();
  var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
  if (!email || !reg.test(email)) {
    alert("请输入正确格式的邮箱！");
    return;
  }

  zlajax.get({
    url: "/user/mail/captcha?mail=" + email
  }).done(function (result) {
    alert("验证码发送成功！");
  }).fail(function (error) {
    alert(error.message);
  })
}

function bindEmailCaptchaClick() {
    // 为 id 为 captcha-btn 的按钮添加点击事件处理函数
    $("#captcha-btn").click(function (event) {
        // this: 代表当前按钮的 jQuery 对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();

        // 获取名为 email 的输入框的值
        var email = $("input[name='email']").val();
        // 发起 AJAX 请求，向服务器发送请求
        $.ajax({
            url: "/user/captcha/email?email=" + email,
            method: "GET",
            success: function (result) {
                // 从返回结果中获取 code
                var code = result['code'];
                // 如果 code 为 200，则表示请求成功
                if (code == 200) {
                    // 设置倒计时初始值为 60 秒
                    var countdown = 60;
                    // 开始倒计时之前，取消按钮的点击事件
                    $this.off("click");
                    // 设置定时器，每隔一秒执行一次
                    var timer = setInterval(function () {
                        // 更新按钮的文本为倒计时的剩余秒数
                        $this.text(countdown);
                        // 倒计时减少一秒
                        countdown -= 1;
                        // 倒计时结束时执行
                        if (countdown <= 0) {
                            // 清除定时器
                            clearInterval(timer);
                            // 恢复按钮文本为 "获取验证码"
                            $this.text("获取验证码");
                            // 重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000); // 间隔为 1 秒
                    // 在成功发送验证码后显示成功消息
                    $("#success-message").text("邮箱验证码发送成功!").show();
                    // 3 秒后隐藏成功消息
                    setTimeout(function () {
                        $("#success-message").hide();
                    }, 3000);
                } else {
                    // 如果请求不成功，则弹出错误消息
                    alert(result['message']);
                }
            },
            error: function (error) {
                // 如果请求出错，则在控制台打印错误信息
                console.log(error);
            }
        });
    });
}

// $(function () {
//   $('#captcha-btn').on("click",function(event) {
//     event.preventDefault();
//     // 获取邮箱
//     var email = $("input[name='email']").val();
//
//     zlajax.get({
//       url: "/user/mail/captcha?mail=" + email
//     }).done(function (result) {
//       alert("验证码发送成功！");
//     }).fail(function (error) {
//       alert(error.message);
//     })
//   });
//   bindEmailCaptchaClick();
// });
$(function () {
  bindEmailCaptchaClick();
});