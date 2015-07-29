'use strict';

var _ = require('lodash-node');

var config = function($stateProvider, $urlRouterProvider, $locationProvider) {

    $locationProvider.html5Mode(true).hashPrefix('!');

    $stateProvider
        .state('main', {
            url: "/",
            views: {
                "main": {
                    templateUrl: "/assets/partials/main.html",
                    //controller: 'MainCtrl'
                }
            }
        })
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
                    templateUrl: "/accounts/ajax-login/"
                }
            }
        })
        .state('profile', {
            url: "/accounts/profile/",
            views: {
                "main": {
                    templateUrl: "/assets/partials/profile.html",
                    controller: 'ProfileCtrl'
                }
            }
        })
        .state('courses', {
            url: "/courses/",
            views: {
                "main": {
                    templateUrl: "/assets/partials/courses/courses.html",
                    controller: "TeacherCoursesCtrl"
                }
            }
        })
        .state('course', {
            url: "/courses/:course_id/",
            views: {
                "main": {
                    templateUrl: "/assets/partials/courses/course.html",
                    controller: "TeacherCourseCtrl"
                }
            }
        })
        .state('lessons', {
            url: "/lessons/",
            views: {
                "main": {
                    templateUrl: "/assets/partials/lessons.html",
                    controller: "PupilLessonsCtrl"
                }
            }
        })
        .state('pupils', {
            url: "/pupils/",
            views: {
                "main": {
                    templateUrl: "/assets/partials/pupils.html",
                    controller: "TeacherPupilCtrl"
                }
            }
        })
        .state('price', {
            url: "/price/",
            views: {
                "main": {
                    templateUrl: "/assets/partials/price.html",
                    controller: 'MainCtrl'
                }
            }
        })
        .state('editor_lesson', {
            url: "/editor/lesson/:lesson_id/",
            views: {
                "main": {
                    templateUrl: "/assets/partials/editor_lesson.html",
                    controller: 'EditLessonCtrl'
                }
            }
        })
        .state('new_editor_lesson', {
            url: "/editor/lesson/",
            views: {
                "main": {
                    templateUrl: "/assets/partials/editor_lesson.html",
                    controller: 'EditLessonCtrl'
                }
            }
        })
        .state('play', {
            url: "/play/:enroll_id/?",
            views: {
                "main": {
                    templateUrl: "/assets/partials/play.html",
                    controller: 'PlayCtrl'
                }
            }
        })
        .state('play_demo', {
            url: "/play/demo/:lesson_id/?",
            views: {
                "main": {
                    templateUrl: "/assets/partials/play.html",
                    controller: 'PlayCtrl'
                }
            }
        })
        .state('djangoAccounts', {
            url: "^/accounts/{url:.*}"
        })
        .state('djangoAdmin', {
            url: "^/admin/{url:.*}"
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
        .otherwise('/');
};

var DJANGO_ACCOUNT_URLS = [
    'admin',
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

var run = function($state, $rootScope, $location, $http, $cookies) {
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

    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
};

module.exports = {
    'config': ['$stateProvider', '$urlRouterProvider', '$locationProvider', config],
    'run': ['$state', '$rootScope', '$location', '$http', '$cookies', run]
};


