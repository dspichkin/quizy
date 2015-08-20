'use strict';

dialog.directive("dinput", ["$timeout", '$sce',
    function($timeout, $sce) {
        return {
            require: "^dialog",
            templateUrl: window.EXAM_SERVICE_TEMPLATES_PATH + 'modules/dinput.html',
            restrict: "AE",
            link: function(scope, element, attr, api) {
                console.log("controls", scope.model.step.variants[0].data.text)
                var _text = scope.model.step.variants[0].data.text;
                var _words = _text.split(' ');
                scope.finished = false;
                scope.inputed = "";
                scope.inputed_words = "";
                var inputed_old = null;

                var index = 0;
                var current_word = _words[index];
                

                scope.inputedWords = function() {
                    if (scope.inputed.length > current_word.length + 3) {
                        scope.inputed = inputed_old
                    } else {
                        inputed_old = scope.inputed;
                    }
                    if (scope.inputed[0].toLowerCase() == current_word[0].toLowerCase()) {
                        scope.inputed_words += current_word + '&nbsp;&nbsp;&nbsp;';
                        scope.inputed = ""
                        index += 1;

                        if (index >= _words.length) {
                            index -= 1;
                            scope.finished = true;
                            current_word = null;
                        } else {
                            current_word = _words[index];
                        }
                    }
                    if (scope.finished == true) {
                        console.log('finished', scope.model.step.variants[0].id)
                        scope.variantClick(null, scope.model.step.variants[0].id)
                    }
                }


            }
        };
    }
])