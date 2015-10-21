'use strict';

module.exports = ['$compile',
    function($compile) {
        return {
            restrict: "AE",
            scope: {},
            replace: true,
            controller: function() {},
            link: function(scope, elem, attr) {
                //'content': $(raw_tabs[i]).children('div').html()
                var header = $(elem, this);
                var element = elem[0];
                var height = element.offsetHeight;
                var min_height = $(element).css('min-height');

                window.addEventListener("scroll", function(event) {
                    //testScroll(event)

                    if (this.scrollY > height - 40) {
                        $(element).css('position', 'fixed');
                        $(element).css('height', '40px');
                        $(element).css('min-height', 'initial');
                        $(element).css('top', '0px');
                        $(element).css('left', '0px');
                        $(element).css('width', '100%');
                    } else {
                        $(element).css('position', 'static');
                        $(element).css('min-height', min_height);
                        $(element).css('top', 'initial');
                        $(element).css('left', 'initial');
                        $(element).css('width', '100%');
                    }
                }, false);
            }
        }
    }
];
