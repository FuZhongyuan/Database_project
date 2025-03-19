// 检查表单提交时邮箱地址的格式是否正确
function validateForm() {
    $("#exampleInputEmail1").blur(function() {
        var $this = $(this);
        var emailField = document.getElementById('exampleInputEmail1');
        var emailValue = emailField.value;

        // 使用正则表达式检查邮箱地址的格式
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailValue)) {
            // 如果邮箱地址格式不正确，显示弹窗提示用户
            alert("邮箱格式错误!");
            // 阻止表单提交
            return false;
        }
        // 取消光标选中
        $this.blur();
    });
}


// 检查密码是否符合要求
function validatePassword() {
    $("#exampleInputPassword1").blur(function() {
        var $this = $(this);
        // 密码长度应该在6到20位之间
        var password = document.getElementById('exampleInputPassword1').value;
        if (password.length >= 6 && password.length <= 20) {

        } else {
            alert("密码长度应该在6到20位之间");
            return false;
        }
        // 取消光标选中
        $this.blur();
    });
}

function validatePasswordConfirm() {
    $("#exampleInputPassword_confirm1").blur(function() {
        var $this = $(this);
        // 密码长度应该在6到20位之间
        var password = document.getElementById('exampleInputPassword_confirm1').value;
        if (password.length >= 6 && password.length <= 20) {

        } else {
            alert("验证密码长度应该在6到20位之间");
            return false;
        }
        // 取消光标选中
        $this.blur();
    });
}
// 检查验证码是否符合要求
function validateVerificationCode() {
    $("#exampleInputVerification").blur(function() {
        var $this = $(this);
        // 验证码长度应该为6位
        var verificationCode = document.getElementById('exampleInputVerification').value;
        if (verificationCode.length === 6) {

        } else {
            alert("验证码长度应该为6位");
            return false;
        }
        // 取消光标选中
        $this.blur();
    });
}

// 检查用户名是否符合要求
function validateUsername() {
    $("#exampleInputUsername1").blur(function() {
        var $this = $(this);
        // 用户名长度应该在2到20位之间
        var username = document.getElementById('exampleInputUsername1').value;
        if (username.length >= 2 && username.length <= 20) {

        } else {
            alert("用户名长度应该在2到20位之间");
            return false;
        }
        // 取消光标选中
        $this.blur();
    });
}

// 当整个网页加载完成后执行以下代码
$(function () {
    // 调用 bindEmailCaptchaClick 函数，为按钮绑定点击事件
    validateForm();
    validatePassword();
    validateVerificationCode();
    validateUsername();
    validatePasswordConfirm();
});

// 在表单提交时调用 validateForm 函数
// document.getElementById('myForm').addEventListener('submit', function(event) {
//     // 阻止默认的表单提交行为
//     event.preventDefault();
//     // 调用 validateForm 函数进行验证
//     if (validateForm()&&validatePassword()&&validateVerificationCode()&&validateUsername()) {
//         // 如果验证通过，发送表单数据到服务器
//         var formData = new FormData(this);
//         fetch('/register', {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => {
//             // 检查响应是否成功
//             if (response.ok) {
//                 // 响应成功，检查 JSON 响应中是否存在 validation_failed 标识
//                 return response.json();
//             } else {
//                 // 响应失败，抛出异常
//                 throw new Error('网络错误');
//             }
//         })
//         .then(data => {
//             // 检查 JSON 响应中是否存在 validation_failed 标识
//             if (data.validation_failed) {
//                 // 如果存在 validation_failed 标识，触发弹窗提示用户
//                 alert("表单验证失败，请检查您的输入!");
//             } else {
//                 // 如果不存在 validation_failed 标识，可以执行其他操作，比如重定向到其他页面
//                 window.location.href = '../../blueprints/auth.register'; // 重定向到成功页面
//             }
//         })
//         .catch(error => {
//             // 捕获网络错误，并提示用户
//             console.error('发生错误:', error);
//             alert('发生错误，请稍后重试');
//         });
//     }
// });
