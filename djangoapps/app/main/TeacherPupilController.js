'use strict';
function getUrlVars(url)
{
    var vars = [], hash;
    var hashes = url.slice(url.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}


var _ = require('lodash-node');
var Pupil = require('../models/pupil');

var TeacherPupilCtrl = function($scope, $mdDialog, $http, $data, $log, $location) {
    $scope.model = {
        pupils: []
    };



    if (!$scope.user || !$scope.user.is_authenticated) {
        $.ajax({
            type: "GET",
            url: '/api/user/',
            async: false
        }).then(function(data) {
            $scope.user = {
                username: 'guest',
                is_authenticated: false,
                loaded: false
            };

            $scope.user = data;
            $scope.user.loaded = true;

        }, function(error) {
            $log.error('Ошибка получения данных', error);
        });

    }

    $scope.main.make_short_header();
    $scope.main.active_menu = 'pupils';


    $scope.load_pupils = function(url, callback) {
        if ($scope.user.account_type == 1) {
            var _page;
            if (!url) {
                var url = '/api/pupils/';
                if (_page) {
                    url += '?page=' + _page;
                }
            } else {
                _page = getUrlVars(url).page;
            }
            if (!_page) {
                _page = 1;
            }

            $http.get(url).then(function(data) {
                var page_length = 10;
                $scope.model.pupils = [];
                for (var i = 0, len = data.data.results.length; i < len; i++) {
                    $scope.model.pupils.push(new Pupil(data.data.results[i]));
                }
                var from_page = _page * page_length - page_length;
                if (!from_page) {
                    from_page = 1;
                }
                var to_page = _page * page_length;
                if (to_page > data.data.count) {
                    to_page = data.data.count;
                }
                $scope.model.page = {
                    next: data.data.next,
                    count: data.data.count,
                    previous: data.data.previous,
                    from_page: from_page,
                    to_page: to_page
                };

            }, function(error) {
                $log.error('Ошибка получения курсов', error);
            });
        } else {
            $location.path('/');
        }
    };

    $scope.remove_enroll = function(enroll_id) {
        $http.delete('/api/enroll_pupil/' + enroll_id + '/').then(function(data) {
            $scope.load_pupils();
        }, function(error) {
            $log.error(error);
        });
    };

    $scope.remove_course_enroll = function(enroll_id) {
        $http.delete('/api/enroll_course_pupil/' + enroll_id + '/').then(function(data) {
            $scope.load_pupils();
        }, function(error) {
            $log.error(error);
        });
    };


    // =================================
    $scope.load_pupils();

}



module.exports = ['$scope', '$mdDialog', '$http', '$log', '$location', TeacherPupilCtrl];

