// 释放摄像头资源
function closeMedia() {
    const video = document.getElementById('video');
    if (!video.srcObject) return
        let stream = video.srcObject
        let tracks = stream.getTracks();
        tracks.forEach(track => {
            track.stop()
        })
}

//获得video摄像头区域
let video = document.getElementById("video");
// 申请调用摄像头
function getMedia() {
    let constraints = {
        video: {width: 500, height: 500},  // 申请视频的分辨率
        audio: false,  // 不申请音频
    };
    /*
        权限申请接口,返回的是一个Promise对象
        如果用户同意使用权限,则会将 MediaStream对象作为resolve()的参数传给then()
        如果用户拒绝使用权限,或者请求的媒体资源不可用,则会将PermissionDeniedError作为reject()的参数传给catch()
    */
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function (MediaStream) {
        video.srcObject = MediaStream;
        video.play();
    }).catch(function (PermissionDeniedError) {
        console.log(PermissionDeniedError);
    })
}

// 执行拍照
function takePhoto() {
    //获得Canvas对象
    let canvas = document.getElementById("canvas");
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, 500, 500);
}

//图片上传到服务器
//获取Canvas的编码
<!--var video = document.getElementById('video');-->
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

function uploadImage(){
    canvas.width = 500;
    canvas.height = 500;
    context.drawImage(video, 0, 0, 500, 500);
    let imgData = canvas.toDataURL("image/jpg");
    imgData = imgData.replace(/^data:image\/(png|jpg);base64,/,"")
    //上传到后台。
    const uploadAjax = $.ajax({
        type: "post",
        url: "/receiveImage/",  // 上传地址
        data: JSON.stringify({"imgData": imgData}),  // 图片转为base64编码
        contentType: "json/application",
        timeout: 10000,  // 超时时间
        async: true,
        success: function (htmlVal) {
            //成功后回调
        },
        error: function (data) {
        },
        //调用执行后调用的函数
        complete: function (XMLHttpRequest, textStatus) {
            if (textStatus == 'timeout') {
                uploadAjax.abort(); //取消请求
                //超时提示：请求超时，请重试
                alert("请求超时，请重试")
                //请求超时返回首页
                // closeCard();
            }
        }
    });
}

function start() {
    setInterval(
        'uploadImage()',
        1000,
    )
}