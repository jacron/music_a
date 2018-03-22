'use strict';


/**
 * Created by orion on 28/10/2017.
 */
$(function () {
    $('.input-album').keydown(function(e){
        if (e.key === 'Enter') {
            const target = $(e.target).val();
            location.href="/album/" + target;
        }
    });
    $('.delete-album').keydown(function(e){
        if (e.key === 'Enter') {
            const target = $(e.target).val();
            if (confirm('album ' + target + ' verwijderen?')){
                const data = {
                    cmd: 'delete_album',
                    albumid: target
                };
                ajaxPost(data);
            }
        }
    });
    $('.extra .add-componist').keydown(function (e) {
        if (e.key === 'Enter') {
            const $target = $('.componisten input.add');
            addNewComponist($target);
        }
    });
    $('.remove-score-fragment').click(function(){
        const code = $(this).attr('code');
        ajaxPost({
            cmd: 'remove_score_fragment',
            code: code
        }, function(){
            location.reload();
        });
    });
    $('.paste-score-fragment').click(function(){
        const code = $(this).attr('code');
        ajaxPost({
            cmd: 'paste_score_fragment',
            code: code
        }, function(){
            // window.open('http://127.0.0.1:8000/librarycode/' + code + '/None/', 'score_proof');
            location.reload();
        });
    });
    $('.favorite-librarycode').change(function(){
        const $this = $(this),
            code = $this.attr('code');
        console.log($this.is(':checked'));
        ajaxPost({
            cmd: 'toggle_code_favorite',
            code: code,
            favorite: $this.is(':checked')
        }, function(){
            // location.reload();
        });
    });
    $('.nav-play').click(function() {
        ajaxPost({
            cmd: 'controlplayer',
            mode: 'pause'  // toggle play
        }, function(){
        });
    });
});
