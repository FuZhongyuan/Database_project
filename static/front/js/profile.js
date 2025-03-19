function show_comments() {
    $('#comment-state-btn').click(function (event) {
        var $this = $(this);
        console.log($this);
        event.preventDefault();
        // var user_id = $this.attr("value");
        // var role_id = parseInt($this.attr("value"));
        // console.log(user_id);
        var data = {
            // user_id: user_id,
            // role_id: role_id
        };
        alert("查询用户评论成功")
        window.location.href = '/view/user_comments_view';

        // zlajax.get({
        //     url: "/user_comments_view",
        //     data: data,
        // })
            // .done(function (data) {
            //     // setTimeout(function () {
            //         // window.location.reload();
            //     // }, 2000);
            // })
            // .fail(function (error) {
            //     alert(error.message);
            // });
    });
}



$(function () {
  show_comments();
});