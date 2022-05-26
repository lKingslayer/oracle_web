           // 使用FileReader读取file实例并显示图片
           function getImgsByFileReader(el, file) {
                el.empty();
                let img = document.createElement('img');
                img.setAttribute('style', 'obj-fit: contain; vertical-align:middle');
                var reader = new FileReader();
                el.append(img);
                reader.onload = function(e) {
                   img.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }

          // 图片传给后端
          function ImageUpload(){
              $("#sel").val("recognition");
              $("#id_input").val("id");
              $("#btn_submit").click();
          }
