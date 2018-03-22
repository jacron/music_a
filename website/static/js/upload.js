/**
 * Created by orion on 25/11/2017.
 */
'use strict';

$(function () {
    const $uploadPath = $('.upload-album-path');
    function getAlbumForPath(path) {
       ajaxGet({
           cmd: 'album_by_path',
           path: path
       }, function(response) {
           console.log(response);
           if (response.Title) {
               $('.upload-album .title').text(response.Title);
               $('.upload-album a').attr('href', '/album/' + response.ID);
           }
       });
    }
    function dirname(path) {
        const w = path.split('/');
        if (w[w.length -1].indexOf('.') !== -1) {
            w.pop();
        }
        return w.join('/');
    }
    $('.get-album-for-path').click(function(){
        getAlbumForPath($uploadPath.val());
    });
    $('.upload .finder').click(function(){
        openpath(dirname($uploadPath.val()))
    });
    $('.upload .dirname').click(function(){
        $uploadPath.val(dirname($uploadPath.val()));
        getAlbumForPath($uploadPath.val());
    });
    $('.upload .tag-editor').click(function() {
        ajaxPost({
            cmd: 'tageditor',
            path: dirname($uploadPath.val())
        });
    });
    $('.upload-go').click(function(){
        function getId(val) {
            const w = val.split('_');
            return w[w.length - 1];
        }
        let componist = $('.componist .tt-input').val(),
            componistId = null;
        if (componist && componist.length) {
            componistId = getId(componist);
        }
        const motherId = $('.upload .mother-id input').val();
        console.log(motherId);
        ajaxPost({
            cmd: 'upload',
            componistId: componistId,
            motherId: motherId,
            path: $('.upload-album-path').val(),
            collection: $('.upload .check-collection').is(':checked')
        }, function(response) {

        });
    });
});