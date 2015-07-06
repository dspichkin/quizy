'use strict';

module.exports = ['$rootScope', '$compile', '$timeout',
    function($rootScope, $compile, $timeout) {
        return {
            restrict: "AE",
            scope: true,
            replace: true,
            //template: '<div ripple fab-class="fab-add-page" ng-click="show_action($event)"  icon="icon-add">' + 
            //    '<a class="icon-add" href="#"></a>' +
            //    '</div>',
            link: function(scope, elem, attr) {
                scope.show_fab = false;
                scope.show_fab_shadow = false;
                scope.show_menu = false;

                //var element = elem[0];
                var controls = [];
                for (var i = 0; i < $(elem).children('div').length; i++) {
                    var _e = $(elem).children('div')[i];
                    var _c = {
                        content: _e,
                        ng_click: $(_e).find('div').attr('ng-click')
                    }
                    controls.push(_c);
                }

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

                var fab_menu_width;
                if (attr.hasOwnProperty('menuWidth')) {
                    fab_menu_width = attr.menuWidth;
                }

                var fab_menu_height;
                if (attr.hasOwnProperty('menuHeight')) {
                    fab_menu_height = attr.menuHeight;
                }


                scope.fab_close = function($event) {
                    //$event.preventDefault();
                    $('body').find('.fab_content_menu').remove();
                };

                scope.show_action = function($event) {
                    scope.fab_close($event);

                    var rightX = attr.menuRightX;
                    var y = attr.menuY;

                    var html_action = '';
                    html_action += '<div class="fab_content_menu">';
                    html_action += '<div class="fab_shadow" ng-click="fab_close($event)"></div>';

                    html_action += '<div class="fab_menu ' + fab_class_menu + '" style="top:' + y + 'px;right:' + rightX + 'px;width:0;height:0;">';
                    html_action += '<div class="fab_menu_items" style="opacity:0;">';
                    for (var i = 0, len = controls.length; i < len; i++) {
                        html_action += '<div class="fab_menu_item" ng-click="fab_close($event)">' + $(controls[i].content).html() + '</div>';
                    }
                    html_action += '</div>';
                    html_action += '</div>';
                    html_action += '</div>';


                    var e = $compile(html_action)(scope);
                    $('.fab').append(e);

                    $(e).find('.fab_menu').velocity({
                        width: fab_menu_width,
                        height: fab_menu_height
                        }, {
                            duration: 400,
                            complete: function() {
                                $(e).find('.fab_menu_items').velocity({opacity: 1}, {duration: 200});
                            } 
                        });

                    $timeout(function() {
                        scope.show_fab = true;
                    }, 300);
                }

                var html_base = '<div class="fab">' + 
                    '<div class="fab_btn">';
                if (fab_class) {
                    html_base += '<button class="shadow fab_btn ' + fab_class + '" ripple ng-click="show_action($event)">';
                } else {
                    html_base += '<button class="shadow fab_btn" ripple ng-click="fab_open()">';
                }
                if (icon) {
                    html_base += '<a class="' + icon + '"  href="#"></a>';
                }
                html_base += '</div>';
                html_base += '</div>';

                var e = scope.elem = $compile(html_base)(scope);
                elem.replaceWith(e);

                
                
            }
        };
    }
];
