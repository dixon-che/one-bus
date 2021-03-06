﻿/*
 * jquery-in-place-edit plugin
 *
 * Copyright (c) 2008 Christian Hellsten
 *
 * Plugin homepage:
 *  http://aktagon.com/projects/jquery-in-place-edit
 *
 * Examples:
 *  http://aktagon.com/projects/jquery-in-place-edit/examples
 *
 * Version 1.0
 *
 * Tested with:
 *  Windows:  Firefox 2, Firefox 3, Internet Explorer 6
 *  Linux:    Firefox 2, Firefox 3, Opera
 *  Mac:      Firefox 2, Firefox 3, Opera
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/mit-license.php
 *
 * TODO:
 *   - Use jQuery() instead of $()
 */
(function($) {

	$.fn.inPlaceEdit = function(options) {

    // Add click handler to all matching elements
    return this.each(function() {
      // Use default options, if necessary
      var settings = $.extend({}, $.fn.inPlaceEdit.defaults, options);

      var element = $(this);
      
      element.click(function() {
        // Prevent multiple clicks, and check if inplace editing is disabled
        if (element.hasClass("editing") || element.hasClass("disabled")) {
            return;
        }
        
        var id = '#' + element.attr('id').replace('value', 'options');
        $(id).hide();

        element.addClass("editing");

        element.old_html = element.html();          // Store old HTML so we can revert to it later
        
        if(typeof(settings.html) == 'string') {     // There are two types of form templates: strings and DOM elements
          element.html(settings.html);              // Replace current HTML with given HTML
        }
        else {
          element.html('');                         // Replace current HTML with given object's HTML
          var form_template = settings.html.children(':first').clone(true);
          form_template.appendTo(element);          // Clone event handlers too
        }

        $('.field', element).focus();               // Set focus to input field
        $('.field', element).select();              // Select all text in field
        $('.field', element).val(element.old_html); // Set field value to old HTML
        
        // On blur: cancel action
        if(settings.onBlurDisabled == false) {
          $('.field', element).blur(function() {
            // Prevent cancel from being triggered when clicking Save button
            element.timeout = setTimeout(cancel, 500);
          });
        }
        
        // On save: revert to old HTML and submit
        $('.save-button', element).click(function() {
          return submit();
        });

        // On cancel: revert to old HTML
        $('.cancel-button', element).click(function() {
          return cancel();
        });
        
        // On keyup: submit (ESC) or cancel (enter)
        if(settings.onKeyupDisabled == false) {
          $('.field', element).keyup(function(event) {
            var keycode = event.which;
            var type = this.tagName.toLowerCase();
            
            if(keycode == 27 && settings.escapeKeyDisabled == false)	{	     // escape
              return cancel();
            } 
            else if(keycode == 13) { // enter
              // Don't submit on enter if this is a textarea
              if(type != "textarea") {
                return submit();
              }
            }
            return true;
          });
        }
      });
      
      // Add hover class on mouseover
      element.mouseover(function() {
        element.addClass("hover");
      });
      
      // Remove hover class on mouseout
      element.mouseout(function() {
        element.removeClass("hover");
      });
      
      function cancel() {
        element.html(element.old_html);

        element.removeClass("hover editing");

        if(options.cancel) {
          options.cancel.apply(element, [element]);
        }
        var id = '#' + element.attr('id').replace('value', 'options');
        $(id).show();
        return false; // Stop propagation
      };
      
      function submit() {
        clearTimeout(element.timeout);

        var id = element.attr('id');
        var value = $('.field', element).val();

        if(options.submit) {
          options.submit.apply(element, [element, id, value]);
        }
        
        element.removeClass("hover editing");

        element.html(value);
        id = '#' + element.attr('id').replace('value', 'options');
        $(id).show();
        return false; // Stop propagation
      };
    });
    
  };
  
  // Default (overridable) settings
  $.fn.inPlaceEdit.defaults = {
    onBlurDisabled  : false,
    onKeyupDisabled : false,
    escapeKeyDisabled : false,
    html : ' \
          <div class="inplace-edit"> \
            <input type="text" value="" class="field" /> \
            <span class="buttons">&nbsp; \
              <img src="images/ok.png" title="Сохранить" class="save-button" />&nbsp; \
              <img src="images/cancel.png" title="Отмена" class="cancel-button" /> \
            </span> \
          </div>'
  };
})(jQuery);