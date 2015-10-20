jQuery(window).ready(function() {
	$('.submit').on('click', function() {
		$(this).closest('form').submit();
	});
    $('.popup').popup();
   
    $(".login input").keypress(function(event) {

        if(event.keyCode == 13) { 
        textboxes = $(".login input");
        currentBoxNumber = textboxes.index(this);
        if (textboxes[currentBoxNumber + 1] != null) {
            nextBox = textboxes[currentBoxNumber + 1]
            nextBox.focus();
            nextBox.select();
            event.preventDefault();
            return false 
            } else {
                $('.login').submit();
            }
        }
    });

    $('#tags').tagsInput({width: 'auto'});
});