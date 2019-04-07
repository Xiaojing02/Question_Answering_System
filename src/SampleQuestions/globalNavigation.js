/**
 * globalNavigation.js, resize the navigation div and content div
 **/

var globalNavigation = {};

globalNavigation.init = function()
{
  var quickLinks = $('quick_links_wrap');
  
  if ( self != window.parent )
  {
    // If we have a parent then we're not in the top of the page - while we shouldn't get here in the first
    // place due to proper application logic not showing the globalnav to begin with, if we DO then this is
    // a fallback to remove it from the page.  Currently this logic should only be kicking in when you
    // add 'portfolio homepage' to your course content area and then click through to it and then navigate into
    // various pieces of the portfolio tool - nested pages may not retain the globalNavigation=false
    // parameter and this code handles that case.
    var navArea = $( 'globalNavPageNavArea' );
    if ( navArea )
    {
      var navBarWrap = navArea.up().down( '.global-nav-bar-wrap' );
      if ( navBarWrap )
      {
        navBarWrap.hide();
      }
      navArea.hide();
      if ( quickLinks )
      {
        quickLinks.hide();
      }
      return;
    }
  }
  
  // to set contentDiv height
  globalNavigation.onResize();  

  var navDivHeight = globalNavigation.getNavDivHeight();
  if ( quickLinks  && navDivHeight !== 0 )
  {
    quickLinks.setStyle({ top: (navDivHeight - quickLinks.getHeight()) + 'px'});
  }
};

globalNavigation.getNavDivHeight = function()
{
  return $('globalNavPageNavArea') ? $('globalNavPageNavArea').getHeight() : 0;
};

globalNavigation.setNavDivHeight = function(height)
{
  if (window.self === window.top) {
    $('globalNavPageNavArea').setStyle({height: height + 'px'});
    globalNavigation.onResize();
  }
};

globalNavigation.onResize = function(ev)
{
  var windowHeight = document.viewport.getHeight();
  var navDivHeight = $('globalNavPageNavArea').getHeight();
  var contentDiv = $('globalNavPageContentArea');
  contentDiv.hide();

  if (window.matchMedia("(max-width: 1024px)").matches) {
    if (window.self === window.top) { 
      contentDiv.setStyle({height: (windowHeight - navDivHeight) + 'px'});
    }
  } else {
    contentDiv.setStyle({height: (windowHeight - navDivHeight) + 'px', overflow: 'visible'});
  }

  contentDiv.show();
};

globalNavigation.getContentAreaScrollOffset = function()
{
  var contentDiv = $( 'globalNavPageContentArea' );
  if ( contentDiv )
  {
    var res =
    {
        scrollLeft : contentDiv.scrollLeft,
        scrollTop : contentDiv.scrollTop
    };
    return res;
  }
  else
  {
    var res =
    {
        scrollLeft : 0,
        scrollTop : 0
    };
    return res;
  }
};

globalNavigation.openHelpWindow = function(helpUrl)
{
  var features='width=900, height=675, toolbar=yes, location=yes, menubar=yes, scrollbars=yes, status=yes, resizable=yes';
  newWindow=window.open(helpUrl,'_blank',features);
  if(newWindow != null){
    newWindow.focus();
  }
  return false;
};

globalNavigation.getNoGlobalNavUrl = function(url)
{
  return url + (url.split('?')[1] ? '&':'?') + 'globalNavigation=false';
};

globalNavigation.redirectTopWindow = function()
{
  if(window != top && !page.util.insideUltra() )
  {
    top.location.href = window.location.href.replace('globalNavigation=false', 'globalNavigation=true');
  }
};

globalNavigation.openFullPageFromIframe = function(baseWindow, url)
{
  var par = baseWindow || window;
  var tmp = par.parent;
  while (tmp && tmp != par)
  {
    par = tmp;
    tmp = par.parent;
  }

  if ( baseWindow && baseWindow.page.util.insideUltra() )
  {
    //Ultra is enabled in the opener window.
    var classicCourseIframe = par.document.getElementsByClassName("classic-learn-iframe")[0];
    if ( classicCourseIframe )
    {
      if ( url.startsWith('/') )
      {
        url = document.location.origin + url;
      }
      classicCourseIframe.src = url;
    }
    //TODO: the case of the classic learn iframe not exiting need be handled, i.e. if you navigate away from the course in Ultra but leave the separate window open and then click,
    //the course need be opened then. 
  }
  else
  {
    par.document.location = url;
  }
};