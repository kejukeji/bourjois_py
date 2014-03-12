// todo-lyw 这个文件应该集成到框架里面去，还有更好的实现方法，目前想不到方案，先ln导入到包里面去了
// 相关的model的create.html和update.html也改变了，需要ln导入

$(document).ready(function(){
	function add_select() {
		g_belong_area_id = $("#belong_area_id").val();
		var city_select = $.parseHTML("<select name='belong_area_id' id='belong_area_id'></select>");
		$("#belong_area_id").replaceWith(city_select);
		// 添加文件上传
		var picture_select = $.parseHTML("<input class='btn btn-success' type='file' name='picture' id='picture' multiple>");
		$("#picture").replaceWith(picture_select);
		// 添加百度地图
		$("#latitude").parent().parent().parent().after("<div id='baidumap' style='width:800px; height:500px; margin-bottom:20px;'></div>");
		// 添加地图搜索
		$("#latitude").parent().parent().parent().after("<div id='float_search_bar'><input type='text' id='keyword' /><span id='search_button' style='margin-left:-45px;' class='btn'>查找</span></div>");
	};

	add_select();

    // 如果不是新建的话，添加一个图片管理和活动管理的东西，到哪里去
//    if (g_province_id != "") {
//        var manager_link = $.parseHTML("<p><a class='btn btn-danger' href='/admin/pubpicturefile?pub_id="+gup('id')+"'>图片管理</a></p>");
//        var activity_link = $.parseHTML("<p><a class='btn btn-danger' href='/admin/activityview?pub_id="+gup('id')+"'>活动管理</a></p>");
//        $("#picture").after(manager_link);
//        $("#picture").after(activity_link);
//        $("#picture").remove();  // 去掉图片上传
//    }


    function change_textarea() {
        $("#intro").css('width', '552px').css('height', '400px');
    };
    change_textarea();

    // 定义获取当前url属性的函数
    function gup( name ) {
        name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
        var regexS = "[\\?&]"+name+"=([^&#]*)";
        var regex = new RegExp( regexS );
        var results = regex.exec( window.location.href );
        if( results == null )
            return "";
        else
            return results[1];
    }

    function init_loacation(init_province) {
        // 获取省的json
        $.ajax({
            type: "GET",
            url: "/restful/admin/area",
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                $("#belong_area_id").empty();
                $.each(json, function(i, value) {
                    $("#belong_area_id").append($("<option>").text(value[1]).attr('value', value[0]));
                });
                $("#belong_area_id").val(init_province);
                g_belong_area_id = init_province;
            },
            error: function() {
                alert("获取省份资料失败，请刷新网页！");
            }
        });

//        // 获取特定省下面的市区
//        $.ajax({
//            type: "GET",
//            url: "/restful/admin/city/" + init_province,
//            dataType: "json",
//            async: false,
//            cache: false,
//            success: function(json) {
//                $("#city_id").empty();
//                $.each(json, function(i, value) {
//                    $("#city_id").append($("<option>").text(value[1]).attr('value', value[0]));
//                });
//                $("#city_id").val(init_city);
//                g_city_id = init_city;
//                // 这里设置市改变之后，区县的option也跟着改变
//            },
//            error: function() {
//                alert("获取市资料失败，请刷新网页！");
//            }
//        });
//
//        // 获取特定市下面的区县
//        $.ajax({
//            type: "GET",
//            url: "/restful/admin/county/" + init_city,
//            dataType: "json",
//            async: false,
//            cache: false,
//            success: function(json) {
//                $("#county_id").empty();
//                $.each(json, function(i, value) {
//                    $("#county_id").append($("<option>").text(value[1]).attr('value', value[0]));
//                });
//                $("#county_id").val(init_county);
//                g_county_id = init_county;
//            },
//            error: function() {
//                alert("获取区县资料失败，请刷新页面！")
//            }
//        })
    }

    // 如果是新建的话，这几个id是不存在的，无法获取，使用默认参数
    if (g_belong_area_id != "") {
        init_loacation(g_belong_area_id);
    } else {
        init_loacation("1");
    }

	// 地图初始化
	function setResult(lng, lat) {
		$("#latitude").val(lat);
		$("#longitude").val(lng);
	};

	function init_map() {
		createMap();
		setMapEvent(); // 设置地图事件
		addMapControl(); // 向地图添加控件
	};

	function createMap() {
		var map = new BMap.Map("baidumap"); //在百度地图容器中创建一个地图
		var point = new BMap.Point(121.487899, 31.249162);
		map.centerAndZoom(point, 12);
		window.map = map; //将map变量存储在全局
	};

	function setMapEvent() {
        map.enableDragging(); //启用地图拖拽事件，默认启用(可不写)
        map.enableScrollWheelZoom(); //启用地图滚轮放大缩小
        map.enableDoubleClickZoom(); //启用鼠标双击放大，默认启用(可不写)
        map.enableKeyboard(); //启用键盘上下左右键移动地图
	};

	function addMapControl() {
        //向地图中添加缩放控件
		var ctrl_nav = new BMap.NavigationControl({anchor:BMAP_ANCHOR_TOP_LEFT,type:BMAP_NAVIGATION_CONTROL_SMALL});
		map.addControl(ctrl_nav);
        //向地图中添加缩略图控件
		var ctrl_ove = new BMap.OverviewMapControl({anchor:BMAP_ANCHOR_BOTTOM_RIGHT,isOpen:0});
		map.addControl(ctrl_ove);
        //向地图中添加比例尺控件
		var ctrl_sca = new BMap.ScaleControl({anchor:BMAP_ANCHOR_BOTTOM_LEFT});
		map.addControl(ctrl_sca);
	};

	init_map();

// 百度地图数据部分 start
	var marker_trick = true;
	var marker = new BMap.Marker(new BMap.Point(121.487899, 31.249162), {
		enableMassClear: false,
		raiseOnDrag: true
	});
	marker.enableDragging();
	map.addEventListener("click", function(e) {
		setResult(e.point.lng, e.point.lat);
	});
	marker.addEventListener("dragend", function(e) {
		setResult(e.point.lng, e.point.lat);
	});
	var local = new BMap.LocalSearch(map, {
		renderOptions: {map: map},
		pageCapacity: 1
	});
	local.setSearchCompleteCallback(function(results) {
		if (local.getStatus() != BMAP_STATUS_SUCCESS) {
			//alert("无结果");
		} else {
			marker.hide();
		}
	});
	local.setMarkersSetCallback(function(pois) {
		for (var i=pois.length; i--; ) {
			var marker = pois[i].marker;
			marker.addEventListener("click", function(e) {
				marker_trick = True;
				var pos = this.getPosition();
				setResult(pos.lng, pos.lat);
			});
		}
	});
    $("#keyword").change(function() {
    	local.search($("#keyword").val());
    });
    $("#keyword").onkeyup = function(e){
        var me = this;
        e = e || window.event;
        var keycode = e.keyCode;
        if(keycode === 13){
            local.search($("#keyword").val());
        }
    };
// 百度地图数据部分 stop

	//填写酒吧名字自动填写搜索的内容
	$("#name").change(function() {
		$("#keyword").val($("#name").val());
    	local.search($("#keyword").val());
	})

	// 表单屏蔽回车提交
    $("input").keypress(function(e) {
        var keyCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
        if (keyCode == 13) {
            return false;
        } else {
            return true;
        }
    });

	// 多选的时候返回1，2，3
	$("input[value|='Submit']").click(function() {
		var pub_type = $("#pub_type").val().toString();
		var pub_type_text = $.parseHTML("<input id='pub_type' tpye='text' name='pub_type'>")
		$("#pub_type").replaceWith(pub_type_text)
		$("#pub_type").val(pub_type)
	});
});