function hidden_post(){
        $(".active-btn").click(function (event) {
        event.preventDefault();
        var $this = $(this);
        var is_active = parseInt($this.attr("data-active"));
        var message = is_active ? "您确定要禁用此帖子吗？" : "您确定要取消禁用此帖子吗？";
        var post_id = $this.attr("data-post-id");
        var result = confirm(message);
        if (!result) {
            return;
        }
        var data = {
            is_active: is_active ? 0 : 1
        }
        console.log(data);
        zlajax.post({
            url: "/cms/posts/active/" + post_id,
            data: data
        }).done(function () {
            window.location.reload();
        }).fail(function (error) {
            alert(error.message);
        })
    });
}

function editPost() {
        // 为 id 为 captcha-btn 的按钮添加点击事件处理函数
    $('.edit-post-btn').click(function (event) {
        // this: 代表当前按钮的 jQuery 对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();
        var post_id = $this.attr("data-post-id"); //这个代码获取了按钮的id值
        var data = {
            post_id: post_id
        }
        // zlajax.post({
        //     url: "/cms/boards/change_name/" + board_id,
        //     data: data
        // })
        window.location.href = "/cms/post/change/" + post_id;
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

$(function () {
    hidden_post()
    editPost()
});