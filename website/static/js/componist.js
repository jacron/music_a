/**
 * Created by orion on 15/10/2017.
 */

'use strict';

function addComponist0(componistId, albumId) {
    const data = {
        cmd: 'add_componist',
        componistid: componistId,
        albumid: albumId
    };
    ajaxPost(data);
    location.reload();
}

function addComponist($select) {
    addComponist0($select.val(), $select.attr('albumid'));
}

function addComponist2($target) {
    addComponist0($target.attr('id'), $('#album_id').val());
}

function newComponist($input, cb) {
    const data = {
        cmd: 'new_componist',
        name: $input.val(),
        albumid: $input.attr('albumid')
    };
    ajaxPost(data, function(response) {
        if (cb) { cb(response); }
    });
}

function addNewComponist($input) {
    const data = {
        cmd: 'abs_new_componist',
        name: $input.val()
    };
    ajaxPost(data, function (id) {
        console.log(id);
        $('.componist-added').text(id);
    });
    // location.reload();
}

function removeComponist($this) {
    const data = {
        cmd: 'remove_componist',
        id: $this.attr('id'),
        albumid: $('#album_id').val()
    };
    ajaxPost(data);
    location.reload();
}

function editComponistName($this, componist_id) {
    const data = {
        cmd: 'update_componist_name',
        name: $this.text().trim(),
        id: componist_id
    };
    ajaxPost(data);
}

function editPersonYears($this, cmd, person_id) {
    const data = {
        cmd: cmd,
        years: $this.val().trim(),
        id: person_id
    };
    ajaxPost(data);
}

function saveInputYears($input, cmd, person_id) {
    $input
        .focus(function(){$(this).select()})
        .mouseup(function(e){e.preventDefault()})
        .keydown(function(e) {
        if (e.key === 'Tab' || e.key === 'Enter') {
            editPersonYears($(this), cmd, person_id);
        }
    });
}

function pastePerson($this) {
    var id = $this.attr('id'),
        type = $this.attr('type');
    // console.log(id, type);
    ajaxPost({
        cmd: 'paste_person',
        id: id,
        type: type
    }, function(){
        location.reload();
    });
}

$(function () {
    // componist
    $('button.select-componist').click(function () {
        addComponist($('select.select-componist'));
    });
    $('button.add-componist').click(function () {
        newComponist($('input.add-componist'), function() {
            location.reload();
        });
    });
    $('input.add-componist-extra').keydown(function (e) {
        if (e.key === 'Enter') {
            var $input = $('input.add-componist-extra');
            newComponist($input, function(response) {
                $('.componist-extra-added').text($input.val());
                $input.val();
            });
        }
    });
    $('select.select-componist').keydown(function (e) {
        if (e.key === 'Enter') {
            addComponist($('select.select-componist'));
        }
    });
    $('.add-componist').click(function (e) {
        addComponist2($(e.target));
    });

    $('.componist-period').keydown(function (e) {
        if (e.key === 'Enter') {
            const $target = $(e.target);
            location.href = '/componist/' + $target.val() + '/period/';
        }
    });
    $('.componist .remove').click(function () {
        removeComponist($(this));
    });
    $('.paste-person').click(function(){
        pastePerson($(this));
    });
    const componist_id = $('#componist_id').val();
    if (componist_id) {
        $('.edit-componist-name').keydown(function (e) {
            if (e.key === 'Tab') {
                editComponistName($(this), componist_id);
            }
        });
        saveInputYears($('.edit-componist-birth'), 'update_componist_birth', componist_id);
        saveInputYears($('.edit-componist-death'), 'update_componist_death', componist_id);
    }
});

