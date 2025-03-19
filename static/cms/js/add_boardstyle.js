function add_borad(role_id) {
    $('#submit').click(function (event) {
        var $this = $(this);
        console.log($this);
        event.preventDefault();
        // 获取输入框的值
        var BoardName = $('#category_name').val();
        // var user_id = $this.attr("value");
        // var role_id = parseInt($this.attr("value"));
        console.log(BoardName);
        // 获取URL
        var boardUrl = document.getElementById('board-link').dataset.url;

        var data = {
            BoardName: BoardName,
            // role_id: role_id
        };
        alert("修改成功");
        zlajax.post({
            url: "/cms/board/add_board",
            data: data,
        })
            .done(function (data) {
                setTimeout(function () {
                    // window.location.reload();
                    // 使用URL跳转
                    window.location.href = boardUrl;
                }, 2000);
            })
            .fail(function (error) {
                alert(error.message);
            });
    });
}

$(function () {

    add_borad();
});