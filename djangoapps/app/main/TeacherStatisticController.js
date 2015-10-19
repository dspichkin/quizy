'use strict';


var TeacherStatisticCtrl = function($scope, $mdDialog, $http, $log, $location) {
    $scope.model = {
        pupils: []
    };


    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.go_home_page();
            }
        });
        return;
    } else if ($scope.user.account_type != 1) {
        $scope.main.go_home_page();
        return;
    }


    $scope.main.make_short_header();
    $scope.main.active_menu = 'statistic';


    load_statistic();


    function load_statistic(url) {
        var _page;
        if (!url) {
            url = '/api/statistic/';
            if (_page) {
                url += '?page=' + _page;
            }
        } else {
            _page = window.utils.getUrlVars(url).page;
        }
        if (!_page) {
            _page = 1;
        }


        $http.get(url).then(function(data) {
            $scope.model.pupils = data.data.results;
            var page_length = 10;
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
            $log.error('Ошибка получения статистики', error);
        });
    }


    $scope.remove_statistic = function($event, statistic_id) {
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: '/assets/partials/confirm/confirm_delete_statistic.html',
            disableParentScroll: true,
            clickOutsideToClose: true,
            scope: $scope,        // use parent scope in template
            preserveScope: true,
            controller: function DialogController($scope, $mdDialog) {
                $scope.closeDialog = function() {
                    $mdDialog.hide();
                };

                $scope.submit = function() {
                    $mdDialog.hide();
                    $http.delete('/api/statistic/' + statistic_id + '/').then(function(data) {
                        load_statistic();
                    }, function(error) {
                        $log.error(error);
                    });
                };
            }
        });
    };




};

module.exports = ['$scope', '$mdDialog', '$http', '$log', '$location', TeacherStatisticCtrl];


