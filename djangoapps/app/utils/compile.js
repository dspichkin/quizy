'use strict';

module.exports = ['$compile',
    function($compile) {
        return {
            restrict: "AE",
            scope: true,
            link: function(scope, elem, attrs) {
                scope.$watch(
                    function(scope) {
                        // watch the 'compile' expression for changes
                        return scope.$eval(attrs.compile);
                    },
                    function(value) {
                        // when the 'compile' expression changes
                        // assign it into the current DOM
                        elem.html(value);

                        // compile the new DOM and link it to the current
                        // scope.
                        // NOTE: we only compile .childNodes so that
                        // we don't get into infinite loop compiling ourselves
                        $compile(elem.contents())(scope);
                    }
                );
            }
        }
    }
]