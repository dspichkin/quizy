'use strict';

var Page = require('../models/page');
var Lesson = require('../models/lesson');

var EditCtrl = function($scope, $stateParams, $log, $data, $location, $mdDialog) {
    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.go_home_page();
    }

    $scope.model['editor'] = {
        is_dirty_data: false,
        page_types: [{
            type: "text",
            text: "Страница с текстовым вопросом"
        }, {
            type: "checkbox",
            text: "Страница с выбором нескольких ответов"
        }, {
            type: "radiobox",
            text: "Страница с выбором одного ответа"
        }, {
            type: "pairs",
            text: "Страница с подбором пары"
        }],
        pages: [],
        current_page_index: 0,
        current_lesson: null,
        new_lesson: false,
        loading: false,
        unsaved: false
    };

    $scope.main.make_short_header();
    $scope.main.active_menu = 'lessons';

    // todo:  сделать loading на созание нового урока
    // создаем новый урок
    if (!$stateParams.lesson_id) {
        $scope.model.editor.new_lesson = true;
        /*
        $data.new_lesson().then(function(data) {
            if (data.hasOwnProperty('data')) {
                if (data.data.hasOwnProperty('id')) {
                    $location.path('/editor/' + data.data.id + '/');
                }
            }
        }, function(error) {
            $log.error('Ошибка создания нового урока', error);
        });
        */
    } else {
        $scope.model.editor.new_lesson = false;
        $data.get_lesson($stateParams.lesson_id).then(function(data) {
            $scope.model.editor.current_lesson = new Lesson(data.data);
            if (!data.data || data.data.length == 0) {
                $scope.main.go_home_page();
            } else {
                for (var i = 0, len = data.data.pages.length; i < len; i++) {
                    var q = new Page(data.data.pages[i]);
                    $scope.model.pages.push(q);
                }
            }
        }, function(error) {
            $scope.model.editor.current_lesson = null;
            $log.error('Ошибка получения урока', error);
            $scope.main.go_home_page();
        });
    }


    // Заново раздаем номера вопросам
    var re_number_pages = function() {
        for (var i = 0, len = $scope.model.editor.pages.length; i < len; i++) {
            $scope.model.editor.pages[i].number = i + 1;
        }

        $data.save_data($scope.model.editor.pages).then(function(response) {
            console.log($scope.model.editor.pages);
        }, function(error) {
            $log.error("Ошибка записи вопросов.", error);
        });
    };

    $scope.finish_moving = function($item, $partFrom, $partTo, $indexFrom, $indexTo) {
        for (var i = 0, len = $scope.model.editor.pages.length; i < len; i++) {
            if ($scope.model.editor.pages[i].id == $item.id) {
                $scope.model.editor.current_page_index = i;
            }
        }
        re_number_pages();
    };


    $scope.ta_toolbar = function() {
        /*
        ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'quote'],
        ['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo', 'clear'],
        ['justifyLeft', 'justifyCenter', 'justifyRight', 'indent', 'outdent'],
        ['html', 'insertImage','insertLink', 'insertVideo', 'wordcount', 'charcount']
         */
        return [['h1', 'h2', 'h3'], ['bold', 'italics'], ['p', 'pre', 'quote'],
            ['undo', 'clear']];
    };

    $scope.delete_current_lesson = function($event) {
        console.log($scope.model.editor.current_lesson)
        $mdDialog.show({
              targetEvent: $event,
              templateUrl: '/assets/partials/confirm_delete_lesson.html',
              disableParentScroll: true,
              clickOutsideToClose: true,
                scope: $scope,        // use parent scope in template
                preserveScope: true,
                controller: function DialogController($scope, $mdDialog) {

                    $scope.form_errors = {};
                    $scope.closeDialog = function() {
                        $mdDialog.hide();
                    };
                    $scope.submit = function($event) {
                        $event.preventDefault();
                        $mdDialog.hide();
                        $scope.model.editor.current_lesson.delete();
                        $scope.main.go_lessons_page();
                    };
                }
            });
    }

    $scope.add_page = function(type_slug) {
        $scope.model.editor.loading = true;
        var _new_page = Page({
            type: type_slug,
            number: $scope.model.editor.pages.length + 1,
            text: "",
            variants: []
        });


        _new_page.create($scope.model.editor.current_lesson.id).then(function(response) {
            _new_page.id = response.id;
            $scope.model.editor.pages.push(_new_page);
            $scope.model.editor.current_page_index = $scope.model.editor.pages.length - 1;
            $scope.add_variant(type_slug);
            $scope.$apply();
            $scope.model.editor.loading = false;
        }, function(error) {
            $scope.model.editor.loading = false;
            $log.error("Ошибка. Не могу создать новую страницу! ", error);
        });

    };

    $scope.change_page = function($index, $event) {
        $scope.model.editor.current_page_index = $index;
    };

    $scope.remove_page = function() {
        if (confirm("Вы действительно хотите удалить вопрос?")) {
            $scope.model.editor.loading = true;
            var current_index = $scope.model.editor.current_page_index;
            $scope.model.editor.pages[$scope.model.editor.current_page_index].remove().then(
                function(response) {
                    $scope.model.editor.pages.splice(current_index, 1);
                    if (current_index >= $scope.model.editor.pages.length - 1) {
                        $scope.model.editor.current_page_index = $scope.model.editor.pages.length - 1;
                    }
                    re_number_pages();
                    $scope.$apply();
                    $scope.model.editor.loading = false;
                }, function(error) {
                    $log.error("Ошибка удаленния вопроса. ", error);
                    $scope.model.editor.loading = false;
                });
        }
    };

    $scope.get_type_name = function(type_slug) {
        for (var i = 0, len = $scope.model.editor.page_types.length; i < len; i++) {
            if ($scope.model.editor.page_types[i].type == type_slug) {
                return $scope.model.editor.page_types[i].text;
            }
        }
    };

    $scope.changed_page_text = function() {
        $scope.model.is_dirty_data = true;
    };


    /**
     * Сохранение изменний
     * Если нет урока создаем его
     * @return {[type]} [description]
     */
    $scope.finish_changed_page_text = function() {
        $scope.model.editor.loading = true;
        $scope.model.editor.pages[$scope.model.current_page_index].save().then(
            function() {
                $scope.model.editor.loading = false;
                $scope.model.editor.is_dirty_data = false;
                $scope.$apply();
            },
            function(error) {
                $log.error("Ошибка сохранения вопроса. ", error);
                $scope.model.editor.loading = false;
            }
        );
    };

    $scope.add_variant = function(type) {
        $scope.model.editor.loading = true;
        if (type == 'radiobox' || type == 'checkbox') {
            var _variant = {
                text: "",
                right_answer: false
            };
            $scope.model.editor.pages[$scope.model.current_page_index]
                .new_variant(_variant).then(
                    function(data) {
                        _variant = data;
                        $scope.model.pages[$scope.model.current_page_index].variants.push(_variant);
                        $scope.$apply();
                        $scope.model.editor.loading = false;
                    },
                    function(error) {
                        $log.error("Ошибка создания нового варианта ответа. ", error);
                        $scope.model.editor.loading = false;
                    }
                );
        }

        if (type == 'pairs') {
            var _variant_page = {
                text: "",
                pair_type: "question"
            };
            var _variant_answer = {
                text: "",
                pair_type: "answer"
            };

            $scope.model.editor.pages[$scope.model.current_page_index]
                .new_variant(_variant_page).then(
                    function(data) {
                        _variant_question = data;
                        _variant_answer.pair = _variant_question.id;

                        $scope.model.pages[$scope.model.current_page_index]
                            .new_variant(_variant_answer).then(
                                function(data) {
                                    _variant_question.pair_object = data;
                                    $scope.model.pages[$scope.model.current_page_index].variants.push(_variant_question);
                                    $scope.$apply();
                                },
                                function(error) {
                                    $log.error("Ошибка создания нового варианта ответа. ", error);
                                    $scope.model.editor.loading = false;
                                }
                            );
                    },
                    function(error) {
                        $log.error("Ошибка создания нового варианта ответа. ", error);
                        $scope.model.editor.loading = false;
                    }
                );
        }

        if (type == 'text') {
            var _variant = {
                text: ""
            };
            $scope.model.editor.pages[$scope.model.current_page_index]
                .new_variant(_variant).then(
                    function(data) {
                        _variant = data;
                        $scope.model.editor.pages[$scope.model.current_page_index].variants.push(_variant);
                        $scope.$apply();
                        $scope.model.editor.loading = false;
                    },
                    function(error) {
                        $log.error("Ошибка создания нового варианта ответа. ", error);
                        $scope.model.editor.loading = false;
                    }
                );
        }
    };


    $scope.remove_variant = function(id) {
        $scope.model.editor.pages[$scope.model.current_page_index]
            .remove_variant(id).then(
                function(data) {
                    var _v = $scope.model.pages[$scope.model.current_page_index].variants;
                    var index = -1;
                    for (var i = 0, len = _v.length; i < len; i++) {
                        if (_v[i].id == id) {
                            index = i;
                            break;
                        }
                    }
                    if (index > -1) {
                        _v.splice(index, 1);
                        $scope.$apply();
                    }
                    $scope.model.editor.loading = false;
                },
                function(error) {
                    $log.error("Ошибка удаления варианта ответа. ", error);
                    $scope.model.editor.loading = false;
                }
            );
    };

    $scope.finish_changed_variant = function(id) {
        $scope.model.editor.loading = true;
        var _page = $scope.model.editor.pages[$scope.model.current_page_index];
        // console.log('_page', _page)
        _page.save().then(
            function(data) {
                $scope.model.editor.loading = false;
                $scope.model.editor.is_dirty_data = false;
                $scope.$apply();
            },
            function(error) {
                $log.error("Ошибка сохранения изменения ответа. ", error);
                $scope.model.editor.loading = false;
            }
        );
    };

    /**
     * Сохранение урока
     * @return {[type]} [description]
     */
    $scope.finish_changed_lesson = function() {
        //$scope.model.editor.new_lesson = true;
        /*
        $data.new_lesson().then(function(data) {
            if (data.hasOwnProperty('data')) {
                if (data.data.hasOwnProperty('id')) {
                    $location.path('/editor/' + data.data.id + '/');
                }
            }
        }, function(error) {
            $log.error('Ошибка создания нового урока', error);
        });
        */
        $scope.model.editor.loading = true;
        if ($scope.model.editor.new_lesson == true) {
            $data.new_lesson($scope.model.editor.current_lesson).then(function(data) {
                if (data.hasOwnProperty('data')) {
                    if (data.data.hasOwnProperty('id')) {
                        $scope.main.go_editor_lesson(data.data.id)
                    }
                }
            }, function(error) {
                $log.error('Ошибка создания нового урока', error);
            });
        } else {
            $scope.model.editor.current_lesson.save().then(function() {
                $scope.model.editor.loading = false;
                $scope.model.editor.is_dirty_data = false;
                $scope.$apply();
            }, function() {
                $log.error("Ошибка сохранения урока. ", error);
                $scope.model.editor.loading = false;
            });
        }


        
    };
/*
    var is_new_lesson = function(data) {
        if ($scope.model.editor.new_lesson == true) {
            $data.new_lesson(data).then(function(data) {
                if (data.hasOwnProperty('data')) {
                    if (data.data.hasOwnProperty('id')) {
                        // $location.path('/editor/lesson/' + data.data.id + '/');
                        $scope.main.go_editor_lesson(data.data.id)
                        return;
                    }
                }
            }, function(error) {
                $log.error('Ошибка создания нового урока', error);
            });
        }
    }
*/

    $scope.make_dirty_data = function() {
        $scope.model.editor.is_dirty_data = true;
    };


    $scope.$watch('model.editor.is_dirty_data', function(newValue, oldValue) {
        if (oldValue == false && newValue == true) {
            $scope.model.editor.unsaved = true;
        }
        if (oldValue == true && newValue == false) {
            $scope.model.editor.unsaved = false;
        }
    });





};


module.exports = ['$scope', '$stateParams', '$log', '$data', '$location', '$mdDialog', EditCtrl];
