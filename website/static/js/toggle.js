/**
 * Created by orion on 12/11/2017.
 */
'use strict';

function toggleContent($this, parent, sibling) {
    const next = $this.parents(parent).siblings(sibling);
    if ($this.hasClass('fa-caret-right')) {
        $this.addClass('fa-caret-down');
        $this.removeClass('fa-caret-right');
        next.first().show();
    } else {
        $this.addClass('fa-caret-right');
        $this.removeClass('fa-caret-down');
        next.first().hide();
    }
}

function toggleContents($this, parent, sibling) {
    const next = $this.parents(parent).siblings(sibling);
    if ($this.hasClass('fa-caret-right')) {
        $this.addClass('fa-caret-down');
        $this.removeClass('fa-caret-right');
        next.show();
    } else {
        $this.addClass('fa-caret-right');
        $this.removeClass('fa-caret-down');
        next.hide();
    }
}

$(function () {
    function toggle($this) {
        const next = $this.next(),
            caret = $this.find('.fa');
        if (caret.hasClass('fa-caret-right')) {
            caret.addClass('fa-caret-down');
            caret.removeClass('fa-caret-right');
            next.show();
        } else {
            caret.addClass('fa-caret-right');
            caret.removeClass('fa-caret-down');
            next.hide();
        }
    }
    $('.toggle-content').click(function () {
        toggleContents($(this), 'div', 'table');
    });
    $('.toggle-edit').click(function () {
        toggleContent($(this), 'div', '.content.edit');
    });
    $('.toggle-cue').click(function () {
        toggleContent($(this), 'div', '.content.cue');
    });
    $('.toggle-cue-lines').click(function () {
        toggleContents($(this), 'li', '.content.cue-lines');
    });
    $('.toggle-cue-content').click(function() {
        toggleContent($(this), 'div', '.cue');
    });
    $('.toggle-cuesheets-content').click(function() {
        toggleContent($(this), 'div', '.cuesheets-content');
    });
    $('.toggle').click(function() {
        toggle($(this));
    });
});