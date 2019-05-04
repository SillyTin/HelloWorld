layui.use('upload', function(){
    var $ = layui.jquery,upload = layui.upload;
    var demoListView = $('#proImageList');
    uploadListIns = upload.render({
     elem: '#file-input', //选择文件的按钮
     url: 'upload!ftp.action', //后台处理文件长传的方法
     data:{'serviceName':'外协订单供应商上传检验报告','tableName':'T_OUTSOURCE_ORDER','fileType':'图片'},
     accept: 'file', 
     multiple: false,  //是否允许多文件上传
     acceptMime: '*', //规定打开文件选择框时，筛选出的文件类型
     field:'upload',  
     auto: false, 
     bindAction: '#upload', //用来触发上传的按钮ID
     choose: function(obj){ //选择文件后的回调函数，本例中在此将选择的文件进行展示
      var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
      //读取本地文件
      obj.preview(function(index, file, result){
       var tr = $(['<tr id="upload-'+ index +'">'
        ,'<td>'+ file.name +'</td>'
        ,'<td>'+ (file.size/1014).toFixed(1) +'kb</td>'
        ,'<td>等待上传</td>'
        ,'<td>'
        ,'<button class="layui-btn layui-btn-xs demo-reload layui-hide">重传</button>'
        ,'<button class="layui-btn layui-btn-xs layui-btn-danger demo-delete">删除</button>'
        ,'</td>'
        ,'</tr>'].join(''));
     
       //单个重传
       tr.find('.demo-reload').on('click', function(){
        obj.upload(index, file);
       });
     
       //删除
       tr.find('.demo-delete').on('click', function(){
        delete files[index]; //删除对应的文件
        tr.remove();
        uploadListIns.config.elem.next()[0].value = ''; //清空 input file 值，以免删除后出现同名文件不可选
       });
       demoListView.append(tr);
      });
     },  
     done: function(res, index, upload){    //多文件上传时，只要有一个文件上传成功后就会触发这个回调函数
      console.info(res);
      if(res.status == "success"){ //上传成功
       var tr = demoListView.find('tr#upload-'+ index)
        ,tds = tr.children();
       tds.eq(2).html('<span style="color: #5FB878;">上传成功</span>');
       tds.eq(3).html('<a href="'+res.url+'" rel="external nofollow" >查看</a>'); //清空操作
       return delete this.files[index]; //删除文件队列已经上传成功的文件
      }else{
       alert(res.message);
      }
      this.error(index, upload);
     },
     allDone: function(obj){ //当文件全部被提交后，才触发
      if(obj.total > obj.successful){
       layer.msg("有文件上传失败，暂不更新生产进度，请重试或联系管理员");
      }else {
       //更新生产进度
       updateProductionSchedule(currentId, currentSchedule);
      }
     },
     error: function(index, upload){
      var tr = demoListView.find('tr#upload-'+ index)
       ,tds = tr.children();
      tds.eq(2).html('<span style="color: #FF5722;">上传失败</span>');
      tds.eq(3).find('.demo-reload').removeClass('layui-hide'); //显示重传
     }
    });
    $(".layui-upload-file").hide();
   });