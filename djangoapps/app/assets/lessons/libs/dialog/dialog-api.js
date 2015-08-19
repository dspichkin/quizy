'use script';

function DialogApi(quiz) {

    var data = $.extend(true, {}, quiz);
    var _base = data.base || {};

    _.each(data.steps, function(_step) {
        $.extend(_step, $.extend(true, {}, _base, _step));
    });



    this.quiz = data;

}

$.extend(DialogApi.prototype, {

    init: function(callback) {
        //console.log('run init in api', this);
        $.extend(this, {
            /**
             * порядковый номер вопроса
             */
            settings: this.quiz.settings,
            step_index: 0,
            first_step: this.quiz.first_step,
            next_reflexy: null,
            steps: this.quiz["steps"],
            // этапы прохождения диалога
            parts: [],
            status: this.quiz.status,
            current_step: null,
            number_of_steps: this.quiz.steps_count || this.quiz["steps"].length,
            points: 0,
            status: 'init'
        })

        var _settings = $.extend(true, {},this.settings);
        callback({settings: _settings});

    },
    _get_reflexy: function(reflexy_id) {
        for (var i = 0; i < this.quiz.reflexy.length; i++) {
            if (this.quiz.reflexy[i].id == reflexy_id) {
                return this.quiz.reflexy[i];
            }
        }
    },
    /*
    Переход к следующему шагу и формируем данные для модели
     */
    nextStep: function(callback) {
        this.status = 'next';
        var finish;
        this.step_index++;

        //данные из предыдущего вопроса
        if (this.current_step) {
            if (this.current_step.hasOwnProperty('next_step')) {
                this.next_step_id = this.current_step.next_step;
            }
            if (this.current_step.hasOwnProperty('next_reflexy')) {
                this.next_reflexy_id = this.current_step.next_reflexy;
            }
        }
        if (this.next_reflexy_id) {
            finish = true;
        }
        var _next = this.next_step_id || this.first_step;
        if (!finish && _next != 'finish') {
            this._step_prototype = _.find(this.steps, function(_q) {
                return _q.id == _next;
            });
        }

        if (finish) {
            //если вопросов больше нет, вывод рефлексии
            this.current_step = null;
            this.status = 'finish';
            var data = {
                status: 'finish',
                step: null,
                points: this.points,
                number_of_steps: this.number_of_steps,
                step_index: this.step_index
            };
            if (this.next_reflexy_id) {
                data['reflexy'] = this._get_reflexy(this.next_reflexy_id);
            }
            callback(data);
        } else {

            //внутренние данные
            this.current_step = $.extend(true, {
                    variants: [],
                    points: 1,
                    attempt: 1,
                    data: {}
                }, this._step_prototype);


            // данный для возврата в модель
            var data = {
                step: {
                    answers: [],
                    variants_status: 'init',
                    variants: _.map(this.current_step.variants, function(_variant) {
                        return _.pick(_variant,
                            "id",
                            "data",
                            "reflexy"
                        );
                    }),
                    data: this.current_step.data
                },
                points: this.points,
                number_of_steps: this.number_of_steps,
                step_index: this.step_index
            };
            if (this.current_step.type) {
                data.step['type'] = this.current_step.type;
            }
            if (callback) {
                callback(data);
            }
        }


    },

    /**
     * Сохранить результат и получить рефлексию
     * формируем parts = []
     */
    postAnswer: function(data, callback) {
        // считаем текущий результат
        var _result = $.extend({
            points: this.points,
            status: this.status
        }, data);

        //console.log('postAnswer', _result)

        this.next_step_id = _result.reflexy.next_step;
        this.parts.push(_result);

        // callback для обновления модели
        callback(_result);
    }

});
