
// Note: include this file when using prototype and jQuery on the same page. Be sure to include prototype.js
// and jquery.js before this file.
// The jQuery $ function will be remapped to $j as to not conflict with the prototype version of that function.

// Be aware that some jQuery plugins may use the $ function and in that case, they should be edited to use $j instead.

(function($) {
  $.noConflict();$j = $;
})(jQuery);

