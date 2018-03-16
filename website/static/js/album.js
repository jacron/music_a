/**
 * Created by orion on 22/10/2017.
 */
'use strict';


$(function () {
    function getTitle($this) {
        const parent = $this.parents('.cue-header').find('span').first();
        return parent.text();
    }
    function editAlbumTitle($this, albumId) {
        ajaxPost({
            cmd: 'update_album_title',
            title: $this.text().trim(),
            albumid: albumId
        })
    }
    function editAlbumDescription($this, albumId) {
        ajaxPost({
            cmd: 'update_album_description',
            description: $this.text().trim(),
            albumid: albumId
        })
    }
    function copyTitle($this, albumId) {
        const title = getTitle($this),
            $title = $('.edit-title');

        if (confirm('Use this title for the album? ' + title)) {
            $title.text(title);
            ajaxPost({
                cmd: 'update_album_title',
                title: title,
                albumid: albumId
            });
        }
    }
    function copyCueTitle($this) {
        const title = getTitle($this);
        $('.make-cuesheet').val(title);
    }
    function editCuesheet($this, albumid) {
        ajaxPost({
            cmd: 'editcuesheet',
            id: $this.attr('id'),
            albumid: albumid
        })
    }
    function splitOneCueAlbum(albumid) {
        $('#album-logger').show();
        ajaxPost({
            cmd: 'split_one_cue_album',
            albumid: albumid
        })
    }
    function reloadPieces(albumid) {
        ajaxPost({
            cmd: 'refetch',
            albumid: albumid
        })
    }
    function deleteApe(albumid) {
        $('#logger').show();
        ajaxPost({
            cmd: 'delete_ape',
            albumid: albumid
        })
    }
    function splitCuedFile($this, albumid) {
        $('.cuesheetslist-logger').show();
        ajaxPost({
            cmd: 'split_cued_file',
            cue_id: $this.attr('id'),
            albumid: albumid
        }, function(response) {
           // console.log(response)
        });
    }
    function cycleSizes($this) {
        if ($this.hasClass('expanded')) {
            $this.removeClass('expanded');
            $this.addClass('super');
        }
        else if ($this.hasClass('super')) {
            $this.removeClass('super');
        }
        else {
            $this.addClass('expanded');
        }
    }
    function combineCuesheets(albumId) {
        ajaxPost({
            cmd: 'combinesubs',
            albumid: albumId
        }, function() {
            refetch();
        });
    }
    function makeSubs(albumId) {
        ajaxPost({
            cmd: 'makesubs',
            albumid: albumId
        }, function() {
            refetch();
        });
    }
    function normCuesheet($this, albumid) {
        ajaxPost({
            cmd: 'normcuesheet',
            albumid: albumid,
            id: $this.attr('id')
        }, function()  {
            refetch();
        });
    }
    function removeCuesheet($this, albumid) {
        const title = $this.attr('title');
        if (!confirm("cuesheet '" + title + "' verwijderen?")){
            return;
        }
        ajaxPost({
            cmd: 'removecuesheet',
            albumid: albumid,
            id: $this.attr('id')
        }, function(){
            refetch();
        });
    }
    function renameCuesheet($this, albumid) {
        const title = $this.attr('title');
        const answer = prompt('hernoemen?', title);
        if (!answer) {
            return;
        }
        ajaxPost({
            cmd: 'renamecuesheet',
            albumid: albumid,
            id: $this.attr('id'),
            newname: answer
        }, function(){
            refetch();
        });
    }
    function removeAlbum(albumId, idText) {
        if (confirm('Album ' + albumId + ' verwijderen?')) {
            ajaxPost({
                cmd: 'delete_album',
                album_id: albumId
            }, function() {
                idText.hide();
            });
        }
    }
    function adjustKk(album_id, $this) {
        ajaxPost({
            cmd: 'adjust_kk',
            albumid: album_id
        }, function(){
            $this.hide();
        });
    }
    function inheritElements(albumId) {
        ajaxPost({
            cmd: 'inherit_elements',
            albumid: albumId
        }, function(response) {

        });
    }
    function readAlbums(albumId) {
        ajaxPost({
            cmd: 'read_albums',
            albumid: albumId
        }, function(){
            location.reload();
        })
    }
    function filterAlbums($input) {
        const search = $input.val().toLowerCase();
        $('.album-list li').each(function() {
            const li = $(this),
                title = li.find('.title'),
                text = title.text().toLowerCase();
            if (!search.length || text.indexOf($input.val()) !== -1) {
                li.show();
            } else {
                li.hide();
            }
        });
    }

    function applyClass(cb, classActive, containerClass) {
        const container = $(containerClass);
        if ($(cb).is(':checked')) {
            container.addClass(classActive)
        } else {
            container.removeClass(classActive);
        }
    }

    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        $('.edit-title').keydown(function (e) {
            if (e.key === 'Tab') {
                editAlbumTitle($(this), albumId);
            }
        });
        $('.edit-description').keydown(function(e){
            if (e.key === 'Tab') {
                editAlbumDescription($(this), albumId);
            }
        });
        $('.refetch').click(function(){
            // if (confirm("De stukken opniew ophalen?"))
            {
                refetch();
            }
        });
        $('.album-image').dblclick(function () {
            cycleSizes($(this));
        });
        $('.cue-plus').click(function () {
            copyTitle($(this), albumId);
        });
        $('.cue-title').click(function() {
            copyCueTitle($(this));
        });
        $('.cue-split').click(function() {
            splitCuedFile($(this), albumId);
        });
        $('.cue-edit').click(function() {
            editCuesheet($(this), albumId);
        });
        $('.cue-norm').click(function() {
            normCuesheet($(this), albumId);
        });
        $('.cue-remove').click(function(){
            removeCuesheet($(this), albumId);
        });
        $('.cue-rename').click(function () {
            renameCuesheet($(this), albumId);
        });
        $('.make-subs').click(function() {
            makeSubs(albumId);
        });
        $('.combine-subs').click(function() {
            combineCuesheets(albumId);
        });
        $('.album .ID .remove').click(function() {
            removeAlbum(albumId, $('.album .ID'));
        });
        $('.kk').click(function() {
            adjustKk(albumId, $(this));
        });
        $('.inherit-elements').click(function(){
            inheritElements(albumId);
        });
        $('.read_albums').click(function(){
            readAlbums(albumId);
        });
        $('.album-image.folder').click(function() {
            $('.album-image.back').toggle();
        });
        $('.toggle-show-proposals').change(function(){
            ajaxPost({
                'cmd': 'proposals'
            }, function(){
                location.reload();
            });
        });
        $('.edit-stukken').change(function(){
            applyClass(this, 'editable', '.stukken-container');
        });
        $('.edit-stukken-codes').change(function() {
            applyClass(this, 'codable', '.stukken-container');
        });
        $('.edit-stukken-tags').change(function() {
            applyClass(this, 'active', '.tag-values');
        });
        $('.edit-stukken-tag-title').change(function() {
            applyClass(this, 'active', '.tag-title');
        });
        $('.stukken-remove-title-tag').click(function() {
            ajaxPost({
                cmd: 'remove_tag_titles',
                albumid: albumId
            })
        });
        $('.edit-cuesheet-codes').change(function() {
            applyClass(this, 'codable', '.cuesheets-content');
        });
        $('.title-to-tag').click(function(){
            ajaxPost({
                cmd: 'title2tag',
                albumid: albumId,
                mode: 'short'
            })
        });
        $('.all-to-tag').click(function(){
            ajaxPost({
                cmd: 'title2tag',
                albumid: albumId,
                mode: 'long'
            })
        });

    }
    $('.cue-split-id').click(function() {
        const albumId = $(this).attr('id');
        splitOneCueAlbum(albumId);
    });
    $('.reload-pieces').click(function() {
        const albumId = $(this).attr('id');
        reloadPieces(albumId);
    });
    $('.cue-del-ape').click(function() {
        const albumId = $(this).attr('id');
        deleteApe(albumId);
    });

    // albumlist also lives on componist page etc
    $('.filter-albums').keydown(function(e){
        if (e.key === 'Enter') {
            filterAlbums($(this));
        }
    });
    $('.open-finder').keydown(function(e){
        if (e.key === 'Enter') {
            openfinder($(this).val(), 'album');
        }
    });

});

