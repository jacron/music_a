/**
 * Created by orion on 18/11/2017.
 */

'use strict';

$(function () {
    function preventSpilledDrop(obj) {
        obj.on('dragenter', function (e) {
            e.stopPropagation();
            e.preventDefault();
        });
        obj.on('dragover', function (e) {
            e.stopPropagation();
            e.preventDefault();
            obj.css('border', '2px dotted #0B85A1');
        });
        obj.on('drop', function (e) {
            e.stopPropagation();
            e.preventDefault();
        });
    }
    function uploadFile(fd, obj) {
        const url = '/ajax/';
        const headers = {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        };
        $.ajax({
            url: url,
            data: fd,
            type: 'POST',
            contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
            processData: false, // NEEDED, DON'T OMIT THIS
            headers: headers,
            success: function(msg){
                console.log(msg);
                obj.css('border', 'none');
                location.reload();
            },
            failure: function(msg){
                console.log(msg);
                obj.css('border', 'none');
            }
        });
    }
    function handleFileUpload(files, obj, personId, fieldName) {
        // user has dropped one or more files
        for (var i = 0; i < files.length; i++) {
            const file = files[i];
            console.log(file);
            var fd = new FormData();
            fd.append('file', file);
            fd.append('cmd', 'upload');
            fd.append(fieldName, personId);
            uploadFile(fd, obj);
        }
    }
    function handleDroppedUrl(url, obj, personId, fieldName, type) {
        // user dropped a url (image from browser)
        var cmd = type === 'person'? 'url':'years';
        const data = {
            cmd: cmd,
            url: url
        };
        data[fieldName] = personId;
        ajaxPost(data, function() {
            obj.css('border', 'none');
            location.reload();
        });
    }
    function prepareDrop(obj) {
        obj.on('dragenter', function (e) {
            e.stopPropagation();
            e.preventDefault();
            $(this).css('border', '2px solid #0B85A1');
        });
        obj.on('dragover', function (e) {
            e.stopPropagation();
            e.preventDefault();
        });
    }
    function handleDrop(obj, personId, fieldName, type) {
        prepareDrop(obj);
        obj.on('drop', function (e) {
            $(this).css('border', '2px dotted #0B85A1');
            e.preventDefault();
            const dt = e.originalEvent.dataTransfer;
            const files = dt.files;
            console.log('dt', dt);
            if (files.length) {
                if (type === 'person') {
                    handleFileUpload(files, obj, personId, fieldName);
                }
            } else {
                var url = dt.getData('url');
                console.log('url', url);
                if (!url) {
                    url = dt.getData('text/plain');
                    console.log('text', url);
                }
                handleDroppedUrl(url, obj, personId, fieldName, type);
            }
        });
    }
    function handleAlbumDrop(obj) {
        prepareDrop(obj);
        obj.on('drop', function (e) {
        });
    }

    const componist_id = $('#componist_id').val();
    if (componist_id) {
        handleDrop($('#drop-area-componist'), componist_id, 'componist_id', 'person');
        preventSpilledDrop($('.componist'));
    }
    const performer_id = $('#performer_id').val();
    if (performer_id) {
        handleDrop($('#drop-area-performer'), performer_id, 'performer_id', 'person');
        preventSpilledDrop($('.performer'));
    }
    const dropAlbum = $('#drop-album');
    if (dropAlbum.length) {
        handleAlbumDrop(dropAlbum);
    }
});
