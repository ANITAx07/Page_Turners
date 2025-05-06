(function($) {
    
	var $window = $(window),
		$body = $('body');

	// Breakpoints
	breakpoints({
		xlarge:   [ '1281px',  '1680px' ],
		large:    [ '981px',   '1280px' ],
		medium:   [ '737px',   '980px'  ],
		small:    [ '481px',   '736px'  ],
		xsmall:   [ '361px',   '480px'  ],
		xxsmall:  [ null,      '360px'  ]
	});

	// Initial animations
	$window.on('load', function() {
		window.setTimeout(function() {
			$body.removeClass('is-preload');
		}, 100);
	});

	// Mobile detection
	if (browser.mobile)
		$body.addClass('is-touch');

	// Theme switcher placeholder
	var themeSwitcher = $('<div ></div>');
	themeSwitcher.appendTo($body);

	// Auto-resizing textareas
	var $form = $('form');
	$form.find('textarea').each(function() {
		var $this = $(this),
			$wrapper = $('<div class="textarea-wrapper"></div>');

		$this
			.wrap($wrapper)
			.attr('rows', 1)
			.css('overflow', 'hidden')
			.css('resize', 'none')
			.on('keydown', function(event) {
				if (event.keyCode == 13 && event.ctrlKey) {
					event.preventDefault();
					event.stopPropagation();
					$(this).blur();
				}
			})
			.on('blur focus', function() {
				$this.val($.trim($this.val()));
			})
			.on('input blur focus --init', function() {
				$wrapper.css('height', $this.height());
				$this
					.css('height', 'auto')
					.css('height', $this.prop('scrollHeight') + 'px');
			})
			.on('keyup', function(event) {
				if (event.keyCode == 9)
					$this.select();
			})
			.triggerHandler('--init');

		if (browser.name == 'ie' || browser.mobile)
			$this.css('max-height', '10em').css('overflow-y', 'auto');
	});

	// Menu logic
	var $menu = $('#menu');

	$menu.wrapInner('<div class="inner"></div>');

	$menu._locked = false;

	$menu._lock = function() {
		if ($menu._locked) return false;
		$menu._locked = true;
		window.setTimeout(function() {
			$menu._locked = false;
		}, 350);
		return true;
	};

	$menu._show = function() {
		if ($menu._lock()) $body.addClass('is-menu-visible');
	};

	$menu._hide = function() {
		if ($menu._lock()) $body.removeClass('is-menu-visible');
	};

	$menu._toggle = function() {
		if ($menu._lock()) $body.toggleClass('is-menu-visible');
	};

	$menu
		.appendTo($body)
		.on('click', function(event) {
			event.stopPropagation();
		})
		.on('click', 'a', function(event) {
			var href = $(this).attr('href');
			event.preventDefault();
			event.stopPropagation();
			$menu._hide();
			if (href != '#menu') {
				window.setTimeout(function() {
					window.location.href = href;
				}, 350);
			}
		})
		.append('<a class="close" href="#menu">Close</a>');

	$body
		.on('click', 'a[href="#menu"]', function(event) {
			event.stopPropagation();
			event.preventDefault();
			$menu._toggle();
		})
		.on('click', function() {
			$menu._hide();
		})
		.on('keydown', function(event) {
			if (event.keyCode == 27) $menu._hide();
		});

	// ✅ Genre Dropdown Toggle
	$('.dropdown-toggle').on('click', function (e) {
		e.preventDefault();
		$(this).toggleClass('open');
		$(this).next('.dropdown-menu').toggleClass('show');
	});

})(jQuery);
