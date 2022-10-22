$(document).ready(function(){
    $(".siderbar_menu li").click(function(){
        $(".siderbar_menu li").removeClass("active");
        $(this).addClass("active");
    })
    $(".hamburger").click(function(){
        $(".wrapper").addClass("active");
    })
    $(".bg_shadow,.close").click(function(){
        $(".wrapper").removeClass("active");
    })
})

function Uploadbingli(){
    alert("病历提交成功")
}