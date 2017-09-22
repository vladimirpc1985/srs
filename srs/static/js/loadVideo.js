$('.video_select').click(function(e){
	// Assign video source after selecting video
	$("#video_box").attr("src", $(this).attr('data-path'));
	$("#vidsource").text('Source: ' + $(this).attr('data-source'));
	$("#vidtitle").text($(this).attr('title'));
	$("#video")[0].load();

	// Open modal​
	$(".backdrop").show();
	$("#vidmodal").fadeIn();
});

$('#vid_close').click(function(e){
	// Stop video
	$("#video").get(0).pause();

	// Close modal
	$(".backdrop").hide();
	$("#vidmodal").fadeOut();
});