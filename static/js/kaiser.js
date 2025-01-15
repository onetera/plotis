const showMenuCheckbox = document.getElementById('show-menu');

if (showMenuCheckbox) {
    showMenuCheckbox.addEventListener('change', function() {
        const menu = document.querySelector('.header-box');
        if (menu) {
            if (this.checked) {
                // 메뉴가 열릴 때
                menu.style.animation = 'slideDown 0.3s ease-out';
            } else {
                // 메뉴가 닫힐 때
                menu.style.animation = 'none';
            }
        }
    });
}


// navigation
if (config.nav) {
	for (i = 0; i < slides.length; i+=1) {
  	$('<li/>').attr( {'class': 'nav-item','id': i}).appendTo('.slide-nav');
	};
  $('.nav-item').first().addClass('item-active');
  switch(config.navStyle) { // navigation style
    case 'square':
        $('.nav-item').addClass('square');
        break;
    case 'rectangle':
        $('.nav-item').addClass('rectangle');
        break;
    default:
        $('.nav-item').addClass('dot');
  };
  function navigation() {
    $('.nav-item').removeClass('item-active');
    $('.nav-item').eq(currentIndex).addClass('item-active');
  };
	$('.nav-item').click(function() {
  	clearInterval(autoSlide);
  	var navNumb =  $(this).attr('id');
  	currentIndex = navNumb;
  	navigation();
  	setSlides();
  });
};
