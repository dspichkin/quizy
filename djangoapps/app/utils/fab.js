'use strict';

module.exports = ['$rootScope', '$compile', '$timeout',
    function($rootScope, $compile, $timeout) {
        return {
            restrict: "AE",
            scope: true,
            replace: true,
            controller: function() {
            },
            link: function(scope, elem, attr) {
                scope.show_fab = false;
                scope.show_fab_shadow = false;
                scope.show_menu = false;

                scope.fab_open = function() {
                    scope.show_menu = !scope.show_menu;
                    scope.show_fab_shadow = !scope.show_fab_shadow;
                };

                scope.fab_close = function() {
                    scope.show_fab_shadow = false;
                    scope.show_menu = false;
                };

                
                var element = elem[0];
                var height = element.offsetHeight;
                var controls = [];
                for (var i = 0; i < $(elem).children('div').length; i++) {
                    var _e = $(elem).children('div')[i];
                    var _c = {
                        content: _e,
                        ng_click: $(_e).find('div').attr('ng-click')
                    }
                    controls.push(_c);

                };

                var icon;
                if (attr.hasOwnProperty('icon')) {
                    icon = attr.icon;
                }
                var fab_class;
                if (attr.hasOwnProperty('fabClass')) {
                    fab_class = attr.fabClass;
                }

                var fab_class_menu;
                if (attr.hasOwnProperty('fabClassMenu')) {
                    fab_class_menu = attr.fabClassMenu;
                }

                var html = '';
                html += '<div class="fab">';
                html += '<div class="fab_shadow" ng-show="show_fab_shadow" ng-click="fab_close()"></div>';
                html += '<div class="fab_btn" ng-show="show_fab">';
                if (fab_class) {
                    html += '<button class="shadow fab_btn ' + fab_class + '" ripple ng-click="fab_open()">';
                } else {
                    html += '<button class="shadow fab_btn" ripple ng-click="fab_open()">';
                }

                if (icon) {
                    html += '<a class="' + icon + '"  href="#"></a>';
                }

                html += '</button>';

                if (fab_class_menu) {
                    html += '<div class="' + fab_class_menu + '" ng-show="show_menu">';
                } else {
                    html += '<div class="fab_menu" ng-show="show_menu">';
                }

                //html += '<div class="fab_menu" ng-show="show_menu">';
                for (var i = 0, len = controls.length; i < len; i++) {
                    html += '<div class="fab_menu_item" ng-click="' + controls[i].ng_click + '"">' + $(controls[i].content).html() + '</div>';
                }
                html += '</div>';
                html += '</div>';
                html += '</div>';
                var e = scope.elem = $compile(html)(scope);

                elem.replaceWith(e);

                $timeout(function() {
                    scope.show_fab = true;
                }, 300);
            }
        };
    }
];
