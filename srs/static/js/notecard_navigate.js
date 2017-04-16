$(document).keydown(
    function(e)
    {
    	if (e.keyCode == 38 ) { //Up
            if( INDEX > TOP && TOP < MAX_TOP){
                TOP += 1;
                BOTTOM = TOP - 4;
                start = TOP - 5;
                new_list = trim_list(notecards, start);
                load_notecards(new_list);
            }else if( INDEX < MAX_TOP){             
            $(".imageDiv:focus").prev().focus();
            INDEX++; 
            }
             
        }
        if (e.keyCode == 40) { //Down
            if( INDEX < BOTTOM && BOTTOM > 1){
                BOTTOM -= 1;
                TOP = BOTTOM + 4 ;
                start = TOP - 5;
                new_list = trim_list(notecards, start);
                load_notecards(new_list);
            }else if( INDEX > 1){ 
                $(".imageDiv:focus").next().focus();
                INDEX--; 
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