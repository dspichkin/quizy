'use strict';

var Page = require('../models/page');
var Lesson = require('../models/lesson');


var EditCtrl = function($scope, $sce, $http, $stateParams, $log, $data, $location, $mdDialog, Upload) {
    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.reset_menu();
                $location.path('/');
                return;
            }
        });
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
        }, {
            type: "words_in_text",
            text: "Страница с подбором слов в тексте"
        }],
        pages: [],
        current_page_index: 0,
        current_lesson: null,
        new_lesson: false,
        loading: false,
        unsaved: false
    };
    // для отображения прогресса загрузки медиа контента
    $scope.progressUpload = 0;

    $scope.main.make_short_header();
    $scope.main.active_menu = 'courses';

    $scope.current_menu = 'common';

    $scope.reload_lesson = function(callback) {
        $data.get_lesson($stateParams.lesson_id).then(function(data) {
            // Определения типа урока
            if (data.data.lesson_type != 'inside') {
                $scope.main.reset_menu();
                $location.path('/');
            }

            var _is_correct = data.data.is_correct;
            var l = new Lesson(data.data);

            // изменяет variants для pairs
            for (var x = 0, lenx = l.pages.length; x < lenx; x++) {

                if (l.pages[x].type == 'pairs') {
                    var _raw_variants = l.pages[x].variants;
                    var _new_variants = [];
                    for (var i = 0, len = _raw_variants.length; i < len; i++) {
                        if (_raw_variants[i].pair_type == "answer") {
                            var _answer = _raw_variants[i];
                            var _page;
                            for (var j = 0, len = _raw_variants.length; j < len; j++) {
                                if (_raw_variants[j].id == _answer.pair) {
                                    _page = _raw_variants[j];
                                    _page.pair_object = _answer;

                                    _new_variants.push(_page);
                                }
                            }
                        }
                    }
                    l.pages[x].variants = _new_variants;
                }
            }

            $scope.model.editor.current_lesson = l;
            $scope.detect_media_type();
            // проверяем на правильность во время загрузки
            var _c = $scope.model.editor.current_lesson.is_correct;
            $scope.model.editor.current_lesson.check();

            if (_is_correct != $scope.model.editor.current_lesson.is_correct) {
                $scope.model.editor.current_lesson.save();
            }

            // Todo сделать обработку ситуации
            if (!data.data || data.data.length == 0) {
                $scope.main.go_home_page();
            }

            if (callback) {
                callback();
            }

        }, function(error) {
            $scope.model.editor.current_lesson = null;
            $log.error('Ошибка получения урока', error);
            $scope.main.go_home_page();
        });
    };


    // todo:  сделать loading на созание нового урока
    // создаем новый урок
    if (!$stateParams.lesson_id) {
        // создаем новый урок
        $scope.model.editor.new_lesson = true;

        if (!$scope.main.current_course) {
            $location.path('/');
            return;
        } else {
            $scope.model.editor.current_lesson = new Lesson({
                course: $scope.main.current_course
            });
        }

        $scope.model.editor.current_lesson.create().then(function(data) {
            $scope.$apply(function() {
                $location.path('/editor/lesson/' + data.id + '/');
                $scope.main.make_short_header();
            });
        }, function(error) {
            $log.error('Ошибка создания нового урока', error);
        });
    } else {
        $scope.model.editor.new_lesson = false;
        $scope.reload_lesson();
    }






    // Заново раздаем номера вопросам
    var re_number_pages = function() {
        for (var i = 0, len = $scope.model.editor.current_lesson.pages.length; i < len; i++) {
            $scope.model.editor.current_lesson.pages[i].number = i + 1;
        }

        $data.save_data($scope.model.editor.current_lesson.pages).then(function(response) {
        }, function(error) {
            $log.error("Ошибка записи вопросов.", error);
        });
    };


    $scope.go_current_course = function(course_id) {
        $location.path('/courses/' + course_id + '/');
    };

    $scope.go_edit_current_course = function(course_id) {
        $location.path('/editor/course/' + course_id + '/');
    };

    $scope.show_editor_common = function() {
        $scope.current_menu = 'common';
    };

    $scope.show_editor_content = function() {
        $scope.current_menu = 'content';
    };

    $scope.get_template_content = function() {
        if ($scope.current_menu == 'common') {
            return '/assets/partials/editor/editor_lesson_common.html';
        }

        if ($scope.current_menu == 'content') {
            return '/assets/partials/editor/editor_lesson_content.html';
        }
    };


    var move_in_array = function(array, old_index, new_index) {
        if (new_index >= array.length) {
            var k = new_index - array.length;
            while ((k--) + 1) {
                this.push(undefined);
            }
        }
        array.splice(new_index, 0, array.splice(old_index, 1)[0]);
        return array; // for testing purposes
    };

    $scope.page_up = function(page_id) {
        var _page = $scope.model.editor.current_lesson.pages;
        var _current_page_index = null;
        for (var i = 0, len = $scope.model.editor.current_lesson.pages.length; i < len; i++) {
            if ($scope.model.editor.current_lesson.pages[i].id == page_id) {
                _current_page_index = i;
            }
        }
        if (_current_page_index > 0) {
            move_in_array(_page, _current_page_index, _current_page_index - 1);

        }
        re_number_pages();
    };
    $scope.page_down = function(page_id) {
        var _page = $scope.model.editor.current_lesson.pages;
        var _current_page_index = null;
        for (var i = 0, len = $scope.model.editor.current_lesson.pages.length; i < len; i++) {
            if ($scope.model.editor.current_lesson.pages[i].id == page_id) {
                _current_page_index = i;
            }
        }
        if (_current_page_index < _page.length) {
            move_in_array(_page, _current_page_index, _current_page_index + 1);

        }
        re_number_pages();
    };


    $scope.delete_current_lesson = function($event) {
        var _course_id = $scope.model.editor.current_lesson.course.id;
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: '/assets/partials/confirm/confirm_delete_lesson.html',
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
                        $scope.main.go_courses_page(_course_id);
                    };
                }
            });
    };

    $scope.delete_current_page = function($event) {
        $mdDialog.show({
              targetEvent: $event,
              templateUrl: '/assets/partials/confirm/confirm_delete_page.html',
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
                        $scope.model.editor.loading = true;
                        var current_index = $scope.model.editor.current_page_index;
                        $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index].remove().then(
                            function(response) {
                                $scope.model.editor.current_lesson.pages.splice(current_index, 1);
                                if (current_index >= $scope.model.editor.current_lesson.pages.length - 1) {
                                    $scope.model.editor.current_lesson.current_page_index = $scope.model.editor.current_lesson.pages.length - 1;
                                }
                                re_number_pages();
                                $scope.model.editor.current_page_index = 0;
                                $scope.$apply();
                                $scope.model.editor.loading = false;
                            }, function(error) {
                                $log.error("Ошибка удаленния вопроса. ", error);
                                $scope.model.editor.loading = false;
                            });
                                };
                            }
            });
    };

    $scope.add_page = function(type_slug) {
        $scope.model.editor.loading = true;
        var _new_page = Page({
            type: type_slug,
            number: $scope.model.editor.current_lesson.pages.length + 1,
            text: "",
            code_errors: {},
            variants: []
        });


        _new_page.create($scope.model.editor.current_lesson.id).then(function(response) {
            _new_page.id = response.id;
            $scope.reload_lesson(function() {
                $scope.model.editor.current_page_index = $scope.model.editor.current_lesson.pages.length - 1;
                if ($scope.model.editor.current_page_index < 0) {
                    $scope.model.editor.current_page_index = 0;
                }

                setTimeout(function() {
                    $scope.$apply();
                    $scope.add_variant($scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index].type);
                    $scope.model.editor.current_lesson.check();
                });

                $scope.model.editor.loading = false;
            });
        }, function(error) {
            $scope.model.editor.loading = false;
            $log.error("Ошибка. Не могу создать новую страницу! ", error);
        });

    };

    /**
     * Определем медиа тип вопроса для текущей страницы
     */
    $scope.detect_media_type = function() {
        var _current_page = $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index];
        if (_current_page && _current_page.hasOwnProperty('media')) {
            var _filename = _current_page.media;
            if (_filename) {
                var _ext = _filename.substr(_filename.length - 3);
                if (_ext == 'mp4') {
                    $scope.model.editor.media_type = 'video';
                    $scope.model.editor.media_sources = [{
                        src: $sce.trustAsResourceUrl(_current_page.media),
                        type: "video/mp4"
                    }];
                }
                if (_ext == 'webm') {
                    $scope.model.editor.media_type = 'video';
                    $scope.model.editor.media_sources = [{
                        src: $sce.trustAsResourceUrl(_current_page.media),
                        type: "video/webm"
                    }];
                }
                if (_ext == 'mp3') {
                    $scope.model.editor.media_type = 'audio';
                    $scope.model.editor.media_sources = [{
                        src: $sce.trustAsResourceUrl(_current_page.media),
                        type: "audio/mp3"
                    }];
                }
                if (_ext == 'jpg' || _ext == 'png' || _ext == 'gif') {
                    $scope.model.editor.media_type = 'image';
                }
            }
        }
    };

    $scope.change_page = function($index, $event) {
        $scope.model.editor.current_page_index = $index;
        $scope.model.editor.current_lesson.check();
        $scope.detect_media_type();
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
     * Сохранение изменний на странице
     */
    $scope.finish_changed_page_text = function() {
        $scope.model.editor.loading = true;
        $scope.model.editor.current_lesson.check();
        $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index].save().then(
            function() {
                $scope.model.editor.loading = false;
                $scope.model.editor.is_dirty_data = false;
                $scope.$apply();
            },
            function(error) {
                $log.error("Ошибка сохранения текущей страницы. ", error);
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
            $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index]
                .new_variant(_variant).then(
                    function(data) {
                        _variant = data;
                        $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index].variants.push(_variant);
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

            $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index]
                .new_variant(_variant_page).then(
                    function(data) {
                        var _variant_question = data;
                        _variant_answer.pair = _variant_question.id;

                        $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index]
                            .new_variant(_variant_answer).then(
                                function(data) {
                                    _variant_question.pair_object = data;
                                    $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index].variants.push(_variant_question);
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
        if (type == 'text' || type == 'words_in_text') {
            var _variant = {
                code_errors: {},
                is_correct: true,
                number: 1,
                text: ""
            };
            $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index]
                .new_variant(_variant).then(
                    function(data) {
                        $scope.reload_lesson(function() {
                            $scope.model.editor.loading = false;
                        });
                    },
                    function(error) {
                        $log.error("Ошибка создания нового варианта ответа. ", error);
                        $scope.model.editor.loading = false;
                    }
                );
        }
    };


    $scope.remove_variant = function(id) {
        $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index]
            .remove_variant(id).then(
                function(data) {
                    var _v = $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index].variants;
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
        $scope.model.editor.current_lesson.check();
        var _page = $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index];
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
     */
    $scope.finish_changed_lesson = function() {
        $scope.model.editor.loading = true;

        if ($scope.model.editor.new_lesson == false) {
            $scope.model.editor.current_lesson.check();
            $scope.model.editor.current_lesson.save().then(function() {
                $scope.model.editor.loading = false;
                $scope.model.editor.is_dirty_data = false;
                $scope.$apply();
            }, function(error) {
                $log.error("Ошибка сохранения урока. ", error);
                $scope.model.editor.loading = false;
            });
        }
    };


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

    

    $scope.upload = function($files, $event) {
        var file = $files[0];
        Upload.upload({
            url: 'api/lessons/' + $scope.model.editor.current_lesson.id + '/upload/',
            file: file
        }).progress(function(evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            //console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
            $scope.progressUpload = progressPercentage + '%';
        }).success(function(data, status, headers, config) {
            $scope.progressUpload = 0;
            $scope.reload_lesson(function() {
                setTimeout(function() {
                    $scope.$apply();
                });
            });

        }).error(function(data, status, headers, config) {
            $log.error('Ошибка загрузки: ' + status);
            $scope.progressUpload = 0;
            $scope.reload_lesson();
            setTimeout(function() {
                $scope.$apply();
            });
        });
    };
    $scope.page_picture_upload = function($files, $event) {
        var file = $files[0];
        Upload.upload({
            url: 'api/pages/' + $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index].id + '/upload/',
            file: file
        }).progress(function(evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            $scope.progressUpload = progressPercentage + '%';
        }).success(function(data, status, headers, config) {
            $scope.progressUpload = 0;
            $scope.reload_lesson();
            setTimeout(function() {
                $scope.$apply();
            });
        }).error(function(data, status, headers, config) {
            $log.error('Ошибка загрузки: ' + status);
            $scope.progressUpload = 0;
            $scope.reload_lesson();
            setTimeout(function() {
                $scope.$apply();
            });
        });
    };

    $scope.remove_lesson_picture = function() {
        $scope.model.editor.current_lesson.remove_lesson_media().then(function() {
            $scope.reload_lesson();
            setTimeout(function() {
                $scope.$apply();
            });
        }, function() {
            $log.error("Ошибка удаления картинки урока.", error);
        });
    };

    $scope.remove_question_media = function() {
        $scope.model.editor.current_lesson.pages[$scope.model.editor.current_page_index].remove_page_media().then(function() {
            $scope.reload_lesson(function() {
                setTimeout(function() {
                    $scope.$apply();
                });
            });

        }, function() {
            $log.error("Ошибка удаления картинки урока.", error);
        });
    };


};


module.exports = ['$scope', '$sce', '$http', '$stateParams', '$log', '$data', '$location', '$mdDialog', 'Upload', EditCtrl];
