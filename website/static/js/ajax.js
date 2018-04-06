/**
 * Created by orion on 15/10/2017.
 */

'use strict';

function ajaxGet(data, cb) {
    const url = '/ajax/';
    const headers = {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
        type: 'GET',
        url: url,
        data: data,
        headers: headers,
        dataType: 'json'
    }).done(function(response){
        cb(response);
    }).fail(function(err) {
        cb(err.responseText);
    });
}

function ajaxPost(data, cb) {
    const url = '/ajax/';
    const headers = {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        headers: headers,
        dataType: 'json'
    }).done(function(response){
        console.log('done', response);
        if (cb) {
            cb(response);
        }
    }).fail(function(err) {
        console.log('err', err);
        if (cb) {
            cb(err);
        }
    });
}

function openfinder(objectId, kind) {
    ajaxPost({
        objectid: objectId,
        cmd: 'openfinder',
        kind: kind
    });
}

function openpath(path) {
    ajaxPost({
        cmd: 'openpath',
        path: path
    });
}

function tageditoralbum(albumId) {
    ajaxPost({
        cmd: 'tageditoralbum',
        albumid: albumId
    })
}

function openterminal(objectId, kind) {
    ajaxPost({
        objectid: objectId,
        cmd: 'openterminal',
        kind: kind
    });
}

function exportAlbums(objectId, kind) {
    ajaxPost({
        objectid: objectId,
        cmd: 'exportalbums',
        kind: kind
    });
}

function openwebsite(albumId) {
    ajaxPost({
        cmd: 'openwebsite',
        albumid: albumId
    })
}

function play(elm, idPiece) {
    // console.log('elm', elm);
    ajaxPost({
        arg: idPiece,
        cmd: 'play'
    }, function() {
        $('.played').removeClass('played');
        $(elm).addClass('played');
    });
}

function postMakeCuesheet(name, ids, cb) {
    if (!ids.length) {
        console.log('no ids for creating cuesheet');
        return;
    }
    if (!name || !name.length) {
        console.log('empty name for creating cuesheet');
        return;
    }
    // console.log(ids);
    console.log({
        cmd: 'makecuesheet',
        ids: ids,
        name: name,
        albumid: $('#album_id').val()
    });
    ajaxPost({
        cmd: 'makecuesheet',
        ids: ids,
        name: name,
        albumid: $('#album_id').val()
    }, function(response){if (cb) {cb(response);}})
}

function postRenameCuesheet(pieceId, albumId, nerwname, cb) {
    ajaxPost({
        cmd: 'renamecue',
        id: pieceId,
        newname: newname,
        albumid: albumId
    }, function(response){if (cb) {cb(response);}})
}

function refetch() {
    ajaxPost({
        albumid: $('#album_id').val(),
        cmd: 'refetch'
    }, function(){
        location.reload();
    });
}

