'use strict';
require("../assets/js/velocity.min.js");

module.exports = ['$rootScope', '$compile', '$timeout',
    function($rootScope, $compile, $timeout) {
        return {
            restrict: "AE",
            scope: {
                course_id: "=courseId",
                enroll_courseFn: "=enrollCourse",
                edit_courseFn: "=editCourse"
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
                    html_menu += '  <div class="shadow content" style="top:' + y + 'px;left:' + x + 'px;width:0;height:0;opacity:0;">';
                    html_menu += '      <div class="header">';
                    html_menu += '          <div class="header_close" ng-click="close_action()"></div>';
                    //html_menu += '          <div class="header_delete"></div>';
                    html_menu += '          <div class="header_title">Course menu</div>';
                    html_menu += '      </div>';
                    html_menu += '      <div class="action_menu_items" style="opacity: 0">';
                    html_menu += '          <div class="action_item" ng-click="enroll_course()">Enroll pupil</div>';
                    html_menu += '          <div class="action_item" ng-click="edit_enroll_course()">Edit enroll</div>';
                    html_menu += '          <div class="action_item" ng-click="edit_course()">Edit lesson</div>';
                    html_menu += '      </div>';
                    html_menu += '  </div>';
                    html_menu += '</div>';
                    var e = $compile(html_menu)(scope);

                    $('body').append(e);
                    $(e).find('.content').velocity({
                        width: 300,
                        height: 238,
                        opacity: 1}, {
                            duration: 200,
                            complete: function() {
                                $(e).find('.action_menu_items').velocity({opacity: 1}, {duration: 200});
                            } });
                };


                scope.enroll_course = function($event) {
                    scope.close_action();
                    scope.enroll_courseFn($event, scope.course_id);
                };

                scope.edit_course = function($event) {
                    scope.close_action();
                    scope.edit_courseFn(scope.course_id);
                }
            }
        };
    }
];
