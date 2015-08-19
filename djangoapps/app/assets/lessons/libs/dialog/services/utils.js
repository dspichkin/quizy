'use scripts'

var scriptURL = function() {
    var scripts = document.getElementsByTagName("script")
    var currentScriptPath = scripts[scripts.length - 1].src;
    return currentScriptPath.substring(0, currentScriptPath.lastIndexOf('/') + 1);
};


var TriggeredObject = {
    $on: function(eventName, handler, caller) {
        if (!this._eventHandlers) {
            this._eventHandlers = [];
        }

        if (handler == "") {
            console.error("Обработчик события строка");
        }

        if (!this._eventHandlers[eventName]) {
            this._eventHandlers[eventName] = [];
        }

        this._eventHandlers[eventName].push({
            handler: handler,
            caller: caller,
            args: [].slice.call(arguments, 3)
        });
    },
    /*
    * Прекращение подписки
    */
    $off: function(eventName, handler) {
        if (!this._eventHandlers) return;
        var handlers = this._eventHandlers[eventName];
        if (!handlers) return;
        for (var i = 0; i < handlers.length; i++) {
            if (handlers[i].handler == handler) {
                handlers.splice(i--, 1);
            }
        }
    },
    /*
     * Запуск события
     */
    $trigger: function(eventName) {
        if (!this._eventHandlers) return;
        var handlers = this._eventHandlers[eventName];
        if (handlers) {
            for (var i = 0; i < handlers.length; i++) {
                var args = handlers[i].args.concat([].slice.call(arguments, 1));
                if (handlers[i].caller) {
                    args.unshift(this);
                }
                if (typeof handlers[i].handler != 'undefined') {
                    handlers[i].handler.apply(handlers[i].caller || this, args);
                } else {
                    console.log("!!! Ошибка обработчика запуска события ", handlers[i]);
                }
            }
        }
        /**
         * вызываем функцию, позволяющую обслуживать любые события
         */
        if (eventName != true) {
            this.$trigger(true, arguments);
        }
    }
}


_.mixin({
    getParentDirectoryUrl: function(url) {
        return url.substr(0, url.lastIndexOf("/") + 1);
    },
    recoursive: function(object, criteria) {
        var readed = [];
        if (!object) return;
        return (function sub_recoursive(object) {
            if (readed.indexOf(object) != -1) {
                return;
            }
            readed.push(object);



            if (object instanceof Array) {
                for (var prop = object.length; prop--;) {
                    if (object[prop] && (object[prop].constructor == Object || object[prop].constructor == Array)) {
                        sub_recoursive(object[prop]);
                    } else {
                        var break_ = criteria(prop, object[prop], object);
                    }
                }
            } else {
                for (var prop in object) {
                    if (object[prop] && (object[prop].constructor == Object || object[prop].constructor == Array)) {
                        sub_recoursive(object[prop]);
                    } else {
                        var break_ = criteria(prop, object[prop], object);
                    }
                }
            }
        })(object);
    },

    get_inline_json: function(url, dataType, callback_success, callback_error) {
        if(window.CACHED_JSON && window.CACHED_JSON[url]){
            callback_success(window.CACHED_JSON[url]);
            return;
        }
        var inline = $("script[id='" + window.CACHED_JSON + "']");
        if (inline.length > 0) {
            var _data =
                inline[0].innerText || //all
                inline[0].textContent || //firefox
                inline[0].text; //ie8
            if(dataType == "json"){
                callback_success(JSON.parse(_data));
            }else{
                callback_success(_data);
            }

        } else {
            $.ajax({
                async: false,
                url: url,
                dataType: dataType
            }).success(function(data) {
                if(dataType == "json"){
                    var script = $("<script type='text/json' id='" + url + "'>" + JSON.stringify(data) + "</script>");
                }else{
                    var script = $("<script type='text/" + dataType + "' id='" + url + "'>" +  data + "</script>");
                }

                $("body").append(script);
                callback_success(data);
            }).fail(function(error_object) {
                //отображение ошибки
                console.error(error_object);
                callback_error(url, error_object);
            })
        }

    },

    load_json: function(value, callback_success, callback_error) {
        /**
         позволяет использовать конструкции вида


         расширить данные из файла template.json
         "@extend" : "url(data/template.json)",
         "@extend" : "url(data/template.json#settings/stages)",

         //заменить строку наданные из файла
         "stages":       "url(data/template.json#settings/stages)",

         * @param filename
         * @param callback_success
         * @param callback_error
         */

        var filename, regex_data, init_property;
        regex_data = /^([^#]*)#?(.*)$/.exec(value);

        filename = regex_data[1];
        init_property = regex_data[2];


        var _data;

        _.get_inline_json(filename,"json", function(data) {

            /*
             замена записей "url(./path/to/file)  на "../../path/to/file"
             url начинающиеся с ./ относительно родителького json файла

             url с "/" добавляется APP_STATIC_PATH
             */
            _.recoursive(data,
                function(property, value, parent) {
                    if (/^url\(.*\)$/.test(value)) {
                        var regex_data = /^url\((\.?\/)?(.*)\)$/.exec(value);
                        var url = regex_data[2];

                        if (regex_data[1] == "/") {
                            url = window.APP_STATIC_PATH + url;
                        }
                        if (regex_data[1] == "./") {
                            url = getParentDirectoryUrl(filename) + url;
                        }

                        parent[property] = _.rewritePath(url);
                    }
                }
            );

            /**
             * remove comments
             */
            _.recoursive(data,
                function(property, value, parent) {
                    /*
                    remove comments like

                    ["@comment()"]
                    "@comment": {}
                     */
                    if (/^@comment\(.*\)$/.test(value) || property == "@comment") {

                        if(parent.constructor == Array ){
                            parent.splice(property, 1);
                        }else{
                            delete parent[property];
                        }


                    } else if (/^@extend.*$/.test(property)) {
                        var data = _.load_json(value);
                        var ext_data = $.extend(true, data, parent);
                        $.extend(true, parent, ext_data);
                    } else if (/^@extend\(.*\)$/.test(value)) {
                        var _reg_data = /^@extend\((\.\/)?(.*)\)$/.exec(value);
                        var url = _reg_data[2];
                        if (_reg_data[1]) {
                            url = _.getParentDirectoryUrl(filename) + url;
                        }
                        var data = _.load_json(url);
                        parent[property] = data;

                    }

                }
            );


            _.recoursive(data,
                function(property, value, parent) {
                    if (/^@load\((.*)\)$/.test(value)) {
                        var _reg_data = /^@load\((\.?\/)?(.*)\)$/.exec(value);
                        var url = _reg_data[2];
                        if (_reg_data[1] == "/") {
                            url = window.APP_STATIC_PATH + url;
                        }
                        if (_reg_data[1] == "./") {
                            url = _.getParentDirectoryUrl(filename) + url;
                        }

                        _.get_inline_json(url,"html", function(data) {
                            parent[property] = data;
                        });

                            /*

                        $.ajax({
                            async: false,
                            url: url,
                            success: function(data) {
                                parent[property] = data;
                            }
                        });*/
                    }
                }
            );

            if (init_property) {
                var prop_arr = init_property.split("/");
                for (var i = 0; i < prop_arr.length; i++) {
                    data = data[prop_arr[i]];
                }
            }

            _data = data;
        }, callback_error);

        if (callback_success) callback_success(_data);
        return _data;
    }





});





