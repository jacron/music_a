/**
 * Created by orion on 15/10/2017.
 */

'use strict';

function addTag($select) {
    const data = {
        cmd: 'add_tag',
        tagid: $select.val(),
        albumid: $select.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

function newTag($input) {
    const data = {
        cmd: 'new_tag',
        name: $input.val(),
        albumid: $input.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

function removeTag($this) {
    const data = {
        cmd: 'remove_tag',
        id: $this.attr('id'),
        albumid: $('#album_id').val()
        // albumid: $this.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}


$(function () {
    // tag
    $('button.select-tag').click(function () {
        addTag($('select.select-tag'));
    });
    $('button.add-tag').click(function () {
        newTag($('input.add-tag'));
    });
    $('input.add-tag').keydown(function (e) {
        if (e.key === 'Enter') {
            newTag($('input.add-tag'));
        }
    });
    $('select.select-tag').keydown(function (e) {
        if (e.key === 'Enter') {
            addTag($('select.select-tag'));
        }
    });
   $('.tag .remove').click(function(){
       removeTag($(this));
   });
});
