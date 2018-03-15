/**
 * Created by orion on 25/11/2017.
 */
'use strict';

$(function () {
    var $uploadPath = $('.upload-album-path');
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
        var w = path.split('/');
        if (w[w.length -1].indexOf('.') !== -1) {
            w.pop();
        }
        return w.join('/');
    }
    $('.get-album-for-path').click(function(){
        var p = dirname($uploadPath.val());
        getAlbumForPath(p);
    });
    $('.upload .finder').click(function(){
        var p = dirname($uploadPath.val());
        openpath(p)
    });
    $('.upload .dirname').click(function(){
        $uploadPath.val(dirname($uploadPath.val()));
    });
    $('.upload .tag-editor').click(function() {
        var p = dirname($uploadPath.val());
        // console.log('p', p);
        ajaxPost({
            cmd: 'tageditor',
            path: p
        });
    });
    $('.upload-go').click(function(){
        function getId(val) {
            var w = val.split('_');
            return w[w.length - 1];
        }
        var componist = $('.componist .tt-input').val(),
            componistId = null,
            motherId = null;
        if (componist && componist.length) {
            componistId = getId(componist);
        }
        motherId = $('.upload .mother-id input').val();
        console.log(motherId);
        ajaxPost({
            cmd: 'upload',
            componistId: componistId,
            motherId: motherId,
            path: $('.upload-album-path').val(),
            collection: $('.upload .check-collection').is(':checked')
            // stepin: $('.upload .check-stepin').is(':checked')
        }, function(response) {

        });
    });
});