// // function deleteBoard() {
// //     // 为 id 为 captcha-btn 的按钮添加点击事件处理函数
// //     $('.delete-board-btn').click(function (event) {
// //         // this: 代表当前按钮的 jQuery 对象
// //         var $this = $(this);
// //         // 阻止默认的事件
// //         event.preventDefault();
// //         var board_id = $this.attr("data-board-id"); //这个代码获取了按钮的id值
// //         var data = {
// //             board_id: board_id
// //         }
// //         zlajax.post({
// //             url: "/cms/board/delete/" + board_id,
// //             data: data
// //         })
// //             .done(function (data) {
// //                 setTimeout(function () {
// //                     // window.location = "/";
// //                     window.location.reload();
// //                 }, 2000);
// //             }).fail(function (error) {
// //             alert(error.message);
// //         });
// //     });
// // }
// function editStaff(ab) {
//     // 为 id 为 captcha-btn 的按钮添加点击事件处理函数
//     $('.active-btn').click(function (event) {
//         console.log('选中的角色ID是：', ab);
//         // this: 代表当前按钮的 jQuery 对象
//         var $this = $(this);
//         // 阻止默认的事件
//         event.preventDefault();
//         var user_id = $this.attr("user_id"); //这个代码获取了按钮的id值
//         var role_id = parseInt($this.attr("role_id")); //这个代码获取了按钮的id值
//         var data = {
//             user_id: user_id,
//             role_id:a
//         }
//         zlajax.post({
//             url: "/cms/staff/edit1/" + user_id,
//             data: data,
//
//         })
//             .done(function (data) {
//                 setTimeout(function () {
//                     // window.location = "/";
//                     window.location.reload();
//                 }, 2000);
//             }).fail(function (error) {
//             alert(error.message);
//         });
//     });
// }
// function get_role_id(){
//     var a;
//     // $('.role').click(function (event){
//     //     var $this = $(this);
//     //     // 阻止默认的事件
//     //     event.preventDefault();
//     //     var role_id = $this.attr("role_id"); //这个代码获取了按钮的id值
//     //     var data = {
//     //         role_id: role_id
//     //     }
//     //     a=role_id;
//     // });
//     // var firstdirectory=$("#form-check-inline").datagrid("getSelected");
//     // 绑定带有 checked 属性的单选按钮
//     $('input[type="radio"][checked]').click( function(event) {
//         // 在这里执行您的操作
//         // 阻止默认的事件
//         var $this = $(this);
//         // event.preventDefault();
//         var role_id = parseInt($this.attr("value")); //这个代码获取了按钮的id值
//         a=role_id;
//         console.log('选中的角色ID是：', a);
//     });
//
//
//     // 绑定没有 checked 属性的单选按钮
//     $('input[type="radio"]:not([checked])').click( function(event) {
//         // 在这里执行您的操作
//         // 阻止默认的事件
//         var $this = $(this);
//         // event.preventDefault();
//         var role_id = parseInt($this.attr("value")); //这个代码获取了按钮的id值
//         a=role_id;
//         console.log('选中的角色ID是：', a);
//     });
//     return a; // 返回存储的角色ID
// }
//
// // 当整个网页加载完成后执行以下代码
// $(function () {
//     // 调用 bindEmailCaptchaClick 函数，为按钮绑定点击事件
//     // deleteBoard();
//     // get_role_id();
//     editStaff(get_role_id());
//
// });


// function editStaff(role_id) {
//     $('.active-btn').click(function (event) {
//         console.log('选中的角色ID是：', role_id);
//         var $this = $(this);
//         event.preventDefault();
//         var user_id = $this.attr("myuser_id");
//         var data = {
//             user_id: user_id,
//             role_id: role_id
//         }
//         zlajax.post({
//             url: "/cms/staff/edit1/" + user_id,
//             data: data,
//         })
//             .done(function (data) {
//                 setTimeout(function () {
//                     window.location.reload();
//                 }, 2000);
//             }).fail(function (error) {
//             alert(error.message);
//         });
//     });
// }
function editStaff(role_id) {
    $('#submit').click(function (event) {
        var $this = $(this);
        console.log($this);
        event.preventDefault();
        var user_id = $this.attr("value");
        // var role_id = parseInt($this.attr("value"));
        console.log(user_id);
        var data = {
            user_id: user_id,
            role_id: role_id
        };
        alert("修改成功");
        zlajax.post({
            url: "/cms/staff/edit1/" + user_id,
            data: data,
        })
            .done(function (data) {
                setTimeout(function () {
                    window.location.reload();
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


function get_isstaff(callback) {
    $('input[name="is_staff"][checked]').click(function (event) {
        var $this = $(this);
        var isstaff = parseInt($this.attr("value"));
        console.log('选中的角色ID是：', isstaff);
        callback(isstaff); // 调用回调函数，并传递选中的角色ID
    });

    $('input[name="is_staff"]:not([checked])').click(function (event) {
        var $this = $(this);
        var isstaff = parseInt($this.attr("value"));
        console.log('选中的角色ID是：', isstaff);
        callback(isstaff); // 调用回调函数，并传递选中的角色ID
    });
}
function editStaff2(isstaff) {
    $('#submit').click(function (event) {
        var $this = $(this);
        console.log($this);
        event.preventDefault();
        var user_id = $this.attr("value");
        // var role_id = parseInt($this.attr("value"));
        console.log(user_id);
        var data = {
            user_id: user_id,
            isstaff: isstaff
        };
        alert("这个修改成功");
        zlajax.post({
            url: "/cms/staff/edit2/" + user_id,
            data: data,
        })
            .done(function (data) {
                setTimeout(function () {
                    window.location.reload();
                }, 2000);
            })
            .fail(function (error) {
                alert(error.message);
            });
    });
}


$(function () {
    get_role_id(function (role_id) {
        editStaff(role_id);
    });

    get_isstaff(function (isstaff) {
        editStaff2(isstaff);
    });
});


