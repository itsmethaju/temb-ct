(function (jQuery) {
  "use strict";
  jQuery(document).ready(function () {


    function loadmore_n_infinityscroll() {
      var loadMoreWrapper = jQuery('.post-loadmore-wrapper'),
      infinityScrollWrapper = jQuery('.post-infscroll-wrapper');


      
      if (loadMoreWrapper.length) {
        loadMore(loadMoreWrapper);
      }
      if (infinityScrollWrapper.length) {
        infinityScroll(infinityScrollWrapper);
      }
      function loadMore(jQuerywrapper) {
        var button = jQuery('.gen-button-loadmore'),icon = jQuery('.loadmore-icon'),
        CurrentPage = 1;
        var sThisVal = '';
        var postData , maxPage , query , post_type , taxo_type , box_style;
        postData = jQuery('.post-loadmore-data');
        maxPage = postData.data('max');
        query = postData.attr('data-query');
        post_type = jQuery('.post-loadmore-data').data('post_type');
        box_style = jQuery('.post-loadmore-data').data('box_style');

      
        icon.hide();

     

        button.on('click', button, function() {

          var data = {
            'action': 'loadmore_post',
            'context': 'frontend',
            'nonce': postData.data('nonce'),
            'query': query,
            'post_type': post_type,
            'box_style': box_style,

            'view': jQuery('body').hasClass('product-list-view') ? 'list' : 'grid',
            'paged': CurrentPage
          };
          jQuery.ajax({
            url: woo_obj.ajaxurl,
            type: 'POST',
            data: data,
            beforeSend: function beforeSend() {
              disableBtn(button);
            },
            success: function success(data) {
            //console.log(data);
            if (data) {
              CurrentPage++;
              jQuerywrapper.append(data);
              jQuery('.movie-actions--link_add-to-playlist .dropdown-toggle').html('<i class="fa fa-plus"></i>')
            
              if (CurrentPage == maxPage) {
                removeBtn(button);
              } else {
                enableBtn(button);
              }
              jQuery(document).trigger("afterLoadMore");
            } else {
              removeBtn(button);
            }
            jQuery('.gen-movie-contain .movie-actions--link_add-to-playlist .dropdown-toggle').html('<i class="fa fa-plus"></i>')
            jQuery('.gen-movie-contain .tv-show-actions--link_add-to-playlist .dropdown-toggle').html('<i class="fa fa-plus"></i>')
            jQuery('.gen-movie-contain .video-actions--link_add-to-playlist .dropdown-toggle').html('<i class="fa fa-plus"></i>')

          }
        });
          return false;
        });
      }
      function infinityScroll(jQuerywrapper) {
        var canBeLoaded = true,
        icon = jQuery('.loadmore-icon'),
        CurrentPage = 1;
        var button = jQuery('.gen-button-loadmore');
        var postData , maxPage , query , post_type , taxo_type , box_style;
        postData = jQuery('.post-loadmore-data');
        maxPage = postData.data('max');
        query = postData.attr('data-query');
        post_type = jQuery('.post-loadmore-data').data('post_type');
        box_style = jQuery('.post-loadmore-data').data('box_style');
        
        jQuery(window).on('scroll load', function() {
          if (!canBeLoaded) {
            return;
          }

         



          if (isScrollable(jQuerywrapper)) {
           var data = {
            'action': 'loadmore_post',
            'context': 'frontend',
            'nonce': postData.data('nonce'),
            'query': query,
            'post_type':post_type,
            'box_style':box_style,
            'taxo_type': taxo_type,
            'query': query,
            'paged': CurrentPage
          };
          jQuery.ajax({
            url: woo_obj.ajaxurl,
            type: 'POST',
            data: data,
            beforeSend: function beforeSend() {
              canBeLoaded = false;
              icon.show();
            },
            success: function success(data) {
             
             if (data) {

              CurrentPage++;
              canBeLoaded = true;
              jQuerywrapper.append(data);
              WcUpdateResultCount(jQuerywrapper);
              icon.hide();
              jQuery(document).trigger("afterInfinityScroll");
              if (CurrentPage == maxPage) {
                removeBtn(button);
              } else {
                enableBtn(button);
              }
            } else {
              icon.hide();
            }
            jQuery('.gen-movie-contain .movie-actions--link_add-to-playlist .dropdown-toggle').html('<i class="fa fa-plus"></i>')
          jQuery('.gen-movie-contain .tv-show-actions--link_add-to-playlist .dropdown-toggle').html('<i class="fa fa-plus"></i>')
          jQuery('.gen-movie-contain .video-actions--link_add-to-playlist .dropdown-toggle').html('<i class="fa fa-plus"></i>')
          }
        });
        }
      });
      }
      function isScrollable(jQuerywrapper) {
        var ajaxVisible = jQuerywrapper.offset().top + jQuerywrapper.outerHeight(true),
        ajaxScrollTop = jQuery(window).scrollTop() + jQuery(window).height();
        if (ajaxVisible <= ajaxScrollTop && ajaxVisible + jQuery(window).height() > ajaxScrollTop) {
          return true;
        }
        return false;
      }
      function WcUpdateResultCount(jQuerywrapper) {
        
      }
      function disableBtn(button) {
       
        button.attr('disabled', 'disabled');
        button.find('.button-text').hide();
        button.find('.loadmore-icon').show();
      }
      function enableBtn(button) {
       
        button.find('.loadmore-icon').hide();
        button.find('.button-text').show();
        button.removeAttr('disabled');
      }
      function removeBtn(button) {
        jQuery('.gen-load-more-button').hide();
      }
    }

    loadmore_n_infinityscroll();


  });
})(jQuery);