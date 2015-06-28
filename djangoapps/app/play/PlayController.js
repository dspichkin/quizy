'use strict';

var Page = require('../models/page');
var Lesson = require('../models/lesson');

var PlayCtrl = function($scope, $http, $stateParams, $log, $location) {
    if (!$scope.user || !$scope.user.is_authenticated) {
        $location.path('/');
    }


    $scope.model = {
        current_page_index: 0,
        next_question: false,
        answers: [],
        result: null,
        success: null
    };

    var load_lesson = function(lesson_id) {
        $http.get('/api/lessons/' + lesson_id + "/").then(function(data) {
            $scope.model.lesson = data.data;

        }, function(error) {
            $log.error('Ошибка получения назначенных на меня уроков', error);
        });
    };


    if ($stateParams.lesson_id != "") {
        load_lesson($stateParams.lesson_id);
    } else {
        return;
    }

    var has_answer = function() {
        var _pages = $scope.model.lesson.pages;
        if (_pages[$scope.model.current_page_index].type == 'checkbox' ||
            _pages[$scope.model.current_page_index].type == 'radiobox') {
            var _variants = _pages[$scope.model.current_page_index].variants;
            for (var i = 0, len = _variants.length; i < len; i++) {
                if (_variants[i].answer == true) {
                    return true;
                }
            }
        }

        return false;
    };

    $scope.answer_ready = function() {
        $scope.model.next_question = has_answer();
    };

    $scope.next_question = function() {

        if ($scope.model.next_question == true) {
            $scope.model.current_page_index++;
        }

        // Прверяем ответы
        if ($scope.model.current_page_index == $scope.model.lesson.pages.length) {
            $scope.model.answers = [];
            var _pages = $scope.model.lesson.pages;
            for (var i = 0, len = _pages.length; i < len; i++) {
                var _is_correct = true;
                if (_pages[i].type == 'checkbox' || _pages[i].type == 'radiobox') {
                    for (var j = 0, lenj = _pages[i].variants.length; j < lenj; j++) {
                        if (_pages[i].variants[j].right_answer == true) {
                            if (_pages[i].variants[j].hasOwnProperty('answer') == true) {
                                if (_pages[i].variants[j].answer != _pages[i].variants[j].right_answer) {
                                    _is_correct = false;
                                }
                            } else {
                                _is_correct = false;
                            }
                        } else {
                            if (_pages[i].variants[j].hasOwnProperty('answer') == true) {
                                _is_correct = false;
                            }
                        }
                    }
                    $scope.model.answers.push({
                        "page_id": _pages[i].id,
                        "is_correct": _is_correct
                    });
                }

            }

            $http.post('/api/answers/' + $scope.model.lesson.id + "/", $scope.model.answers)
                .then(function(data) {
                    $scope.model.result = data.data;
                    // вычесляем success
                    var _success = true;
                    for (var i = 0, len = $scope.model.answers.length; i < len; i++) {
                        if ($scope.model.answers[i].is_correct == false) {
                            _success = false;
                        }
                    }
                    $scope.model.success = _success;
                }, function(error) {
                    $log.error('Ошибка записи результатов', error);
                });
            //console.log('$scope.model.answers ', $scope.model.answers)
        }

        $scope.model.next_question = false;
    }


    $scope.get_answer_result = function(page_id) {
        for (var i = 0, len = $scope.model.answers.length; i < len; i++) {
            if ($scope.model.answers[i].page_id == page_id) {
                return $scope.model.answers[i].is_correct;
            }
        }
    }
};


module.exports = ['$scope', '$http', '$stateParams', '$log', '$location', PlayCtrl];