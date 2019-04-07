var ProfileAccess = (function () {
  var PROFILE_ACCESSOR_ATTR = 'data-profile-accessor';
  var PROFILE_ID_ATTR = 'data-profile-id';
  var PROFILE_CHANGED_ID_ATTR = 'data-profile-changed-id';

  return Class.create({
    initialize:function (urlStem, sessionRedirectUri, linkUri, socialOn, ajaxNonceKey, ajaxNonce) {
      this.urlStem = urlStem;
      this.sessionRedirectUri = sessionRedirectUri;
      this.linkUri = linkUri;
      this.socialOn = socialOn;
      this.ajaxNonceKey = ajaxNonceKey;
      this.ajaxNonce = ajaxNonce;

      // Watch for clicks on profile accessor
      Event.observe(document.body, 'click', this.onAccessClick.bindAsEventListener(this));
    },
    onAccessClick:function (ev) {
      // If the click was on an accessor, handle it.
      var target = $(Event.findElement(ev, 'a'));
      if (target && target.readAttribute(PROFILE_ACCESSOR_ATTR)) {
        Event.stop(ev);
        this.handleProfileAccess();
      }
    },
    handleProfileAccess:function () {
      var self = this;
      new Ajax.Request(this.urlStem + 'optin/isOptedIn', {
        method:'get',
        onSuccess:function (response) {
          var body = response.responseJSON;
          if (body.optIn) {
            self.goToProfile();
          } else {
            // Make sure that the lightbox in the frameset gets invoked if user clicks the link in MyBb
            if (window === top) {
              self.showOptInLightbox();
            } else {
              top.profileAccess.showOptInLightbox();
            }
          }
        },
        onFailure:function (response) {
          alert(page.bundle.getString("optin.processing.error"));
          window.location.reload();
        }
      });
    },
    goToProfile:function () {
      // Find the profile accessor
      var accessLink = $$('['+PROFILE_ACCESSOR_ATTR+'=true]')[0];
      if (accessLink) {
        var profileId = accessLink.readAttribute(PROFILE_ID_ATTR);
        if (profileId) {
          // did the profileId change during login?
          var profileLink = this.linkUri;
          var changedId = accessLink.readAttribute(PROFILE_CHANGED_ID_ATTR);
          if (changedId) {
            profileLink = profileLink.replace(profileId, changedId);
          }
          if (this.socialOn) {
            social.Profile.toggleView(social.Profile.DISPLAY_TARGET_MYBB, profileLink);
          }
          else {
            social.Profile.toggleView(social.Profile.DISPLAY_TARGET_WINDOW, profileLink);
          }
        }
      }
    },
    showOptInLightbox:function () {
      var lb = new lightbox.Lightbox({
        ajax:{
          url:this.urlStem + 'optin/lightboxContents',
          defaultDimensions:{
            w:640,
            h:480
          },
          useDefaultDimensionsAsMinimumSize:true
        }
      });
      lb.open();
    },
    onChangeTosCheckbox:function () {
      var checkbox = $('acceptCloudTosCheckbox');
      var optInButton = $('cloudTosAccept');
      if (checkbox.checked) {
        optInButton.removeClassName('disabled');
      } else {
        optInButton.addClassName('disabled');
      }
    },
    toggleInstitutionTos:function (ev) {
      var tos = $('institutionTos');
      if (tos) {
        tos.toggle();
        // Make sure the lightbox resizes to fit the content
        lightbox.getCurrentLightbox()._resizeAndCenterLightbox(false);
      }
    },
    setLightboxProcessing:function () {
      var lbContent = $('cloud-tos-lightbox');
      if (lbContent) {
        lbContent.innerHTML = '&nbsp;';
        lbContent.setStyle({height: '100%'});
        lbContent.addClassName('lb-loading');
      }
    },
    optOut:function () {
      var existingProfile = !!$('existingProfileWarning');
      if (!existingProfile || confirm(page.bundle.getString("optin.decline.confirm.existing"))) {
        this.setLightboxProcessing();
        var parameters = {};
        parameters[this.ajaxNonceKey] = this.ajaxNonce;
        new Ajax.Request(this.urlStem + 'optin/optOut', {
          parameters:parameters,
          onSuccess:function (response) {
            window.location.reload();
          },
          onFailure:function (response) {
            alert(page.bundle.getString("optin.processing.error"));
            window.location.reload();
          }
        });
      }
    },
    optIn:function () {
      var self = this;
      var optInButton = $('cloudTosAccept');
      if (!optInButton.hasClassName('disabled')) {
        this.setLightboxProcessing();
        var parameters = {};
        parameters[this.ajaxNonceKey] = this.ajaxNonce;
        new Ajax.Request(this.urlStem + 'optin/optIn', {
          parameters:parameters,
          onSuccess:function (response) {
            var body = response.responseJSON;
            if (!body) {
              alert(page.bundle.getString("optin.processing.error"));
              window.location.reload();
            } else {
              var sessionForm = $('optInSessionForm');
              sessionForm.target = '_top';
              sessionForm.action = self.sessionRedirectUri;
              sessionForm.token.value = body.token;
              sessionForm.ts.value = body.ts;
              sessionForm.n.value = body.n;
              sessionForm.cs.value = body.cs;
              sessionForm.sig.value = body.sig;
              sessionForm.dest.value = body.dest;
              sessionForm.submit();
            }
          },
          onFailure:function (response) {
            alert(page.bundle.getString("optin.processing.error"));
            window.location.reload();
          }
        });
      }
    }
  });
}());
