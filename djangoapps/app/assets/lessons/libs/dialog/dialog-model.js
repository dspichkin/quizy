'use strict';

function DialogModel(DialogApi, callbacks, apply) {
    var self = this;

    if (!callbacks) callbacks = {};
    $.extend(self, {
        api: DialogApi,
        status: 'next',
        settings: {},
        apply: apply
    });

    this.callbacks = {
        onInit: 
            callbacks.onInit || function(currtiime) {},
        onStart:
            callbacks.onStart || function(data) {},
        // Колбэк на именение модели
        onUpdateModel:
            callbacks.onUpdate || function(data) {},
        // Колбэк на переход к следующему вопросу
        onNextStep:
            callbacks.onNextStep || function(data) {},
        onSetAnswer:
            callbacks.onSetAnswer || function(variant_id) {},
        // Колбэк на возврат рефлексии
        onReflexy:
            callbacks.onReflexy || function(data) {},
    }
}



$.extend(DialogModel.prototype, {
    init: function() {
        var self = this;

        self.api.init(function(data) {
            self.settings = data.settings;
            self.callbacks.onInit(data);
        });
    },
    start: function(callback) {
        var self = this;
        //self.api.start(function(data) {
            self.next();
            self._show_step(callback);
        //});
    },
    getExamTemplate: function(tpl) {
        if (tpl) {
            if (tpl.indexOf(".html") == -1) {
                return window.EXAM_SERVICE_TEMPLATES_PATH + tpl + ".html";
            } else {
                return tpl;
            }
        } else {
            return this.settings.template;
        }
    },

    _get_variant: function(id, step) {
        if (step == undefined) step = this.step;
        return _.find(step.variants, function(_answer) {
            return _answer.id == id;
        });
    },

    _process_answer: function(_variant_id, callback) {
        var self = this;
        var _v = this._get_variant(_variant_id);
        // записываем ответ в текущий вопрос
        self.step.answers.push(_v);

        // если есть ауди то воспроизвдим его
        if (_v.data && _v.data.audio && _v.data.audio.loaded == true) {
            var _ended = function(timeout) {
                var _timeout = 2000;
                if (timeout != undefined) {
                    _timeout = timeout;
                }

                // задержка для перехода между репликой варианта и следующим вопросом
                setTimeout(function() {
                    callback();
                }, _timeout);
            };
            _v.data.audio.handled_ended = _ended;
            _v.data.audio.addEventListener("ended", function() {
                _ended();
            }, false);
            self.step.variants_status = 'playing';
            _v.data.audio.play();
        } else {
            callback();
        }
    },

    /*
        Обработка ответа пользователя
     */
    setAnswer: function(_variant_id, callback) {
        var self = this;
        self.stop_media();
        self._process_answer(_variant_id, function() {
            self.post(callback);
            if (self.status == 'next') {
                self._show_step();
            }
        });
    },
    /*
        Переход к следующему шагу
     */
    next: function(callback) {
        //console.log('next step');
        var self = this;
        self.api.nextStep(function(data) {
            // после перехода на следующий шаг
            // обновляем содержимое модели
            $.extend(self, data);
            setTimeout(function() {
                self.apply();
            });
            // callback для возврата в директиву
            if (callback) {
                callback(self);
            }

        });
    },
    /*
     Метод обработки данных полученных от пользователя
     */
    post: function(callback) {
        var self = this;
        var _current_answer = this.step.answers[0];

        var _data = {
            variant_id: _current_answer.id,
            data: _current_answer.data,
            reflexy: _current_answer.reflexy
        };
        // обрабатываем сделаный ответ
        self.api.postAnswer(_data, function(data) {
            self.next(callback);
        });
    },
    _show_step: function(callback) {
        var self = this;
        self.loadMediaResources(self.step, function() {
            self.step.step_status = 'loading';
            self.step.variants_status = 'loading';
            setTimeout(function() {
                self.apply();
            });
        }, function() {
            self.step.step_status = 'ready';
            self.step.variants_status = 'ready';
            setTimeout(function() {
                self.apply();
            });
            // callback для запуска процесов после завершения загрузки
            if (callback) callback();

            if (self.step.data && self.step.data.audio) {
                self.step.data.audio.play();
            }

        });
    },
    loadMediaResources: function(data, start, end) {
        start();
        // считаем кол-во медиа файлов
        var _total_media = 0;

        if (data.data && data.data.audiofile) {
            _total_media += 1;
            this.loadAudioFile(data.data);
        }

        for (var i = 0; i < data.variants.length; i++) {
            if (data.variants[i].data && data.variants[i].data.audiofile) {
                _total_media += 1;
                this.loadAudioFile(data.variants[i].data);
            }
        }

        // проверяем загруженность медиа объектов
        var _check_loaded = setInterval(function() {
            var _current_loaded_media = 0;
            if (data.data && data.data.audiofile) {
                if (data.data.audio.loaded && data.data.audio.loaded == true) {
                    _current_loaded_media += 1;
                }
            }
            for (var i = 0; i < data.variants.length; i++) {
                if (data.variants[i].data && data.variants[i].data.audiofile) {
                    if (data.variants[i].data.audio && data.variants[i].data.audio.loaded && data.variants[i].data.audio.loaded == true) {
                        _current_loaded_media += 1;
                    }
                }
            }
            if (_current_loaded_media == _total_media) {
                clearInterval(_check_loaded);
                end();
            }
        }, 50);


    },
    loadAudioFile: function(data) {
        data.audio = document.createElement("AUDIO");
        data.audio.src = data.audiofile;
        data.audio.onerror = function() {
            console.log("аудио файл не загружен " + data.audio.src);
        };
        data.audio.addEventListener('canplaythrough', function() {
            data.audio.loaded = true;
        }, false);
        data.audio.load();
    },
    /*
    Останавливаем воспроизведение всех медиа
     */
    stop_media: function() {
        var _data = this.step;
        if (_data.data && _data.data.audiofile) {
            if (_data.data.audio) {
                _data.data.audio.pause();
                _data.data.audio.currentTime = 0;
                if (_data.data.audio.hasOwnProperty('handled_ended')) {
                        _data.variants[i].data.audio.handled_ended(0);
                    }
            }
        }
        for (var i = 0; i < _data.variants.length; i++) {
            if (_data.variants[i].data && _data.variants[i].data.audiofile) {
                if (_data.variants[i].data.audio && _data.variants[i].data.audio.paused == false) {
                    _data.variants[i].data.audio.pause();
                    _data.variants[i].data.audio.currentTime = 0;
                    if (_data.variants[i].data.audio.hasOwnProperty('handled_ended')) {
                        _data.variants[i].data.audio.handled_ended(0);
                    }
                }
            }
        }
    }
});

