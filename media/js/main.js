// Hello.
//
// This is The Scripts used for ___________ Theme
//
//

function main() {

(function () {
   'use strict';

   /* ==============================================
  	Testimonial Slider
  	=============================================== */

  	$('a.page-scroll').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
          if (target.length) {
            $('html,body').animate({
              scrollTop: target.offset().top - 40
            }, 900);
            return false;
          }
        }
      });

    /*====================================
    Show Menu on Book
    ======================================*/
    $(window).bind('scroll', function() {
        var navHeight = $(window).height() - 100;
        if ($(window).scrollTop() > navHeight) {
            $('.navbar-default').addClass('on');
        } else {
            $('.navbar-default').removeClass('on');
        }
    });

    $('body').scrollspy({
        target: '.navbar-default',
        offset: 80
    });

  	$(document).ready(function() {

        $('[data-toggle="popover"]').popover();


        $(".course_remove").click( function() {
            $.post( '/assets/php/doRemoveCoursefromCart.php' , {
                course_id : this.value,
                csrf_token : this.name
            });
            this.closest('tr').remove();
        });

  	  $("#team").owlCarousel({

  	      navigation : false, // Show next and prev buttons
  	      slideSpeed : 300,
  	      paginationSpeed : 400,
  	      autoHeight : true,
  	      itemsCustom : [
				        [0, 1],
				        [450, 2],
				        [600, 2],
				        [700, 2],
				        [1000, 4],
				        [1200, 4],
				        [1400, 4],
				        [1600, 4]
				      ],
  	  });

  	  $("#clients").owlCarousel({

  	      navigation : false, // Show next and prev buttons
  	      slideSpeed : 300,
  	      paginationSpeed : 400,
  	      autoHeight : true,
  	      itemsCustom : [
				        [0, 1],
				        [450, 1],
				        [600, 1],
				        [700, 1],
				        [1000, 1],
				        [1200, 1],
				        [1400, 1],
				        [1600, 1]
				      ],
  	  });

        $("#service").owlCarousel({

            navigation : false, // Show next and prev buttons
            slideSpeed : 300,
            paginationSpeed : 400,
            autoHeight : true,
            itemsCustom : [
                [0, 1],
                [450, 3],
                [600, 3],
                [700, 3],
                [1000, 3],
                [1200, 3],
                [1400, 3],
                [1600, 3]
            ],
        });

      $("#testimonial").owlCarousel({
        navigation : false, // Show next and prev buttons
        slideSpeed : 300,
        paginationSpeed : 400,
        singleItem:true
        });

        function showHide(d)
        {
            alert('clicked');
            var onediv = document.getElementById(d);
            var divs=['content1','content2','content3'];
            for (var i=0;i<divs.length;i++)
            {
                if (onediv != document.getElementById(divs[i]))
                {
                    document.getElementById(divs[i]).style.display='none';
                }
            }
            onediv.style.display = 'block';
        }


        $(function stay() {
            $('ul.menu li a').click(function () {
                $('ul.menu li a').removeClass('selected');
                $(this).addClass('selected');

            });
        });

        $(document).ready(function() {

            var owl = $("#owl-demo");
            owl.owlCarousel({
              itemsCustom : [
                  [0, 1],
                  [450, 2],
                  [600, 2],
                  [700, 2],
                  [1000, 2],
                  [1200, 2],
                  [1400, 2],
                  [1600, 2]
              ],
            });

            // Custom Navigation Events
            $(".next").click(function(){
                owl.trigger('owl.next');
            })
            $(".prev").click(function(){
                owl.trigger('owl.prev');
            })
            $(".play").click(function(){
                owl.trigger('owl.play',1000); //owl.play event accept autoPlay speed as second parameter
            })
            $(".stop").click(function(){
                owl.trigger('owl.stop');
            })
        });

        $(document).ready(function() {

            var owlportal = $("#owl-portal");

            owlportal.owlCarousel({
                items : 5, //10 items above 1000px browser width
                itemsDesktop : [1000,3], //5 items between 1000px and 901px
                itemsDesktopSmall : [900,3], // betweem 900px and 601px
                itemsTablet: [600,2], //2 items between 600 and 0
                itemsMobile : false // itemsMobile disabled - inherit from itemsTablet option
            });

            // Custom Navigation Events
            $(".next").click(function(){
                owlportal.trigger('owl.next');
            })
            $(".prev").click(function(){
                owlportal.trigger('owl.prev');
            })
            $(".play").click(function(){
                owlportal.trigger('owl.play',1000); //owl.play event accept autoPlay speed as second parameter
            })
            $(".stop").click(function(){
                owlportal.trigger('owl.stop');
            })

        });


    });

  	/*====================================
    Portfolio Isotope Filter
    ======================================*/
    $(window).load(function() {
        var $container = $('#lightbox');
        $container.isotope({
            filter: '*',
            animationOptions: {
                duration: 750,
                easing: 'linear',
                queue: false
            }
        });
        $('.cat a').click(function() {
            $('.cat .active').removeClass('active');
            $(this).addClass('active');
            var selector = $(this).attr('data-filter');
            $container.isotope({
                filter: selector,
                animationOptions: {
                    duration: 750,
                    easing: 'linear',
                    queue: false
                }
            });
            return false;
        });

    });



}());


}
main();
