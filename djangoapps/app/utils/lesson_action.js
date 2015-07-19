'use strict';
require("../assets/js/velocity.min.js");

module.exports = ['$rootScope', '$compile', '$timeout',
    function($rootScope, $compile, $timeout) {
        return {
            restrict: "AE",
            scope: {
                lesson_id: "=lessonId",
                enroll_lessonFn: "=enrollLesson",
                play_lessonFn: "=playLesson",
                edit_lessonFn: "=editLesson"
            },
            replace: true,
            template: '<div class="" ng-click="show_action($event)" >' +
                '<a class="icon-menu" href="#"></a>' +
                '</div>',
            link: function(scope, elem, attr) {
                var element = elem[0];
                //scope.lesson_id = attr.lessonId;
                scope.close_action = function() {
                    $('.lesson_action').remove();
                };

                scope.show_action = function($event) {
                    $event.preventDefault();
                    var x = $event.pageX;
                    var y = $event.pageY;
                    var html_menu = '';
                    html_menu += '<div class="lesson_action" style="width:0px;">';
                    html_menu += '  <div class="lesson_action_shadow" ng-click="close_action()"></div>';
                    html_menu += '  <div class="shadow content" style="top:' + y + 'px;left:' + x + 'px;width:0;height:0;opacity:0;" ng-click="test()">';
                    html_menu += '      <div class="header">';
                    html_menu += '          <div class="header_close" ng-click="close_action()"></div>';
                    html_menu += '          <div class="header_delete"></div>';
                    html_menu += '          <div class="header_title">Меню урока</div>';
                    html_menu += '      </div>';
                    html_menu += '      <div class="action_menu_items" style="opacity: 0">';
                    html_menu += '          <div class="action_item" ng-click="edit_lesson()">Редактировать урок</div>';
                    html_menu += '          <div class="action_item" ng-click="enroll_lesson()">Назначить ученика</div>';
                    html_menu += '          <div class="action_item" ng-click="play_lesson($event)">Запустить для тестирования</div>';
                    html_menu += '      </div>';
                    html_menu += '  </div>';
                    html_menu += '</div>';
                    var e = $compile(html_menu)(scope);

                    $('body').append(e);
                    $(e).find('.content').velocity({
                        width: 300,
                        height: 237,
                        opacity: 1}, {
                            duration: 200,
                            complete: function() {
                                $(e).find('.action_menu_items').velocity({opacity: 1}, {duration: 200});
                            } });
                };

                scope.edit_lesson = function() {
                    scope.close_action();
                    scope.edit_lessonFn(scope.lesson_id);
                };

                scope.play_lesson = function() {
                    scope.close_action();
                    scope.play_lessonFn(scope.lesson_id);
                };

                scope.enroll_lesson = function($event) {
                    scope.close_action();
                    scope.enroll_lessonFn($event, scope.lesson_id);
                };
            }
        };
    }
];
