'use strict';

var Page = require('../models/page');
var Lesson = require('../models/lesson');
var Attempt = require('../models/attempt');

var PlayCtrl = function($scope, $http, $stateParams, $log, $location) {

    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.reset_menu();
                $location.path('/');
                return;
            }
        });
    }

    $scope.main.make_short_header();
    $scope.main.active_menu = 'lessons';






    $scope.model['play'] = {
        current_page_index: 0,
        next_question: false,
        result: null,
        success: null,
        lesson: null
    };

    scope.model.play['attempt'] = new Attempt({});

    var load_lesson = function(lesson_id) {
        $http.get('/api/lessons/' + lesson_id + "/").then(function(data) {
            $scope.model.play.lesson = data.data;

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
        var _pages = $scope.model.play.lesson.pages;
        if (_pages[$scope.model.play.current_page_index].type == 'checkbox' ||
            _pages[$scope.model.play.current_page_index].type == 'radiobox') {
            var _variants = _pages[$scope.model.play.current_page_index].variants;
            for (var i = 0, len = _variants.length; i < len; i++) {
                if (_variants[i].answer == true) {
                    return true;
                }
            }
        }
        if (_pages[$scope.model.play.current_page_index].type == 'pairs') {
            var _current_answers = $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index];
            // проверяем количество текущих ответов с ниобходим кол-вом ответов
            var _required_answers = $scope.model.play.lesson.pages[$scope.model.play.current_page_index].variants.length / 2;
            var _current_answers_number = 0;
            for (var i in _current_answers) {
                if (_current_answers[i].answer) {
                    _current_answers_number++;
                }
            }

            if (_current_answers_number == _required_answers) {
                return true;
            } else {
                return false;
            }
        }

        return false;
    };

    $scope.answer_ready = function() {
        $scope.model.play.next_question = has_answer();
        setTimeout(function() {
            $scope.$apply();
        });
    };


    $scope.make_answer = function(question_id, answer_id) {
        // записывае ответ сделанный пользователем
        var _pages = $scope.model.play.lesson.pages;
        if (_pages[$scope.model.play.current_page_index].type == 'pairs') {
            var _variants = _pages[$scope.model.play.current_page_index].variants;
            var _step = $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index];
            if (_step) {
                _step[question_id] = {
                    answer: answer_id,
                    question: question_id
                };
            } else {
                _step = {};
                _step[question_id] = {
                    answer: answer_id,
                    question: question_id
                };
            }

            //console.log("22 ", _step)
            $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index] = _step;
            $scope.answer_ready();
        }
        
    };

    $scope.next_question = function($event) {


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
    };


    $scope.get_answer_result = function(page_id) {
        for (var i = 0, len = $scope.model.answers.length; i < len; i++) {
            if ($scope.model.answers[i].page_id == page_id) {
                return $scope.model.answers[i].is_correct;
            }
        }
    };
};


module.exports = ['$scope', '$http', '$stateParams', '$log', '$location', PlayCtrl];