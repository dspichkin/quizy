'use strict';


var TeacherStatisticCtrl = function($scope, $http, $log, $location) {
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

    $scope.load_statistic = function(url) {
        var _page;
        if (!url) {
            var url = '/api/statistic/';
            if (_page) {
                url += '?page=' + _page;
            }
        } else {
            _page = utils.getUrlVars(url).page;
        }
        if (!_page) {
            _page = 1;
        }


        $http.get(url).then(function(data) {
            $scope.model.pupils = data.data.results;
            console.log($scope.model.pupils)
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


    // =============================
    $scope.load_statistic();


};

module.exports = ['$scope', '$http', '$log', '$location', TeacherStatisticCtrl];


