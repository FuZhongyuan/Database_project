
// document.addEventListener('DOMContentLoaded', function () {
//     var mouse = document.querySelector('.mouse');
//     window.addEventListener('mousemove', function (event) {
//         mouse.style.left = event.clientX - mouse.offsetWidth / 2 + 'px';
//         mouse.style.top = event.clientY - mouse.offsetHeight / 2 + 'px';
//     });
// });
function updateMousePosition() {
    var mouse = document.querySelector('.mouse');
    var mouseX = 0;
    var mouseY = 0;

    function moveMouse(event) {
        mouseX = event.clientX;
        mouseY = event.clientY;
    }

    function animateMouse() {
        var mouseXOffset = mouseX - mouse.offsetWidth / 2;
        var mouseYOffset = mouseY - mouse.offsetHeight / 2;
        mouse.style.left = mouseXOffset + 'px';
        mouse.style.top = mouseYOffset + 'px';
        requestAnimationFrame(animateMouse);
    }

    document.addEventListener('mousemove', moveMouse);
    requestAnimationFrame(animateMouse);
}
function logoff(role_id) {
    $('#logoff').click(function (event) {
        var $this = $(this);
        console.log($this);
        event.preventDefault();
        // 获取输入框的值
        // var inputEmail = $('#email').val();
        // var user_id = $this.attr("value");
        // var role_id = parseInt($this.attr("value"));
        // console.log(user_id);
        // 获取URL
        var logoff_listUrl = document.getElementById('logoff_link').dataset.url;
        var data = {
            // inputEmail: inputEmail,
            // role_id: role_id
        };
        alert("修改成功");
        zlajax.post({
            url: "/user/logoff",
            data: data,
        })
            .done(function (data) {
                setTimeout(function () {
                    // window.location.reload();
                    window.location.href = logoff_listUrl;
                }, 2000);
            })
            .fail(function (error) {
                alert(error.message);
            });
    });
}

$(function () {
  updateMousePosition();
  logoff();
});
