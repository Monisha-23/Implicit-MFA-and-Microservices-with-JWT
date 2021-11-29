var Pattern = function (options) {
    "use strict";
    this.dimension = options.dimension && options.dimension.indexOf('x') !== -1 ? options.dimension.split('x') : [3, 3];

    this.patternRadius = options.patternRadius || 20;
    this.patternGap = options.patternGap || 50;
    this.innerColor = options.innerColor || '90-#239EE0:5-#1951A0:95';
    this.outerColor = options.outerColor || '#333333';
    this.background = options.background || '#000000';
    this.backgroundOpacity = options.backgroundOpacity || 1;
    this.hoverColor = options.hoverColor || '#c8ee17';

    this.errorColor = options.errorColor || '#FF0000';

    this.padding = options.padding || this.patternRadius;

    this.onFinish = options.onFinish || null;

    this.width = this.dimension[0] * (2 * this.patternRadius + this.patternGap) + (this.padding * 4) - this.patternGap;
    this.height = this.dimension[1] * (2 * this.patternRadius + this.patternGap) + (this.padding * 4) - this.patternGap;

    this.paper = null;
    this.patternCircle = [];
    this.value = [];
    this.blocker = null;

    var patternObj = this;
    this.isMouseDown = false;
    this.lineX = 0;
    this.lineY = 0;
    this.currentPath = null;
    this.currentTarget = null;


    //styes
    this.paperStyle = {
        fill: patternObj.background,
        'stroke-width': 0,
        opacity: patternObj.backgroundOpacity
    };
    this.selectedStyle = {
        'fill': '#CCC',
        'fill-opacity': 0.3,
        'stroke-width': 3,
        'stroke': '#C8E02A'
    };
    this.innerStyle = {
        'fill': patternObj.innerColor,
        'stroke-width': 0
    };
    this.outerStyle = {
        'fill': patternObj.outerColor,
        'stroke-width': 0,
        'fill-opacity': 1
    };
    this.hoverStyle = {
        'stroke-width': 3,
        'stroke': patternObj.hoverColor,
        'stroke-opacity': 1
    };
    this.pathStyle = {
        stroke: '#FFF',
        'stroke-width': '5',
        'stroke-linecap': 'round',
        'opacity': 0.3
    };
    this.errorStyle = {
        'stroke-width': 3,
        'stroke': patternObj.errorColor,
        'stroke-opacity': 0.75
    };

    //common handlers
    var paperMouseUpHandler = function () {
        patternObj.isMouseDown = false;
        if (patternObj.currentPath) {
            patternObj.currentPath.remove();
        }
        if (patternObj.currentTarget.length && patternObj.currentTarget[0].data('connection') === 1) {
            patternObj.blocker = patternObj.paper.rect(0, 0, patternObj.width, patternObj.height, patternObj.patternRadius).attr({
                fill: '#000',
                'stroke-width': 0,
                'fill-opacity': 0
            });
        }
        patternObj.currentPath = [];
        patternObj.currentTarget = [];

        if (typeof (patternObj.onFinish)) {
            patternObj.onFinish(patternObj.val());
        }
    };

    var drawPathHandler = function (e) {
        e = e || window.event;

        var pX = e.pageX;
        var pY = e.pageY;
        if (pX === undefined) {
            pX = e.clientX;
            pY = e.clientY;
        }
        pX = pX - ((window.pageXOffset || document.body.scrollLeft) + patternObj.paper.canvas.getBoundingClientRect().left);
        pY = pY - ((window.pageYOffset || document.body.scrollTop) + patternObj.paper.canvas.getBoundingClientRect().top);

        e.stopPropagation();
        if (patternObj.isMouseDown && patternObj.currentPath) {
            patternObj.currentPath.attr('path', "M" + patternObj.lineX + " " + patternObj.lineY + "L" + pX + " " + pY);
        }
    };

    this.disableSelection = function (target) {
        if (typeof target.onselectstart != "undefined") {
            target.onselectstart = function () {
                return false;
            };
        } else if (typeof target.style.MozUserSelect != "undefined") {
            target.style.MozUserSelect = "none";
        } else {
            target.onmousedown = function () {
                return false;
            };
        }
    };

    this.createPattern = function (paperObj) {
        var x = 0,
            y = 0,
            i, j, elm = null;
        for (i = 0; i < patternObj.dimension[0]; i++) {
            x = i * (patternObj.patternGap + patternObj.patternRadius * 2) + patternObj.padding + patternObj.patternRadius;
            for (j = 0; j < patternObj.dimension[1]; j++) {
                y = j * (patternObj.patternGap + patternObj.patternRadius * 2) + patternObj.patternRadius + patternObj.padding;
                elm = patternObj.drawPatternPoint(paperObj, x, y, i, j);
                patternObj.patternCircle.push(elm);
                elm[0].data({
                    x: i,
                    y: j
                });
            }
        }
        patternObj.sort();
    };

    this.sort = function () {
        var i, j, tmpAry = [],
            elm, cnt = 1;
        for (i = 0; i < patternObj.dimension[1]; i++) {
            for (j = 0; j < patternObj.dimension[0]; j++) {
                elm = patternObj.getByXY(j, i);
                elm[0].data({
                    'value': cnt
                });
                elm[1].data({
                    'value': cnt
                });
                tmpAry.push(elm);
                cnt++;
            }
        }
        patternObj.patternCircle = tmpAry;
    };

    this.drawConnection = function (oCircle, iCircle, currentTarget) {
        patternObj.currentPath.attr('path', "M" + patternObj.lineX + " " + patternObj.lineY + "L" + (oCircle.getBBox().x + oCircle.getBBox().width / 2) + " " + (oCircle.getBBox().y + oCircle.getBBox().height / 2));
        patternObj.lineX = (oCircle.getBBox().x + oCircle.getBBox().width / 2);
        patternObj.lineY = (oCircle.getBBox().y + oCircle.getBBox().height / 2);

        patternObj.currentPath = patternObj.paper.path("M" + patternObj.lineX + " " + patternObj.lineY + "L" + patternObj.lineX - 2 + " " + patternObj.lineY - 2).attr(patternObj.pathStyle);
        patternObj.currentPath.mouseup(paperMouseUpHandler);
        currentTarget.data({
            'connection': 1
        }).attr(patternObj.selectedStyle);
        iCircle.data({
            'connection': 1
        });
        oCircle.data({
            'connection': 1
        }).attr(patternObj.selectedStyle);
        patternObj.value.push(oCircle.data('value'));
    };

    this.getByXY = function (x, y) {
        for (var i = 0; i < this.patternCircle.length; i++) {
            if (this.patternCircle[i][0].data('x') === x && this.patternCircle[i][0].data('y') === y) {
                return this.patternCircle[i];
            }
        }
        return null;
    };

    this.drawPatternPoint = function (paperObj, x, y, xi, yi) {
        var patternElm = paperObj.set();
        var oCircle = paperObj.circle(patternObj.padding + x, patternObj.padding + y, patternObj.patternRadius).attr(patternObj.outerStyle);
        var iCircle = paperObj.circle(patternObj.padding + x, patternObj.padding + y, patternObj.patternRadius / 3).attr(patternObj.innerStyle);
        iCircle.data({
            'connection': 0,
            'x': xi,
            'y': yi
        });
        oCircle.data({
            'connection': 0,
            'x': xi,
            'y': yi
        });

        patternElm.push(oCircle, iCircle);

        var patternMousemoveHandler = function () {
            oCircle.attr(patternObj.hoverStyle);

            if (patternObj.currentPath && (patternObj.currentTarget[0] !== oCircle[0] && patternObj.currentTarget[1] !== iCircle[0]) && (iCircle.data('connection') === 0)) {

                var x1 = patternObj.currentTarget[0].data('x');
                var y1 = patternObj.currentTarget[0].data('y');
                var x2 = oCircle.data('x');
                var y2 = oCircle.data('y');

                var xs = x1 > x2 ? x2 : x1;
                var xe = x1 > x2 ? x1 : x2;
                var ys = y1 > y2 ? y2 : y1;
                var ye = y1 > y2 ? y1 : y2;

                var i;
                var telm = null;
                var connect = function (a, b) {
                    telm = patternObj.getByXY(a, b);
                    if (telm[0].data('connection') === 0) {
                        patternObj.drawConnection(telm[0], telm[1], telm[0]);
                    }
                };
                if (x1 === x2 && y1 !== y2) {
                    if (y1 < y2) {
                        for (i = ys; i <= ye; i++) {
                            connect(xs, i);
                        }
                    } else {
                        for (i = ye; i >= ys; i--) {
                            connect(xs, i);
                        }
                    }
                } else if (y1 === y2 && x1 !== x2) {
                    if (x1 > x2) {
                        for (i = xe; i >= xs; i--) {
                            connect(i, ys);
                        }
                    } else {
                        for (i = xs; i <= xe; i++) {
                            connect(i, ys);
                        }
                    }
                } else if (Math.abs(x1 - x2) === Math.abs(y1 - y2)) {
                    for (i = 0; i <= Math.abs(ys - ye); i++) {
                        if (y1 < y2 && x1 > x2) {
                            connect(x1 - i, y1 + i);
                        } else if (y1 > y2 && x1 < x2) {
                            connect(x1 + i, y1 - i);
                        } else if (y1 < y2) {
                            connect(x1 + i, y1 + i);
                        } else {
                            connect(x1 - i, y1 - i);
                        }
                    }
                }
                patternObj.currentTarget.pop();
                patternObj.currentTarget = [oCircle, iCircle];
            }

        };

        var patternMouseoutHandler = function () {
            if (oCircle.data('connection') === 0) {
                oCircle.attr({
                    'stroke-width': 0
                });
            }
        };

        var patternMouseDownHandler = function () {
            patternObj.isMouseDown = true;
            patternObj.currentTarget = [oCircle, iCircle];
            patternObj.lineX = patternElm.getBBox().x + patternElm.getBBox().width / 2;
            patternObj.lineY = patternElm.getBBox().y + patternElm.getBBox().height / 2;
            patternObj.currentPath = patternObj.paper.path("M" + patternObj.lineX + " " + patternObj.lineY + "L" + patternObj.lineX - 2 + " " + patternObj.lineY - 2).attr(patternObj.pathStyle);
            patternObj.currentPath.touchend(paperMouseUpHandler);
            patternObj.currentPath.mouseup(paperMouseUpHandler);
        };

        patternElm.mousemove(patternMousemoveHandler);
        patternElm.mouseout(patternMouseoutHandler);
        patternElm.mousedown(patternMouseDownHandler);
        patternElm.mouseup(paperMouseUpHandler);
        return [oCircle, iCircle];
    };

    this.drawPaper = function (elm) {
        var paper = new Raphael(elm, patternObj.width, patternObj.height);
        var rect = paper.rect(0, 0, patternObj.width, patternObj.height, patternObj.patternRadius).attr(patternObj.paperStyle);
        rect.mousemove(drawPathHandler);
        rect.mouseup(paperMouseUpHandler);
        return paper;
    };

    this.draw = function (elm) {
        patternObj.paper = patternObj.drawPaper(elm);
        patternObj.createPattern(this.paper);
        patternObj.disableSelection(patternObj.paper.canvas);
        return this.paper;
    };

    this.clear = function () {
        var paths = patternObj.paper.canvas.getElementsByTagName('path');
        var cnt = paths.length;
        for (var i = 0; i < cnt; i++) {
            paths[0].parentNode.removeChild(paths[0]);
        }
        patternObj.paper.forEach(function (el) {
            if (el[0].tagName.toLowerCase() == 'circle') {
                el.data({
                    'connection': 0
                });
                if (patternObj.patternRadius == el.attr('r')) {
                    el.attr(patternObj.outerStyle);
                }
            }
        });
        if (patternObj.blocker) {
            patternObj.blocker.remove();
        }
        patternObj.blocker = null;
        patternObj.currentPath = null;
        patternObj.currentTarget = [];
        patternObj.value = [];
    };

    this.error = function () {
        for (var i = 0; i < patternObj.patternCircle.length; i++) {
            if (patternObj.patternCircle[i][0].data('connection') === 1) {
                patternObj.patternCircle[i][0].attr(patternObj.errorStyle);
            }
        }
    };

    this.val = function () {
        return patternObj.value.toString().replace(/,/g, '-');
    };
};