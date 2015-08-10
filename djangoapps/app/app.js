'use strict';

//global.jQuery = global.$ = require('jquery');
var angular = require('angular');
if (!angular.version) {
    // эта версия Angular не работает с require
    angular = global.angular;
}

var states = require('./states');

window.jQuery = window.$ = require('jquery');

require('angular-cookies');
require('angular-sanitize');
require('angular-ui-router');

require('angular-animate');
require('angular-aria');
require('angular-material');
require('angular-material-icons');

//require('angular-parallax');

require('ng-file-upload');

//require('angular-dragdrop');
require('videogular');
require('vg-controls');
require('vg-overlay-play');
require('vg-poster');


require('./editor/filters');
require('./controllers');
require('./directives');

require('./utils/utils')
//'ngDragDrop',
//'angular-parallax',
window.app = angular.module('quizy', [
        'ngCookies',
        'ngSanitize',
        'ui.router',
        'ngMaterial',
        'ngMdIcons',

        "com.2fdevs.videogular",
        "com.2fdevs.videogular.plugins.controls",
        "com.2fdevs.videogular.plugins.overlayplay",
        "com.2fdevs.videogular.plugins.poster",

        'ngFileUpload',
        'quizy.Controllers',
        'quizy.Directives',
        'quizy.filters'])
    .service('$data', require('./editor/EditDataService.js'))
    .config(states.config)
    .run(states.run);

app.config(function($controllerProvider) {
    app.controllerProvider = $controllerProvider;
})
//.config(['$httpProvider', function($httpProvider) {
//    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
//    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
//}])


/*
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
*/
