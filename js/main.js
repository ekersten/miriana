(function($) {
	
	$('nav a').on('click', clickNav);
	$(window).on('resize', resizeHandler);
	$('.top').on('click', clickTop);

	resizeHandler(null);

	function clickNav(e) {
		e.preventDefault();

		$('html, body').animate({
			scrollTop: $($(this).attr('href')).offset().top
		}, 1500);

	}

	function clickTop(e) {
		$('html, body').animate({
			scrollTop: 0,
		}, 1500);		
	}

	function resizeHandler(e) {
		if($(window).width() >= 750) {
			$('.top').hide();
			$(window).on('scroll', scrollHandler);		
		} else {
			$('.top').fadeIn();
			$(window).off('scroll', scrollHandler);
		}
	}

	function scrollHandler(e) {
		var scrollPos = $(window).scrollTop();
		$('section.section').each(function(index, item) {
			if (scrollPos >= $(item).offset().top - 100 && scrollPos > 0) {
				$(item).find('.top').fadeIn();
			} else {
				$(item).find('.top').fadeOut();
			}
		});
	}

})(jQuery);