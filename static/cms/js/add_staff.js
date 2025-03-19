function editStaff(role_id) {
    $('#submit').click(function (event) {
        var $this = $(this);
        console.log($this);
        event.preventDefault();
        // 获取输入框的值
        var inputEmail = $('#email').val();
        var user_id = $this.attr("value");
        // var role_id = parseInt($this.attr("value"));
        console.log(user_id);
        // 获取URL
        var staff_listUrl = document.getElementById('staff_list_link').dataset.url;
        var data = {
            inputEmail: inputEmail,
            role_id: role_id
        };
        alert("修改成功");
        zlajax.post({
            url: "/cms/staff/add_role",
            data: data,
        })
            .done(function (data) {
                setTimeout(function () {
                    // window.location.reload();
                    window.location.href = staff_listUrl;
                }, 2000);
            })
            .fail(function (error) {
                alert(error.message);
            });
    });
}

function get_role_id(callback) {
    $('input[name="role"][checked]').click(function (event) {
        var $this = $(this);
        var role_id = parseInt($this.attr("value"));
        console.log('选中的角色ID是：', role_id);
        callback(role_id); // 调用回调函数，并传递选中的角色ID
    });

    $('input[name="role"]:not([checked])').click(function (event) {
        var $this = $(this);
        var role_id = parseInt($this.attr("value"));
        console.log('选中的角色ID是：', role_id);
        callback(role_id); // 调用回调函数，并传递选中的角色ID
    });
}



$(function () {
    get_role_id(function (role_id) {
        editStaff(role_id);
    });
});