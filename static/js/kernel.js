//选择滤波事件
function selectMode(value) {
    // alert(value);
    $(".kernel").hide();

    if (value === 'fxf') {
        $(".kernel-fxf").show();
    } else {
        $(".kernel-txt").show();
    }


}