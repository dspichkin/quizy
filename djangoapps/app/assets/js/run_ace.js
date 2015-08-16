$(document).ready(function(){

    var editors = [];

    $('textarea').each(function(i){
        var textarea = $(this);
        var editDiv = $('<div>', {
                position: 'absolute',
                width: textarea.width(),
                height: textarea.height(),
                'class': textarea.attr('class')
            }).insertBefore(textarea);
            editDiv.attr('data_id', $(this).attr('id'));
            textarea.css('display', 'none');

        //edited Ponomarev приведение JSON к удобочитаемому виду
        var _val = textarea.val();
        //убирае escape chars
        _val = _val.replace(/\\u([\d\w]{4})/gi, function (match, grp) { return String.fromCharCode(parseInt(grp, 16)); } );
        _val = unescape(_val);
        //добавляем отступы и новые строки
        try {
            _val = JSON.stringify(JSON.parse(_val), null, '\t');
        }catch(e){

        }

        editors[i] = ace.edit(editDiv[0]);
        editors[i].getSession().setValue(_val);
        //editor.setTheme("ace/theme/monokai");
        editors[i].getSession().setMode("ace/mode/javascript");
        editors[i].getSession().on('change', function(){
            textarea.val(editors[i].getSession().getValue());
        });

    })
})
