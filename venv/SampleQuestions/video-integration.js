if ( !window.VideoIntegration )
{
  var VideoIntegration =
  {};

  VideoIntegration.TRUSTY_IFRAME_SOURCE_URL_ORIGIN = "";
  VideoIntegration.shouldSyncAltToTitle = true;

  VideoIntegration.onReceivingMessageHandler = function( event )
  {
    var messageType = event.data.messageType;
    var eventOrigin = event.origin;
    var eventSource = event.source;
    if ( messageType )
    {
      if ( VideoIntegration.TRUSTY_IFRAME_SOURCE_URL_ORIGIN &&
           eventOrigin === VideoIntegration.TRUSTY_IFRAME_SOURCE_URL_ORIGIN )
      {
        /*
         * For now we merely ack, which is expected by the Collab capture app, for most of the messages. In the future,
         * we may actually want to do more with the messages.
         */
        switch ( messageType )
        {
          case 'capture_loaded':
            eventSource.postMessage(
            {
              messageType : 'capture_loaded_ack'
            }, eventOrigin );
            break;
          case 'capture_maximize':
            eventSource.postMessage(
            {
              messageType : 'capture_maximize_ack'
            }, eventOrigin );
            break;
          case 'capture_complete':
            // save video uuid
            $('videoJSONId').value = event.data.uid;
            // display recording, title, alternative text
            $('videoInfoId').show();
            // update duration
            VideoIntegration.updateDuration( event.data.durationSeconds );
            // set focus on title
            $('videoTitleId').focus();
            // hide collab capture iframe
            $('collabCaptureId').hide();
            // add event listeners
            Event.observe('insertLinkId', 'click', VideoIntegration.onInsertLinkHandler);
            Event.observe('videoTitleId', 'input', VideoIntegration.onTitleChangeHandler);
            $j( "#altTextId" ).keydown(function() {
              if ( VideoIntegration.shouldSyncAltToTitle )
              {
                VideoIntegration.shouldSyncAltToTitle = false;
              }
            });
            break;
          case 'capture_close':
            eventSource.postMessage(
            {
              messageType : 'capture_close_ack'
            }, eventOrigin );
            break;
          default:
        }
      }
      else if ( eventOrigin === window.location.origin )
      {
        if ( messageType === 'iframe_origin' )
        {
          var iFrameURLOrigin = event.data.iFrameURLOrigin;
          if ( iFrameURLOrigin )
          {
            VideoIntegration.TRUSTY_IFRAME_SOURCE_URL_ORIGIN = iFrameURLOrigin;
          }
        }
      }
    }
  };
  
  VideoIntegration.updateDuration = function( durationSeconds )
  {
    var date = new Date( null );
    date.setSeconds( durationSeconds );
    var dateStr = date.toISOString();
    // the date format is 'hh:mm:ss'
    
    // hours are not supported for now
    var hourStr = dateStr.substr(11, 2);
    var hours = parseInt( hourStr, 10 );
    
    // minutes
    var minuteStr = dateStr.substr(14, 2);
    var minutes = parseInt( minuteStr, 10 );
    $('minuteId').update( minuteStr );
    if ( minutes > 1 )
    {
      $('minuteUnit').remove();
    }
    else
    {
      $('minutesUnit').remove();
    }
    
    // seconds
    var secondStr = dateStr.substr(17, 2);
    var seconds = parseInt( secondStr, 10 );
    $('secondId').update( secondStr );
    if ( seconds > 1 )
    {
      $('secondUnit').remove();
    }
    else
    {
      $('secondsUnit').remove();
    }
  };
  
  VideoIntegration.validateRecordingNameAndAltText = function()
  {
    var receipt = $('receipt_id');
    if ( receipt )
    {
      //Remove any existing inline receipt (if any).
      receipt.remove();
    }
    var videoTitle = $('videoTitleId').value.strip();
    var altText = $('altTextId').value.strip();
    if ( !videoTitle )
    {
      new page.InlineConfirmation( "error", page.bundle.getString( 'video-integration.empty.name.error' ), false );
      return false;
    }
    else if ( !altText )
    {
      new page.InlineConfirmation( "error", page.bundle.getString( 'video-integration.empty.altText.error' ), false );
      return false;
    }
    else
    {
      return true;
    }
  };
  
  VideoIntegration.onInsertLinkHandler = function()
  {
    if ( !VideoIntegration.validateRecordingNameAndAltText() )
    {
      return;
    }
    // Make REST API call to LEARN to save video integration.
    var videoJSON = JSON.stringify( { "videoUuid" : $('videoJSONId').value, 
      "videoTitle" : $('videoTitleId').value, "videoAltText": $('altTextId').value } );
    $j.ajax({
      type: "POST",
      url: "/learn/api/v1/video-integration",
      headers: { 'X-Blackboard-XSRF': $( 'ajaxNonceId' ).value },
      contentType: "application/json",
      data: videoJSON,
      success: function (data, status, jqXHR) 
      {
        if ( window.opener.tinyMceWrapper && window.opener.tinyMceWrapper.setMashupData )
        { 
          // Embed link into VTBE text.
          window.opener.tinyMceWrapper.setMashupData( data.videoEmbeddedLink + '"' + $('videoTitleId').value.strip().escapeHTML() + '"' );
        }
        // Close popup.
        self.close();
      },
      error: function (jqXHR, status) 
      {
        new page.InlineConfirmation( "error", page.bundle.getString( 'video-integration.save.recording.failure.receipt' ) , false );
      },
      dataType: 'json'
    });
  };	
  
  VideoIntegration.onTitleChangeHandler = function()
  {
    $('videoNameId').update( $('videoTitleId').value.strip().escapeHTML() );
    if ( VideoIntegration.shouldSyncAltToTitle )
    {
      $('altTextId').value = $('videoTitleId').value;
    }
  };
  
  /**
   * Shows an inline receipt informing the user to not navigate away during the recording process.
   */
  VideoIntegration.showDoNotCloseRecordingWindowMsg = function()
  {
    new page.InlineConfirmation( "success", page.bundle.getString( 'video-integration.do-not-navigate-during-recording' ) , false );
  };
  
  /**
   * Setup communication between the window popup and collab capture.
   */
  VideoIntegration.initCollabCaptureCommunication = function( targetUrl )
  {
    window.addEventListener( "message", VideoIntegration.onReceivingMessageHandler, true );
    var iFrame = $("collabVideoIFrameId");
    iFrame.src = targetUrl;
    var iFrameURL = new URL( iFrame.src );
    window.postMessage(
    {
      messageType : 'iframe_origin',
      iFrameURLOrigin : iFrameURL.origin
    }, window.location.origin );
  };
  
  /**
   * Opens a popup window containing an iFrame displaying the specified video.
   */
  VideoIntegration.viewInPopup = function( courseId, videoUuid )
  {
	var queryParams = { course_id: courseId, videoUuid: videoUuid };
	var viewViewUrl = '/webapps/videointegration/view/play?' + jQuery.param( queryParams );
    var viewWindow = window.open( viewViewUrl, 'VideoIntegrationVideoView', 'height=715,width=1200,status=1,scrollbars=1,resizable=1' );
    if ( viewWindow )
    {
      viewWindow.focus();
    }
    return false;
  };
}
