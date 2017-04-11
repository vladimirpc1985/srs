$(document).keydown(
    function(e)
    {
    	if (e.keyCode == 38) { //Up
			$(".imageDiv:focus").next().focus();
            //alert(notecards);
        }
        if (e.keyCode == 40) { //Down
            $(".imageDiv:focus").prev().focus();
            //alert(notecards);
        }
    }
);


$(document).ready(function() {
    document.getElementById('bottomDiv1').focus();
    //LOAD CONTENT INTO DIV
    //alert(notecards);
    //alert(Object.keys(notecards).length);
    for(var i = 0; i < 1; i++) {
        var id =  'bottomDiv'+ i;
       // alert(notecards[1]);
        document.getElementById("bottomDiv1").innerHTML = notecards[1].name + "<br>" + notecards[1].label;
        //alert(notecards[i].model);

    //var obj = json[i];

    //console.log(obj.id);
}
}	
);
