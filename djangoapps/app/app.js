'use strict';

//global.jQuery = global.$ = require('jquery');
var angular = require('angular');
if (!angular.version) {
    // эта версия Angular не работает с require
    angular = global.angular;
}

var states = require('./states');

require('jquery');

require('angular-cookies');
require('angular-sanitize');
require('angular-ui-router');

require('angular-animate');
require('angular-aria');
require('angular-material');
require('angular-material-icons');

require('angular-parallax');

require('sortable');
require('rangy');
require('textAngular-sanitize');
require('textAngular');


require('./editor/filters');
require('./controllers');
require('./directives');

angular.module('quizy', [
        'ngSanitize',
        'ui.router',
        'ngMaterial',
        'ngMdIcons',
        'angular-sortable-view',
        'textAngular',
        'angular-parallax',

        'quizy.Controllers',
        'quizy.Directives',
        'quizy.filters'])
    .service('$data', require('./editor/EditDataService.js'))
    .config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }])
    .config(states.config)
    .run(states.run)





function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
