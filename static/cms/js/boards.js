function deleteBoard() {
    // 为 id 为 captcha-btn 的按钮添加点击事件处理函数
    $('.delete-board-btn').click(function (event) {
        // this: 代表当前按钮的 jQuery 对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();
        var board_id = $this.attr("data-board-id"); //这个代码获取了按钮的id值
        var data = {
            board_id: board_id
        }
        zlajax.post({
            url: "/cms/board/delete/" + board_id,
            data: data
        })
            .done(function (data) {
                setTimeout(function () {
                    // window.location = "/";
                    window.location.reload();
                }, 2000);
            }).fail(function (error) {
            alert(error.message);
        });
    });
}

function editBoard() {
    // 为 id 为 captcha-btn 的按钮添加点击事件处理函数
    $('.edit-board-btn').click(function (event) {
        // this: 代表当前按钮的 jQuery 对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();
        var board_id = $this.attr("data-board-id"); //这个代码获取了按钮的id值
        var data = {
            board_id: board_id
        }
        // zlajax.post({
        //     url: "/cms/boards/change_name/" + board_id,
        //     data: data
        // })
        window.location.href = "/cms/boards/change_name/" + board_id;
            // .done(function (data) {
            //     setTimeout(function () {
            //         // window.location = "/";
            //         window.location.reload();
            //     }, 2000);
            // }).fail(function (error) {
            // alert(error.message);
        });
    // });
}


// 当整个网页加载完成后执行以下代码
$(function () {
    // 调用 bindEmailCaptchaClick 函数，为按钮绑定点击事件
    deleteBoard();
    editBoard()
});
