'use strict';

if (window.EXAM_SERVICE_TEMPLATES_PATH == undefined) {
    //window.EXAM_SERVICE_TEMPLATES_PATH = "templates/";
    window.EXAM_SERVICE_TEMPLATES_PATH = scriptURL() + "templates/";
}

var VD_STATES = {
    PLAY: 'play',
    READY: 'ready',
    //CLIENT: 'client',
    //PLAYER: 'player',
    //CHOICE: 'choice',
    INTRO: 'intro',
    //TEST: 'test',
    LOADING: 'loading',
    LOADED: 'loaded',
    WAITING_ANSWER: 'waiting_answer',
    SHOW_QUESTION: 'show_question',
    PENDING: 'pending',
    //REFLEXY: 'reflexy',
    //REVERT_PENDING: 'revert_pending',
    //REFLEXY_ACTIVE: 'reflexy_active',
    //REFLEXY_CLOSING: 'reflexy_closing',
    FINISHED: 'finished',
    //LAST_QUESTION_ENDED: 'ended'
};


var dialog = angular.module("dialog", [
    "ngSanitize"
])
.constant("VD_STATES", VD_STATES);




dialog.directive("dialog", ["$timeout",
    function($timeout) {
        return {
            restrict: "A",
            templateUrl: window.EXAM_SERVICE_TEMPLATES_PATH + "base.html",
            scope: {
                examUrl: "=dialog",
                onFinish: "=?",
                onReflexy: "=?",
                onReady: "=?"
            },
            controller: function() {
                var ctrl = this;
                $.extend(ctrl, TriggeredObject);
                /*
                    ctrl.quiz - объект содержимого диалога
                    задается в updateExam и корректируется настройкми по умолчанию при createModel
                */
                $.extend(ctrl, {
                    /**
                     * настройки теста или диалога по умолчанию
                     */
                    defaultSettings: {
                        /**
                         * задержка перд наачлом диалога
                         */
                        start_delay: 2000,
                        ///////////////////////////////////ШАБЛОН ДИАЛОГОВ////////////////////////////
                        /**
                         * Выбор HTML шаблона для вывода теста
                         */
                        template: window.EXAM_SERVICE_TEMPLATES_PATH + "dialog.html",
                    },
                    createModel: function() {
                        //console.log('createModel')
                        ctrl.quiz.settings = _.defaults(ctrl.quiz.settings, ctrl.defaultSettings);
                        var _api = new DialogApi(ctrl.quiz);
                        ctrl.model = new DialogModel(_api, ctrl.dialogCallbacks, function() {
                            ctrl.scope.$apply();
                        });
                        ctrl.model.init();
                    },
                    /**
                     * Все готово для воспроизведения теста (тест инициализирован, ресурсы загружены)
                     * Если introAvailable, иначе - запускаем тест
                     */
                    ready: function(total, loaded) {
                        //console.log('ready')
                        //ctrl.scope.ready = true;
                        ctrl.scope.start();
                    },
                    
                    /**
                     * отобразить новый вопрос
                     */
                    updateModel: function() {
                        // console.log('runNewQuestion')
                        ctrl.scope.model = ctrl.model;
                    },

                    /**
                     * Старт сервис
                     * @param  {[type]} new_value [description]
                     * @return {[type]}           [description]
                     */
                    updateExam: function(new_value) {
                        // console.log('updateExam', new_value)
                        /**
                         * если тест передан как атрибут директивы, то сразу начинаем тест , используя эти данные
                         */
                        if (typeof new_value == "object") {
                            ctrl.quiz = new_value;
                            ctrl.createModel();
                        } else {
                            // загрузка из файла
                        }
                        // Обновляем модель
                        ctrl.updateModel();
                    }
                });

                /*
                callbacks исполуемые в модели
                 */
                ctrl.dialogCallbacks = {
                    onFinish: function(data) {
                        //console.log('callbacks onFinish')
                    },
                    onStart: function(data) {
                        //console.log('callbacks onStart')
                    },
                    onReflexy: function(data) {
                        //console.log('callbacks onReflexy')
                    },
                    /**
                     * когда загружен данные теста
                     * @param data
                     */
                    onInit: function(data) {
                        //console.log('callbacks onInit')
                        // ctrl.loadMediaResources (data, ctrl.ready);
                        // запуск
                        ctrl.ready();
                    },
                    onUpdate: function(data) {
                        //console.log('callbacks onUpdate')

                    },
                    onNextStep: function(data) {
                        // ctrl.state("actor_state", VD_STATES.SHOW_QUESTION);
                        //console.log('callbacks onNextQuestion')
                    },
                    onSetAnswer: function(variant_id) {
                        //console.log('callbacks onSetAnswer')
                    }
                }


            },
            link: function(scope, elem, attr, ctrl) {
                // инициализация объекта состояний
                ctrl.states = scope.states = {};

                window.scope = ctrl.scope = scope;
                //window.scope = scope;


                function browserSupport() {
                 /*   //не поддерживаются браузеры IE < 9
                    if ($.browser.msie && $.browser.version < 8) return false;
                    //не поддерживаются браузер safari на windows (нет звука, глюки со стилями)
                    if ($.browser.safari && $.browser.win) return false;

                    ;*/
                    return true;
                }



                $.extend(scope, {

                    supported: browserSupport(),
                    /**
                     * готово ли прриложение к запуску
                     */
                    ready: false,
                    /**
                     * есть ли ошибки при инициализации
                     */
                    error: false,
                    getExamTemplate: function(tpl) {
                        return ctrl.model.getExamTemplate(tpl);
                    },
                    start: function() {
                        ctrl.model.start(function() {
                            ctrl.scope.ready = true;
                        });
                        
                    },
                    /**
                     * Выбор ответа
                     * @param event
                     * @param _variant_id
                     */
                    variantClick: function(event, _variant_id) {
                        if (event) {
                            event.stopPropagation();
                        }
                        // sounds.click();

                        ctrl.model.setAnswer(_variant_id, function(model) {
                            ctrl.scope.model = model;
                            
                        });
                    },
                    stopMedia: function() {
                        event.stopPropagation();
                        ctrl.scope.model.stop_media();
                    }
                });


                ctrl.run = function() {
                    ctrl.updateExam(scope.examUrl);
                };

                

                if (scope.supported) {
                    ctrl.run();
                }

            }
        };
    }
]);