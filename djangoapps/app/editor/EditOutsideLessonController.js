'use strict';


var EditOutsideLessonCtrl = function($scope, $stateParams, $http, $compile, $log) {

    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.go_home_page();
            }
        });
        return;
    }

    $scope.model['outside'] = {
        path: null,
        template: null,
        controller: null,
        lesson_type: null,
        course_id: null
    };

    $scope.main.make_short_header();
    $scope.main.active_menu = 'lessons';


    start();




    $scope.getController = function() {
        return 'ControllerName';
    };

    $scope.getTemplate = function() {
        return $scope.model.outside.template;
    };

    function load_enroll(enroll_id) {
        return $http.get('/api/enroll_teacher/' + enroll_id + "/").then(function(data) {
            $scope.model.outside.enroll = data.data;
            start_content(data);

            }, function(error) {
                $log.error('Ошибка получения назначенных на меня уроков', error);
            });

    };

    function start_content(data) {

        $scope.model.outside.lesson_type = data.data.lesson.lesson_type;
        $scope.model.outside.course_id = data.data.lesson.course;

        if (data.data.lesson.lesson_type == 'outside') {
            $scope.model.outside.path = data.data.lesson.content.path;
            $scope.model.outside.template = $scope.model.outside.path + data.data.lesson.content.teacher_template;
            $scope.model.outside.controller = $scope.model.outside.path + data.data.lesson.content.teacher_controller;
            var jsLink = $("<script type='text/javascript' src='" + $scope.model.outside.controller + "'>");
            $("head").append(jsLink);
            // Регистрация контроллера
            app.controllerProvider.register('ControllerName', app.ControllerName);

        }
    }

    function start() {
        if ($stateParams.enroll_id) {
            load_enroll($stateParams.enroll_id);
        } else {
            return;
        }
    };


}



module.exports = ['$scope', '$stateParams', '$http', '$compile', '$log', EditOutsideLessonCtrl];
