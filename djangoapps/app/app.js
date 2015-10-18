'use strict';

global.jQuery = global.$ = require('jquery');
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
require('angular-gettext');

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

require('./utils/utils');
require('./utils/angular-ckeditor.js');
//'ngDragDrop',
//'angular-parallax',
window.app = angular.module('quizy', [
        'ngCookies',
        'ngSanitize',
        'ui.router',
        'ngMaterial',
        'ngMdIcons',
        'ngCkeditor',
        'gettext',

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
    //.run(states.run)
    .run(function(gettextCatalog) {
        //states.run();

        gettextCatalog.loadRemote('/assets/js/translations.json');
        gettextCatalog.debug = true;

    }); //states.run


app.config(function($controllerProvider, $mdThemingProvider) {
    app.controllerProvider = $controllerProvider;

    $mdThemingProvider.definePalette('amazingPaletteName', {
        '50': 'ffcdd2',
        '100': 'ffcdd2',
        '200': 'ef9a9a',
        '300': 'e57373',
        '400': '29b6f6',
        '500': '03a9f4',
        '600': '039be5',
        '700': '0288d1',
        '800': '0277bd',
        '900': '01579b',
        'A100': '80d8ff',
        'A200': '40c4ff',
        'A400': '00b0ff',
        'A700': '0091ea',
        //'contrastDefaultColor': 'light',    // whether, by default, text (contrast)
                                            // on this palette should be dark or light
        'contrastDarkColors': ['400', 'A100'],
        'contrastLightColors': undefined    // could also specify this if default was 'dark'
      });

    $mdThemingProvider.theme('default')
    .primaryPalette('amazingPaletteName')
    .accentPalette('orange');

    
});



