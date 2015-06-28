'use strict';

module.exports = ['$compile',
    function($compile) {
        return {
            restrict: "AE",
            scope: {},
            replace: true,
            controller: function() {},
            link: function(scope, elem, attr) {
                var element = elem[0];
                var height = element.offsetHeight;

                var raw_tabs = $(elem).children('div');
                scope.selectedElement = 0;
                scope.tabs = [];
                for (var i = 0, len = raw_tabs.length; i < len; i++) {
                    scope.tabs.push({
                        'label': $(raw_tabs[i]).attr('label'),
                        'content': $(raw_tabs[i]).attr('content-include')
                    })
                }
                scope.isActive = function($index) {
                    if (scope.selectedElement == $index) {
                        return true;
                    }
                }
                scope.selectTab = function($index) {
                    if ($index != scope.selectedElement) {
                        scope.selectedElement = $index;
                    }
                }
                
                var html = '';
                html += '<div class="tabs" style="position:relative">';
                html += '<div class="tabs-canvas">';
                html += '   <div class="tabs-wrapper" style="transform: translate3d(0px, 0px, 0px);">';
                html += '       <div class="tab-item" ripple ng-repeat="item in tabs" ng-click="selectTab($index)" ng-class="{\'tab-active\': isActive($index)}">';
                html += '           <span class="tab-label">{{item.label}}</span>';
                html += '       </div>';
                html += '   </div>';
                html += '</div>';
                html += '<div class="content-wrapper">';
                html += '  <div class="tabs-content" ng-include="tabs[selectedElement].content">';
                html += '</div>';
                html += '</div>';
                var e = $compile(html)(scope);
                
                elem.replaceWith(e);
                
        
            }
        }
    }
];
