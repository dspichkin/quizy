'use strict';

dialog.directive("controls", ["$timeout",
    function($timeout) {
        return {
            require: "^dialog",
            templateUrl: window.EXAM_SERVICE_TEMPLATES_PATH + 'modules/controls.html',
            restrict: "AE",
            link: function(scope, element, attr, api) {
                // console.log("controls", scope)
            }
        };
    }
])