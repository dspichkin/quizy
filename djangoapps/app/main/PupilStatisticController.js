'use strict';
/*global
window: false,
module: false */ 

var PupilStatisticCtrl = function($scope, $http, $log, $location, $mdDialog) {
    $scope.loaded = false;
    $scope.model = {
        enrolls: []
    };


    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.go_home_page();
            }
        });
        return;
    } else if ($scope.user.account_type != 2) {
        $scope.main.go_home_page();
        return;
    }


    $scope.main.make_short_header();
    $scope.main.active_menu = 'statistic';

    $scope.load_statistic = function(url) {
        var _page;
        if (!url) {
            url = '/api/mystatistic/';
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
                $scope.model.enrolls = data.data.results;

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
                $scope.loaded = true;

            }, function(error) {
                $scope.loaded = true;
                $log.error('Ошибка получения курсов', error);
            });
    };


     $scope.show_data = function($event, enroll) {
        //var data = 'data'
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: '/assets/lessons/1/show_archive.html',
            disableParentScroll: true,
            clickOutsideToClose: true,
            preserveScope: true,
            controller: function DialogController($scope, $mdDialog) {
                $scope.enroll = enroll;
                $scope.closeDialog = function() {
                    $mdDialog.hide();
                };
                
            }
        });
    };

    // =============================
    $scope.load_statistic();


};

module.exports = ['$scope', '$http', '$log', '$location', '$mdDialog', PupilStatisticCtrl];


