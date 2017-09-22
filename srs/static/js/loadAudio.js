var wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: '#1a98ff',
    progressColor: '#0070cc'
});

$('.audio_select').click(function(e){
	// Assign video source after selecting video
	wavesurfer.load($(this).attr('data-path'));
	$("#audiosource").text('Source: ' + $(this).attr('data-source'));
	$("#audiotitle").text($(this).attr('title'));

	// Open modal​
	$(".backdrop").show();
	$("#audiomodal").fadeIn();
});

$('#audio_close').click(function(e){
	// Stop audio
	wavesurfer.pause();
	$("#play_btn").html("Play <i class='fa fa-play'></i>");
	$("#play_btn").removeClass("pause_btn");

	// Close modal
	$(".backdrop").hide();
	$("#audiomodal").fadeOut();
});

$("#play_btn").click(function(e){
	// If pause is visible
	if($(this).hasClass('pause_btn')){
	    wavesurfer.pause();
	    $("#play_btn").toggleClass("pause_btn");
	    $("#play_btn").html("Play <i class='fa fa-play'></i>");
	}
	// If play is visible
	else{
		wavesurfer.play();
		$("#play_btn").toggleClass("pause_btn");
		$("#play_btn").html("Pause <i class='fa fa-pause'></i>");
	}
});