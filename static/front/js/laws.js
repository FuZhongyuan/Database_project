/* 获取底层盒子main元素 */
var main = document.querySelector('.main');
/* 得到main的宽度 */
let width = main.offsetWidth;
/* 得到main的高度 */
let height = main.offsetHeight;
/* 建一个颜色数组，放上几种颜色 */
let color = ["#BBFF00", "#FF3333", "#FFFF77", "#0044BB", "#FF77FF", "#99FFFF", "#DDDDDD", "#FF44AA"];
/*  计算一行需要多少的小圆圈，圆圈是20*20的 */
let chuang = Math.floor(width / 20);
/*  计算一列需要多少的小圆圈 */
let kuan = Math.floor(height / 20);
/* 圆圈的总数 */
let zong = chuang * kuan;
/*   循环添加全部圆圈 */
for (let i = 1; i < zong; i++) {
    /* 创建div盒子 */
    let dot = document.createElement('div');
    /* 给新建的盒子添加类名为.dot的选择器 */
    dot.classList.add('dot');
    /* 给新建的盒子添加一个随机颜色 */
    dot.style.cssText = ` --color: ${color[Math.floor(Math.random() * 8)]}; `
    /* 给底层盒子main添加这个新建的div */
    main.appendChild(dot);
}