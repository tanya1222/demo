//选择滤波事件
$(".filter-mode").change(function () {
    selectMode($(this).val());
});


function selectMode(value) {
    // alert(value);
    $(".options").hide();

    switch (value) {
        case "GaussianBlur":
            $(".GaussianBlur-radius").show();
            break;
        case  "UnsharpMask":
            $(".UnsharpMask").show();
            break;
        case "MedianFilter":
        case "MinFilter":
        case "MaxFilter":
        case "ModeFilter":
            $(".MFilter-size").show();
            break;
        case "RankFilter":
            $(".RankFilter").show();
            break;
        default:
            break;
    }


}