'use strict';

var _ = require('lodash-node');

var config = function($stateProvider, $urlRouterProvider, $locationProvider) {

    $locationProvider.html5Mode(true).hashPrefix('!');

    $stateProvider
        .state('signup', {
            url: "/accounts/signup/",
            views: {
                "signup": {
                    templateUrl: "/accounts/ajax-signup/",
                    controller: 'SignupCtrl'
                }
            }
        })
        .state('confirm-email-send', {
            url: "/accounts/confirm-email/",
            views: {
                "confirm-email-send": {
                    templateUrl: "/accounts/ajax-confirm-email-send/",
                    controller: 'SignupCtrl'
                }
            }
        })
        .state('confirm-email', {
            url: "/accounts/confirm-email/:key/",
            views: {
                "confirm-email": {
                    templateUrl: "/accounts/ajax-confirm-email/",
                    controller: 'SignupConfirmCtrl'
                }
            }
        })
        .state('login', {
            url: "/accounts/login/",
            views: {
                "login": {
                    templateUrl: "/accounts/ajax-login/",
                    controller: 'LoginCtrl'
                }
            }
        })
        .state('profile', {
            url: "/accounts/profile/",
            templateUrl: "/assets/partials/profile.html",
            controller: 'ProfileCtrl'
        })
        .state('lessons', {
            url: "/lessons/",
            views: {
                "lessons": {
                    templateUrl: "/assets/partials/lessons.html",
                    controller: 'LessonsCtrl'
                }
            }
        })
        .state('editor', {
            url: "/editor/:lesson_id?",
            templateUrl: "/assets/partials/editor.html",
            controller: 'LessonsCtrl'
        })
        .state('editor_', {
            url: "/editor/:lesson_id/?",
            templateUrl: "/assets/partials/editor.html",
            controller: 'LessonsCtrl'
        })
        .state('play', {
            url: "/play/:lesson_id/?",
            templateUrl: "/assets/partials/play.html",
            controller: 'LessonsCtrl'
        })
        .state('djangoAccounts', {
            url: "^/accounts/{url:.*}"
        })
        .state('djangoAdmin', {
            url: "^/admin{url:.*}"
        })
        /*
        
        
        .state('statistics', {
            url: "/statistics",
            templateUrl: "/assets/partials/statistics.html",
            controller: 'StatisticsController'
        })
        
        
        */


    $urlRouterProvider
        .when(/^\/accounts/, '/accounts/profile')
        .otherwise('/lessons/');
};

var DJANGO_ACCOUNT_URLS = [
    'password/change', 'pasword/set',
    'inactive', 'email', 'password/reset',
    'social/signup', 'social/connections', 'social/login/error',
    'twitter/login', 'vk/login', 'facebook/login'
];
/*
var DJANGO_ACCOUNT_URLS = [
    'signup', 'login', 'logout', 'password/change', 'pasword/set',
    'inactive', 'email', 'confirm-email', 'password/reset',
    'social/signup', 'social/connections', 'social/login/error',
    'twitter/login', 'vk/login', 'facebook/login'
];
 */

var run = function($state, $rootScope, $location) {
    $rootScope.$on('$stateChangeStart', function(e, toState, toParams, fromState, fromParams) {
        if (toState.name === 'djangoAccounts') {
            var url = toParams.url, redirected = false;
            // Некоторые адресы в /accounts должны обрабатываться Angular,
            // а некторые Django
            _.forEach(DJANGO_ACCOUNT_URLS, function(djUrl) {
                var re = new RegExp('^' + djUrl);
                if (re.test(url)) {
                    e.preventDefault();  // Важно, чтобы браузерная кнопка "назад" работала

                    // Обойдем ui-router
                    window.location = '/accounts/' + djUrl + '/';
                    redirected = true;
                    return false;
                }
            });
            if (!redirected) {
                return $location.path('/accounts/profile');
            }
        }
        if (toState.name === 'djangoAdmin') {
            return window.location = '/admin' + toParams.url;
        }
    });
};

module.exports = {
    'config': ['$stateProvider', '$urlRouterProvider', '$locationProvider', config],
    'run': ['$state', '$rootScope', '$location', run]
};


