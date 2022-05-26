
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext("2d");

    var isDraw = false; //定义变量控制画笔是否可用
    var movePos;         //定义变量存放初始画笔开始位置
    var linWidth = 10;
    var linColor = '#333';

    window.onload = function(){
        draw();
    }

    function draw(){
        canvas.width = 275;
        canvas.height = 500;
        context.strokeStyle = "red";
        context.lineWidth = 10;
        // context.beginPath();
        // context.strokeRect(0,0,500,500);
        //设置画笔颜色，宽度
        context.strokeStyle = "red";
        context.lineWidth = 1;
        //使线段连续，圆滑
        context.lineCap = "round";
        context.lineJoin = "round";
        // drawDashedLine(context,0,0,canvas.width,canvas.width);
        // drawDashedLine(context,0,canvas.width,canvas.width,0);
        // drawLine(context,0,canvas.width/2,canvas.width,canvas.width/2);
        // drawLine(context,canvas.width/2,0,canvas.width/2,canvas.width);
        context.fillStyle = '#FFF';
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.stroke();
        context.restore();
    }

    function drawDashedLine(context, x1, y1, x2, y2, dashLength) {
      dashLength = dashLength === undefined ? 5 : dashLength;
      var deltaX = x2 - x1;
      var deltaY = y2 - y1;
      var numDashes = Math.floor(
       Math.sqrt(deltaX * deltaX + deltaY * deltaY) / dashLength);
       for (var i=0; i < numDashes; ++i) {
       context[ i % 2 === 0 ? 'moveTo' : 'lineTo' ]    (x1 + (deltaX / numDashes) * i, y1 + (deltaY / numDashes) * i);
       }
      context.stroke();
    };
    
    //画直线
    function drawLine(context,x1,y1,x2,y2){
        context.moveTo(x1,y1);
        context.lineTo(x2,y2);
        context.stroke();
    };
    
    //获取鼠标相对与canvas位置
    function getPos(x,y){
        var box = canvas.getBoundingClientRect();
        return {x: x-box.left,y: y-box.top};
    };
    
    //画笔
    function drawing(e){
        if(isDraw){
            var position = getPos(e.clientX,e.clientY);
            context.strokeStyle = linColor;
            context.lineWidth = linWidth;
            context.save();
            context.beginPath();
            context.moveTo(movePos.x,movePos.y);
            context.lineTo(position.x,position.y);
            context.stroke();
            movePos = position;
            context.restore();
        }
    }
    
    //鼠标点下
    canvas.onmousedown = function(e){
        isDraw = true;
        movePos = getPos(e.clientX,e.clientY);
        drawing(e);
    }
    
    //鼠标移动
    canvas.onmousemove = function(e){
        drawing(e);
    }
    
    //鼠标松开
    canvas.onmouseup = function(e){
        isDraw = false;
    }
    
    //鼠标离开
    canvas.onmouseout =function(e){
        isDraw = false;
    }
    
    //选择画笔颜色
    $('.color-item').on('click',function(){
        $(this).addClass('active').siblings().removeClass('active');
        linColor = $(this).css('background-color');
    });
    
    //清除
    function clearDraw(){
        context.clearRect(0,0,canvas.width,canvas.width);
        draw();
    }

   
    //保存画板
    function canvasSaveToServer() {
        var imgUrl = canvas.toDataURL("image/jpg");
        console.log(canvas.height)
        console.log(canvas.width)
        var imageDataB64 = imgUrl.substring(22);
 
        imgData = {uploadImg:imageDataB64};
        var senddata = JSON.stringify(imgData);
 
        //通过XMLHttpRequest 传送到后台
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                window.location.replace('/recognition/'+xhr.responseText);
            }
        }
        
        xhr.open("POST", "/uploadcanvas", true);
        xhr.setRequestHeader('content-type', 'application/json');
        res = xhr.send(JSON.stringify(senddata));        
    }