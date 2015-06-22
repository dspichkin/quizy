'use strict';

var _ = require('lodash-node');
var Lesson = require('../models/lesson');

var LessonsCtrl = function($scope, $http, $modal, $data, $timeout, $log, $location) {

    $scope.model = {
        lessons: [],
        lessons_for_me: [],
        archive: []
    };

    var load_lesson = function(callback) {
        $http.get('/api/mylessons/').then(function(data) {
            $scope.model.lessons_for_me = [];
            for (var i = 0, len = data.data.length; i < len; i++) {
                var l = new Lesson(data.data[i]);
                $scope.model.lessons_for_me.push(l);
            }
        }, function(error) {
            $log.error('Ошибка получения назначенных на меня уроков', error);
        });

        $http.get('/api/lessons/').then(function(data) {
            $scope.model.lessons = [];
            for (var i = 0, len = data.data.length; i < len; i++) {
                var l = new Lesson(data.data[i]);
                $scope.model.lessons.push(l);
            }
        }, function(error) {
            $log.error('Ошибка получения уроков', error);
        });

        $http.get('/api/archive/').then(function(data) {
            $scope.model.archive = [];
            for (var i = 0, len = data.data.length; i < len; i++) {
                var l = new Lesson(data.data[i]);
                $scope.model.archive.push(l);
            }
            if (callback) {
                callback();
            }
        }, function(error) {
            $log.error('Ошибка получения архива уроков', error);
        });
    };

    $scope.delete_lesson = function(lesson_id) {
        var _index = -1;
        for (var i = 0, len = $scope.model.lessons.length; i < len; i++) {
            if ($scope.model.lessons[i].id == lesson_id) {
                _index = i;
                break;
            }
        }

        if (_index > -1) {
            $scope.model.lessons[_index].remove().then(function() {
                $scope.model.lessons.splice(_index, 1);
                $scope.$apply();
            }, function() {
                $log.error("Ошибка удаления урока.", error);
            });
        }
    };

    $scope.edit_lesson = function(lesson_id) {
        $location.path('/editor/' + lesson_id + '/');
    };

    $scope.play_lesson = function(lesson_id) {
        $location.path('/play/' + lesson_id + '/');
    };


    $scope.lesson_enroll = function(lesson_id) {
        var modalLessonEnroll = $modal.open({
            animation: true,
            templateUrl: 'modalContentLessonEnroll.html',
            controller: 'ModalInstanceLessonEnrollCtrl',
            size: 'lg',
            resolve: {
                lesson_id: function() {
                  return lesson_id;
                }
            }
        });

        modalLessonEnroll.result.then(function() {
            load_lesson();
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };


    $scope.play_lesson = function(lesson_id) {
        $location.path('/play/' + lesson_id + '/');
    }

    $scope.move_to_archive = function(lesson_id) {
        $http.post('/api/archive/' + lesson_id + "/").then(function(data) {
            load_lesson();
        }, function(error) {
            $log.error('Ошибка перемещения урока в архив', error);
        });
    }


    // =============================
    load_lesson()


};

module.exports = ['$scope', '$http', '$modal', '$data', '$timeout', '$log', '$location', LessonsCtrl];