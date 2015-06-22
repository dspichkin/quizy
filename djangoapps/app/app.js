'use strict';

//global.jQuery = global.$ = require('jquery');
var angular = require('angular');
if (!angular.version) {
    // эта версия Angular не работает с require
    angular = global.angular;
}

var states = require('./states');

require('angular-cookies');
require('angular-sanitize');
require('angular-bootstrap');
require('angular-ui-router');

require('jquery');

//require('pickerjs');
//require('hammerjs');
//require('materialize');

require('bootstrap');
require('sortable');
require('rangy');
require('textAngular-sanitize');
require('textAngular');


require('angularMaterialize');

require('./editor/filters');
require('./controllers');

angular.module('quizy', [
        'ngSanitize',
        'ngCookies',
        'ui.bootstrap',
        'ui.router',
        'ui.materialize',

        'angular-sortable-view',
        'textAngular',

        'quizy.Controllers',
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
