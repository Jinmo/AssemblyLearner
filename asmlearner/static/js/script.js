jQuery(window).ready(function() {
	$('.submit').on('click', function() {
		$(this).closest('form').submit();
	});
});