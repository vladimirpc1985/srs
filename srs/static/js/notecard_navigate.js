$(document).keydown(
    function(e)
    {
    	if (e.keyCode == 40 ) { //Up
			$(".imageDiv:focus").next().focus();
            if(index > notecard_top ){
                notecard_top += 1;
                start = notecard_top - 5
                new_list = trim_list(notecards, start);
                load_notecards(new_list);
                index++; 
            }
             
        }
        if (e.keyCode == 38) { //Down
            $(".imageDiv:focus").prev().focus();
                index--;
                if(index < notecard_bottom){
                notecard_bottom -= 1;
                new_list = trim_list(notecards, notecard_bottom);
                load_notecards(new_list);
            }
        }
    }
);


$(document).ready(function() {
    document.getElementById('bottomDiv1').focus();
    load_notecards(notecards);
}   
);

function load_notecards(notecards){
     for(var i = 0; i < 5; i++) {
        var id =  'bottomDiv'+ (i+1);
        document.getElementById(id).innerHTML = notecards[i].fields.name + "<br>" + notecards[i].fields.body;
        document.getElementById(id).href = 'http://'+window.location.host+'/notecard/'+notecards[i].pk+'/';
}
}

function trim_list(notecards, index){

    new_list = [];
    var end = index + 5;
    for(index; index < end; index++){
        new_list.push(notecards[index]);
    }
    return new_list;
}