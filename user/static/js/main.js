$(function MeneStyle() {
    var state = true;
    $( ".menu" ).mouseenter(function() {
    
        $( this ).animate({
          backgroundColor: "rgba(204,0,0,.3)"
        }, 200 );
	});
	
     $( ".menu" ).mouseleave(function() {
        $( this).animate({
          backgroundColor: "rgba(204,0,0,0)" 
        }, 200);
    });
});

$(function ToolTip() {
	$('.menu').tooltip()
});

$(function Spinner() {
	$('.spinner').spinner()
});