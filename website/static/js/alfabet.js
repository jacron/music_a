/**
 * Created by orion on 18/11/2017.
 */

'use strict';

$(function () {
    function jumpToSearched(search, fieldName, byVal) {
        var items = $('li.hyperlink');
        items.each(function(){
            var $li = $(this),
                title = $li.find(fieldName),
                text;
            if (byVal) {
                text = title.val().toUpperCase();
            } else {
                text = title.text().toUpperCase().trim();
            }
            if (text.indexOf(search) === 0) {
                $('html, body').animate({
                    scrollTop: $li.offset().top
                },500);
                return false;
            }
        });
    }
    $('.collections .alfabet a').click(function (e) {
        const $target = $(e.target),
            search = $target.text().trim();
        // console.log(search);
        jumpToSearched(search, '.title', false);
    });
    $('.componisten .alfabet a').click(function (e) {
        const $target = $(e.target),
            search = $target.text().trim();
        jumpToSearched(search, '.last-name', true);
    });
    $('.componist .alfabet a').click(function (e) {
        const $target = $(e.target),
            search = $target.text().trim();
        jumpToSearched(search, '.title', false);
    });
    $('.instrument .alfabet a').click(function (e) {
        const $target = $(e.target),
            search = $target.text().trim();
        jumpToSearched(search, '.title', false);
    });
    $('.performer .alfabet a').click(function (e) {
        const $target = $(e.target),
            search = $target.text().trim();
        jumpToSearched(search, '.title', false);
    });
    $('.album .alfabet a').click(function (e) {
        const $target = $(e.target),
            search = $target.text().trim();
        jumpToSearched(search, '.title', false);
    });
    $('.jump-to-letter').keydown(function(e){
        const $target = $(e.target),
            search = $target.val().toUpperCase();
        if (e.key === 'Enter') {
            jumpToSearched(search);
        }
    });
});