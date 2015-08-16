'use strict';
/*
Использование <div dynamic-ctrl="controller"></div>
 */
module.exports = ['$compile', '$parse',
    function($compile, $parse) {
        return {
            restrict: "AE",
            terminal: true,
            priority: 100000,
            scope: true,
            link: function(scope, elem, attrs) {
                var name = $parse(elem.attr('dynamic-ctrl'))(scope);
                elem.removeAttr('dynamic-ctrl');
                elem.attr('ng-controller', name);
                $compile(elem)(scope);
            }
        };
    }
];