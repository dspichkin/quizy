'use strict';

module.exports = ['$compile',
    function($compile) {
        return {
            restrict: "AE",
            scope: {
                action: '=action'
            },
            replace: true,
            controller: function() {},
            link: function(scope, elem, attr) {
                var dragObject = {};

                function getCoords(elem) {
                    var box = elem.getBoundingClientRect();

                    var body = document.body;
                    var docEl = document.documentElement;

                    var scrollTop = window.pageYOffset || docEl.scrollTop || body.scrollTop;
                    var scrollLeft = window.pageXOffset || docEl.scrollLeft || body.scrollLeft;

                    var clientTop = docEl.clientTop || body.clientTop || 0;
                    var clientLeft = docEl.clientLeft || body.clientLeft || 0;

                    var top = box.top + scrollTop - clientTop;
                    var left = box.left + scrollLeft - clientLeft;

                    return {
                        top: top,
                        left: left
                    };
                }

                function createAvatar(avatar) {
                    avatar.old = {
                        parent: avatar.parentNode,
                        nextSibling: avatar.nextSibling,
                        position: avatar.style.position || '',
                        left: avatar.style.left || '',
                        top: avatar.style.top || '',
                        zIndex: avatar.style.zIndex || ''
                    };

                    avatar.save_position = function() {
                        avatar.old = {
                            parent: avatar.parentNode,
                            nextSibling: avatar.nextSibling,
                            position: avatar.style.position,
                            left: avatar.style.left,
                            top: avatar.style.top,
                            zIndex: avatar.style.zIndex
                        };
                    };

                    avatar.rollback = function() {
                        var _coords_base = getCoords(avatar.old.parent);
                        var _coords_current = getCoords(avatar);

                        var interval = setInterval(function() {
                            if (_coords_current.left <= _coords_base.left ||
                                _coords_current.top <= _coords_base.top) {

                                clearInterval(interval);
                                avatar.style.position = avatar.old.position;
                                avatar.old.parent.insertBefore(avatar, avatar.old.nextSibling);
                                avatar.style.zIndex = avatar.old.zIndex;
                                avatar.style.left = _coords_base.left;
                                avatar.style.top = _coords_base.top;

                            }
                            _coords_current.left = _coords_current.left - 20;
                            _coords_current.top = _coords_current.top - 20;
                            avatar.style.left = _coords_current.left + 'px';
                            avatar.style.top = _coords_current.top + 'px';
                        }, 10);
                    };

                    return avatar;
                }

                function startDrag() {
                    var avatar = dragObject.avatar;
                    document.body.appendChild(avatar);
                    avatar.style.zIndex = 9999;
                    avatar.style.position = 'absolute';
                }


                function handleDragMove(e) {
                    if (!dragObject.elem) return;

                    if (!dragObject.avatar) {

                        dragObject.avatar = createAvatar(dragObject.elem); // захватить элемент

                        var coords = getCoords(dragObject.avatar);
                        dragObject.shiftX = dragObject.downX - coords.left;
                        dragObject.shiftY = dragObject.downY - coords.top;

                        startDrag(e);

                    }
                    dragObject.avatar.style.left = e.pageX - dragObject.shiftX + 'px';
                    dragObject.avatar.style.top = e.pageY - dragObject.shiftY + 'px';
                    return false;
                }

                function handleDragStart(e) {
                    e.preventDefault();
                    scope.answer_is_done = false;

                    if (e.which != 1) { // если клик правой кнопкой мыши
                        return; // то он не запускает перенос
                    }

                    var element = e.currentTarget;
                    element.classList.add("dad-dragable");

                    var _question_id = element.getAttribute('data-id');

                    dragObject.elem = element;
                    dragObject.question_id = _question_id;
                    // запомнить координаты, с которых начат перенос объекта
                    dragObject.downX = e.pageX;
                    dragObject.downY = e.pageY;

                    document.onmousemove = handleDragMove;
                    element.onmouseup = handleDragEnd;
                    element.ondragstart = function() {
                         return false;
                    };

                }


                function findDroppable(event) {
                    dragObject.avatar.hidden = true;
                    var elem = document.elementFromPoint(event.clientX, event.clientY);
                    // показать переносимый элемент обратно
                    dragObject.avatar.hidden = false;
                    if (elem == null) {
                        return null;
                    }
                    var _dropEl;

                    if (elem.classList.contains('dragable')) {
                        // Длеаем обмен с другим drag элементом
                        var clone = elem.cloneNode(true);
                        // console.log('clone', clone)
                        // clone.setAttribute('data-id', dragObject.question_id);

                        var _coords = getCoords(dragObject.avatar.old.parent);
                        clone.style.left = _coords.left;
                        clone.style.top = _coords.top;

                        dragObject.avatar.old.parent.appendChild(clone);
                        clone.onmousedown = handleDragStart;
                        if (scope.action) {
                            // записываем ответ для элмента который переносим
                            var _answer_id = dragObject.avatar.old.parent.getAttribute('data-id');
                            var _question_id = clone.getAttribute('data-id');
                            scope.action(_question_id, _answer_id);
                        }
                        return elem.parentNode;
                    }

                    if (elem.classList.contains('dropable')) {
                        return elem;
                    }

                    return false;
                }


                function finishDrag(e) {

                    var dropElem = findDroppable(e);
                    if (!dropElem) {
                        onDragCancel(dragObject);
                    } else {
                        onDragEnd(dragObject, dropElem);
                    }
                }


                function handleDragEnd(e, element) {
                    if (dragObject.avatar) {
                        finishDrag(e);
                    }

                    document.onmouseup = null;
                    dragObject.elem.classList.remove("dad-dragable");
                    dragObject.elem.ondragstart = function() {
                         return true;
                    };

                    dragObject = {};

                }

                function onDragEnd(dragObject, dropElem) {

                    dragObject.avatar.style.position = 'static';
                    dragObject.avatar.style.zIndex = dragObject.avatar.old.zIndex;
                    dropElem.innerHTML = "";
                    dropElem.appendChild(dragObject.avatar, dropElem.nextSibling);

                    if (scope.action) {
                        // записываем ответ
                        var answer_id = dropElem.getAttribute('data-id');
                        scope.action(dragObject.question_id, answer_id);
                    }

                };

                function onDragCancel(dragObject) {
                    dragObject.avatar.rollback();
                };

                elem[0].onmousedown = handleDragStart;

            }
        };
    }
];