const container = document.querySelector('#container');
const signInButton = document.querySelector('#signIn');
const signUpButton = document.querySelector('#signUp');

signUpButton.addEventListener('click',() => container.classList.add('right-panel-active'))
signInButton.addEventListener('click',() => container.classList.remove('right-panel-active'))

var str1,str2
var num = new Array();

function valid(){
    str1=document.getElementById("un1").value;
    str2=document.getElementById("pw1").value;
    if(str1=="" || str2==""){
        alert("您输入信息不完整！")
        return 2;
    }
    else{
        return 1;
    }
}

function sendmessage(){
    var v=valid()
    if(v===2){
        alert('注册失败')
    }
    else{
        document.getElementById("useradd").submit();
        alert("注册成功")
        window.open('http://localhost:5000/')
    }
}
// var data={
//     "role":document.getElementsById("downlist1").value,
//     "id":document.getElementsById("un1").value,
//     "password":document.getElementsById("pw1").value,
// }
// $("#userAdd").click(function () {
//     var v=valid()
//     $.ajax({
//         url: "http://localhost:5000/useradd",
//         type: "get",
//         dataType: "json",
//         success: function (result) {
//             var role = $("#downlist1").val();
//             var id = $("#un1").val();
//             var password = $("#pw1").val();
//             if (v == 1) {
//                 alert('注册成功');
//                 window.open('http://localhost:5000/')
//             } else {
//                 alert("失败")
//             }
//         },
//         error: function () {
//             console.log("false")
//         }
//     })
// })
var fileinput = document.getElementById('img_upload');
fileinput.onchange = function sendM (){
    var username = document.getElementById('id1')
    var password = document.getElementById('pw1')
    var role = document.getElementById('downlist1')
    var File = fileinput.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(File)
    reader.onload = function () {
        console.log(reader.result)
        var ajaxObj = new XMLHttpRequest();
        ajaxObj.open('get','http://127.0.0.1:5000/useradd?downlist1='+role+'&username='+username+'&password='+password+'&baseimg='+reader.result)
        ajaxObj.send(null)
    }
}
    // $.post({
    //     "/useradd",
    //     JSON.stringify({
    //         'id':$("#un1").val(),
    //         'password':$("#pw1").val(),
    //         'role':role,
    //     }),
    // })
// })

// //点击登录按钮 触发事件
// $("#userAdd").click(function(){
//     var username =$("#un1").val();
//     var pwd =$("#pw1").val();
//     if(username=="" || pwd =="")
//     {
//         layer.open({
//             title:"提示",
//             content:"用户名或密码不能为空！"
//         });
//     }
//     else
//     {
//         var usermsg = new Array();
//         usermsg.push({id:username,password:pwd});
//         var datasend=JSON.stringify(usermsg);
//         console.log(datasend);
//         $.ajax({
//             type:'get',
//             url:'http://localhost:5000/useradd',
//             dataType:'json',
//             // contentType: 'application/json; charset=utf-8',
//             data:datasend,
//             success:function(serverdata){
//                layer.msg(serverdata.msg);
//                 if(serverdata.status=="400"){
// 					 layer.msg(serverdata.msg);
//                 }
//             }
//        });
//     }
// });


// $("#userAdd").click(function (){
//     $("#userAdd").attr("disabled",true);
//     role=0;
//     if($("#roleAdmin").prop("checked")){
//         role=1;
//     }
//     if($("#roleDoctor").prop("checked")){
//         role=2;
//     }
//     if($("#roleNurse").prop("checked")){
//         role=3;
//     }
//     if(0===role){
//         //错误提示
//     }
//
//     $.post(
//         "/useradd",
//         JSON.stringify({
//             'id':$("#un1").val(),
//             'password':$("#pw1").val(),
//             'role':role,
//         }),
//
//         function (rsp){
//             data=JSON.parse(rsp)
//             $("#userAdd").attr("disabled",false);
//
//             txt="注册成功"
//             if(data.ret){
//                 txt="注册失败"
//             }
//             $("#modal-body").text(txt);
//             $('#myModal').modal('show')
//         }
//     )
// })
// $(function (){
//     //用户名输入框监听
//     $("#un1").blur(function(){
//         //得到用户输入的字符串对象
//         var vaIn=$(this).val()
//         //用户名正则对象
//         var reg=/^[\u4e00-\u9fa5]{2,4}$/;
//         if(vaIn==""||vaIn==null){
//             $("#un + span").html("*用户名不能为空").css("color","red");
//         }else if(reg.test(vaIn)){
//             $("#un + span").html("*用户名ok").css("color","green");
//         }else{
//             $("#un + span").html("*用户名不符合规则").css("color","red");
//         }
//     });
//
//     $("#pw1").blur(function (){
//         var passwd=$(this).val()
//         if(passwd==""||vaIn==null){
//             $("#un + span").html("*用户名不能为空").css("color","red");
//         }else if(reg.test(passwd)){
//             $("#un + span").html("*用户名ok").css("color","green");
//         }else{
//             $("#un + span").html("*用户名不符合规则").css("color","red");
//         }
//     });
//
//     $("#aa").click(function (){
//         //创建验证码
//         code=Math.floor(Math.random()*1000+1000)
//         //将验证码赋值给span标签的内容
//         $("#code+a").html(code)
//     });
//
//     $("#fm").submit(function (){
//         var flag=true;
//         $("span").each(function (){
//             if($(this).css("color")=="rgb(255,0,0"||$(this).css("color")=="rgb(0,0,0"){
//                 flag=false;
//             }
//         })
//     });
//     return flag?true:false;
//
// })