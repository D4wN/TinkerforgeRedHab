//function update_values() {
//    console.log("update_Values");
//    $.getJSON($SCRIPT_ROOT+"/getAmbientLight",
//        function(data) {
//            $("#AmbientLightLux").text(data.lux+" lux")
//        }
//    );
//}

$(document).ready(function() {
    $("#btn").click(function() {
        console.log("CLICKED!");
    });

    //setInterval("update_values()",2000);
});

