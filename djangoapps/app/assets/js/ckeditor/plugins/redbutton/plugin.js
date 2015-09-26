CKEDITOR.plugins.add('redbutton', {
    requires: 'panelbutton,floatpanel',
    // jscs:disable maximumLineLength
    //lang: 'en', // %REMOVE_LINE_CORE%
    // jscs:enable maximumLineLength
    icons: 'bgcolor,redbutton', // %REMOVE_LINE_CORE%
    hidpi: true, // %REMOVE_LINE_CORE%
    init: function(editor) {
        var config = editor.config;
            //lang = editor.lang.colorbutton;

        if (!CKEDITOR.env.hc) {
            addButton('RedButton', 'fore', 'Red Button', 10);
            //addButton( 'BGColor', 'back', lang.bgColorTitle, 20 );
        }
        //editor.addCommand( 'abbr', new CKEDITOR.dialogCommand( 'abbrDialog' ));
        editor.addCommand('abbr', {
            exec: function(editor) {
                var config = editor.config;
                var type = 'fore';
                var color = '#FF0000';

                // Clean up any conflicting style within the range.
                editor.removeStyle(new CKEDITOR.style(config['colorButton_' + type + 'Style'], {
                    color: 'inherit'
                }));
                var colorStyle = config['colorButton_' + type + 'Style'];
                colorStyle.childRule = type == 'back' ? function(element) {
                    // It's better to apply background color as the innermost style. (#3599)
                    // Except for "unstylable elements". (#6103)
                    return isUnstylable(element);
                } : function(element) {
                    // Fore color style must be applied inside links instead of around it. (#4772,#6908)
                    return !(element.is('a') || element.getElementsByTag('a').count()) || isUnstylable(element);
                };
                editor.applyStyle(new CKEDITOR.style(colorStyle, {
                    color: color
                }));

            }
        });


        function addButton(name, type, title, order) {
            var style = new CKEDITOR.style(config['colorButton_' + type + 'Style']),
                colorBoxId = CKEDITOR.tools.getNextId() + '_colorBox';

            editor.ui.addButton(name, {
                label: 'Set red color',
                command: 'abbr',
                toolbar: 'insert'
            });
        }

    }
});
