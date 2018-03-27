'use strict';

$(function () {
    let lazy;

    setLazy();
    lazyLoad();
    $(window).scroll(function(){
       lazyLoad();
    });
    $(window).resize(function(){
        lazyLoad();
    });
    function setLazy() {
        lazy = $('.lazy');
        // console.log('Found ' + lazy.length + ' lazy images');
    }
    function lazyLoad() {
        for (let i = 0; i < lazy.length; i++) {
            if (isInViewport(lazy[i])) {
                if (lazy[i].getAttribute('data-src')) {
                    // lazy[i].error(function(){
                    //     $(this).hide();
                    // });
                    lazy[i].src = lazy[i].getAttribute('data-src');
                    lazy[i].removeAttribute('data-src');
                }
            }
        }
        cleanLazy();
    }
    function cleanLazy() {
        lazy = Array.prototype.filter.call(lazy, function (l) {
            return l.getAttribute('data-src');
        });
    }
    function isInViewport(el) {
        const rect = el.getBoundingClientRect();

        return (
            rect.bottom >= 0 &&
            rect.right >= 0 &&
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.left <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

});