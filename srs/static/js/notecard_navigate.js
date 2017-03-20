$(document).keydown(
    function(e)
    {
    	if (e.keyCode == 38) { //Up
			$(".imageDiv:focus").next().focus();
            //alert("World");
        }
        if (e.keyCode == 40) { //Down
            $(".imageDiv:focus").prev().focus();
            //alert("Hello");
        }
    }
);


$(document).ready(function() {
    document.getElementById('bottomDiv1').focus(); 
}	
);