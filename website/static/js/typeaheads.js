/**
 * Created by orion on 12/11/2017.
 */

'use strict';

var typeaheadSettings = {
    hint: true,
    highlight: true,
    minLength: 1,
    // limit: 10,
    name: 'name'
};

var match = function (items) {
    return function findMatches(q, cb) {
        var matches, substrRegex;

        matches = [];
        substrRegex = new RegExp(q, 'i');
        $.each(items, function (i, str) {
            if (substrRegex.test(str)) {
                matches.push(str);
            }
        });
        cb(matches);
    };
};

function typeaheadPost(name, cmd) {
    ajaxPost({
        cmd: cmd,
        name: name,
        albumid: $('#album_id').val()
    }, function(result){
        location.reload();
    });
}

function impl_typeahead(items, type) {
    const $typeahead = $('.upload-controls .' + type + ' .typeahead');
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function typeAheadAlbumItems(cmdGet, nameField, $typeahead, cmdPost) {
    ajaxGet({
        cmd: cmdGet
    }, function(response){
        var items = [];
        response.forEach(function(item) {
            items.push(item[nameField]);
        });
        impl_post_typeahead(items, $typeahead, cmdPost);
    });
}

function impl_post_typeahead(items, $typeahead, cmd) {
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            typeaheadPost($(e.target).val(), cmd);
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function typeAheadUpload(cmdGet, nameField, type) {
    ajaxGet({
        cmd: cmdGet
    }, function(response){
        var items = [];
        response.forEach(function(item) {
            items.push(item[nameField] + '_' + item.ID);
        });
        impl_typeahead(items, type);
    });
}

function typeaheadAlbumComponisten($typeahead, $makeCuesheet) {
    const items = getAlbumComponisten();
    if (items.length === 1) {$typeahead.val(items[0]); }
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            copyComponist($typeahead.val(), $makeCuesheet);
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function goResult($naam, val, href, attrId) {
    $naam.each(function () {
        var $this = $(this);
        if ($this.text() === val) {
            location.href = href + $this.attr(attrId);
        }
    });
}

function quickSearch($naam, $typeahead, href, attrId) {
    var items = [];
    $naam.each(function () {
        items.push($(this).text());
    });
    $typeahead.typeahead(
        typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            goResult($naam, $typeahead.val(), href, attrId);
        }
    });
}

//https://stackoverflow.com/questions/21530063/how-do-we-set-remote-in-typeahead-js
var albums = new Bloodhound({
    datumTokenizer: function (datum) {
        return Bloodhound.tokenizers.whitespace(datum.value);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        wildcard: '%QUERY',
        url: '/ajax/?cmd=generalsearch&query=%QUERY',
        transform: function(response) {
            albumIds = [];
            return $.map(response, function(movie) {
                albumIds.push(movie.ID);
                const name = movie.name + '_' + movie.ID;
                return {name:name};
            });
        }
    }
});

var albumIds = [];

function generalSearch($typeahead) {
    function getId(s) {
        var pos = s.lastIndexOf('_');
        return s.substr(pos + 1);
    }

    $typeahead.typeahead(
        typeaheadSettings,
        {
            displayKey: 'name',
            source: albums,
            updater: function(item) {
                console.log(item);
                return item;
            }
        }).keydown(function(e) {
        if (e.key === 'Enter') {
            const id = getId($(e.target).val());
            // console.log(albumIds);
            location.href = '/album/' + id;
        }
    });
}

function searchTagsTypeahead($typeahead, cmdGet, nameField) {
    ajaxGet({
        cmd: cmdGet
    }, function(response){
        var items = [];
        response.forEach(function(item) {
            items.push(item[nameField]);
        });
        $typeahead.typeahead(typeaheadSettings,
            { source: match(items) }
        ).keydown(function(e){

        });
    });
}

$(function () {
    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        typeAheadAlbumItems('instruments', 'Name', $('.album .instrument.typeahead'), 'add_new_instrument');
        typeAheadAlbumItems('performers', 'FullName', $('.album .performer.typeahead'), 'add_new_performer');
        typeAheadAlbumItems('componisten', 'FullName', $('.album .componist.typeahead'), 'add_new_componist');
        typeAheadAlbumItems('tags', 'Name', $('.album .tag.typeahead'), 'new_tag');
    }
    quickSearch($('.performer-naam'), $('.performers .typeahead'), '/performer/', 'performerid');
    quickSearch($('.componist-naam'), $('.componisten .typeahead'), '/componist/', 'componistid');
    generalSearch($('.typeahead.general'));
    searchTagsTypeahead($('.search .tag.typeahead'), 'tags', 'Name');
    if ($('.upload-album-path').length) {
        // functions for the upload page
        typeAheadUpload('instruments', 'Name', 'instrument');
        typeAheadUpload('performers', 'FullName', 'performer');
        typeAheadUpload('componisten', 'FullName', 'componist');
        typeAheadUpload('tags', 'Name', 'tag');
    }
    $('.search-title').keydown(function(e){
        if (e.key === 'Enter') {
            location.href = '/search/' + $(this).val();
        }
    });
    $('.search-inside-componist').keydown(function(e){
        if (e.key === 'Enter') {
            location.href = '/componist/' + $('#componist_id').val() + '/search/' +
                $(this).val() + '/';
        }
    });
    $('.search-inside-collection').keydown(function(e){
        if (e.key === 'Enter') {
            location.href = '/collection/' + $(this).val() + '/search';
        }
    });
    $('.search-inside-instrument').keydown(function(e){
        if (e.key === 'Enter') {
            location.href = '/instrument/' + $('#instrument_id').val() + '/search/' + $(this).val();
        }
    });

});



