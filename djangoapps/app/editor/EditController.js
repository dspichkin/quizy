'use strict';

var Page = require('../models/page');
var Lesson = require('../models/lesson');

var EditCtrl = function($scope, $stateParams, $log, $data, $location) {


    $scope.model = {
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
        //name: "",
        pages: [],
        current_page_index: 0,
        current_lesson: null
    };

    // todo:  сделать loading на созание нового урока
    // создаем новый урок
    if ($stateParams.lesson_id == "") {
        $data.new_lesson().then(function(data) {
            if (data.hasOwnProperty('data')) {
                if (data.data.hasOwnProperty('id')) {
                    $location.path('/editor/' + data.data.id + '/');
                }
            }
        }, function(error) {
            $log.error('Ошибка создания нового урока', error);
        });
    } else {

        $data.get_lesson($stateParams.lesson_id).then(function(data) {
            $scope.model.current_lesson = new Lesson(data.data);
            for (var i = 0, len = data.data.pages.length; i < len; i++) {
                var q = new Page(data.data.pages[i]);
                $scope.model.pages.push(q);
            }
        }, function(error) {
            $scope.model.current_lesson = null;
            //$log.error('Ошибка получения урока', error);
            $location.path('/');
        });
    }

    var loading = {
        show: function() {
            $('#loading').show();
        },
        hide: function() {
            $('#loading').hide();
        }
    };
    var unsaved = {
        show: function() {
            $('#unsaved').show();
        },
        hide: function() {
            $('#unsaved').hide();
        }
    };

    
    // Заново раздаем номера вопросам
    var re_number_pages = function() {
        for (var i = 0, len = $scope.model.pages.length; i < len; i++) {
            $scope.model.pages[i].number = i + 1;
        }

        $data.save_data($scope.model.pages).then(function(response) {
            console.log($scope.model.pages);
        }, function(error) {
            $log.error("Ошибка записи вопросов.", error);
        });
    };

    $scope.finish_moving = function($item, $partFrom, $partTo, $indexFrom, $indexTo) {
        for (var i = 0, len = $scope.model.pages.length; i < len; i++) {
            if ($scope.model.pages[i].id == $item.id) {
                $scope.model.current_page_index = i;
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

   

    $scope.add_page = function(type_slug) {
        loading.show();
        var _new_page = Page({
            type: type_slug,
            number: $scope.model.pages.length + 1,
            text: "",
            variants: []
        });


        _new_page.create($scope.model.current_lesson.id).then(function(response) {
            _new_page.id = response.id;
            $scope.model.pages.push(_new_page);
            $scope.model.current_page_index = $scope.model.pages.length - 1;
            $scope.add_variant(type_slug);
            $scope.$apply();
            loading.hide();
        }, function(error) {
            loading.hide();
            $log.error("Ошибка. Не могу создать новую страницу! ", error);
        });

    };

    $scope.change_page = function($index, $event) {
        $scope.model.current_page_index = $index;
    };

    $scope.remove_page = function() {
        if (confirm("Вы действительно хотите удалить вопрос?")) {
            loading.show();
            var current_index = $scope.model.current_page_index;
            $scope.model.pages[$scope.model.current_page_index].remove().then(
                function(response) {
                    $scope.model.pages.splice(current_index, 1);
                    if (current_index >= $scope.model.pages.length - 1) {
                        $scope.model.current_page_index = $scope.model.pages.length - 1;
                    }
                    re_number_pages();
                    $scope.$apply();
                    loading.hide();
                }, function(error) {
                    $log.error("Ошибка удаленния вопроса. ", error);
                    loading.hide();
                });
        }
    };

    $scope.get_type_name = function(type_slug) {
        for (var i = 0, len = $scope.model.page_types.length; i < len; i++) {
            if ($scope.model.page_types[i].type == type_slug) {
                return $scope.model.page_types[i].text;
            }
        }
    };

    $scope.changed_page_text = function() {
        $scope.model.is_dirty_data = true;
    };

    $scope.finish_changed_page_text = function() {
        loading.show();
        $scope.model.pages[$scope.model.current_page_index].save().then(
            function() {
                loading.hide();
                $scope.model.is_dirty_data = false;
                $scope.$apply();
            },
            function(error) {
                $log.error("Ошибка сохранения вопроса. ", error);
                loading.hide();
            }
        );
    };

    $scope.add_variant = function(type) {
        loading.show();
        if (type == 'radiobox' || type == 'checkbox') {
            var _variant = {
                text: "",
                right_answer: false
            };
            $scope.model.pages[$scope.model.current_page_index]
                .new_variant(_variant).then(
                    function(data) {
                        _variant = data;
                        $scope.model.pages[$scope.model.current_page_index].variants.push(_variant);
                        $scope.$apply();
                        loading.hide();
                    },
                    function(error) {
                        $log.error("Ошибка создания нового варианта ответа. ", error);
                        loading.hide();
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

            $scope.model.pages[$scope.model.current_page_index]
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
                                    loading.hide();
                                }
                            );
                    },
                    function(error) {
                        $log.error("Ошибка создания нового варианта ответа. ", error);
                        loading.hide();
                    }
                );
        }

        if (type == 'text') {
            var _variant = {
                text: ""
            };
            $scope.model.pages[$scope.model.current_page_index]
                .new_variant(_variant).then(
                    function(data) {
                        _variant = data;
                        $scope.model.pages[$scope.model.current_page_index].variants.push(_variant);
                        $scope.$apply();
                        loading.hide();
                    },
                    function(error) {
                        $log.error("Ошибка создания нового варианта ответа. ", error);
                        loading.hide();
                    }
                );
        }
    };


    $scope.remove_variant = function(id) {
        $scope.model.pages[$scope.model.current_page_index]
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
                    loading.hide();
                },
                function(error) {
                    $log.error("Ошибка удаления варианта ответа. ", error);
                    loading.hide();
                }
            );
    };

    $scope.finish_changed_variant = function(id) {
        loading.show();
        var _page = $scope.model.pages[$scope.model.current_page_index];
        // console.log('_page', _page)
        _page.save().then(
            function(data) {
                loading.hide();
                $scope.model.is_dirty_data = false;
                $scope.$apply();
            },
            function(error) {
                $log.error("Ошибка сохранения изменения ответа. ", error);
                loading.hide();
            }
        );
    };

    $scope.finish_changed_lesson = function() {
        loading.show();
        $scope.model.current_lesson.save().then(function() {
            loading.hide();
            $scope.model.is_dirty_data = false;
            $scope.$apply();
        }, function() {
            $log.error("Ошибка сохранения урока. ", error);
            loading.hide();
        });
    };



    $scope.make_dirty_data = function() {
        $scope.model.is_dirty_data = true;
    };


    $scope.$watch('model.is_dirty_data', function(newValue, oldValue) {
        if (oldValue == false && newValue == true) {
            unsaved.show();
        }
        if (oldValue == true && newValue == false) {
            unsaved.hide();
        }
    });





};


module.exports = ['$scope', '$stateParams', '$log', '$data', '$location', EditCtrl];
