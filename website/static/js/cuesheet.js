/**
 * Created by orion on 08/10/2017.
 */
'use strict';

function isMusicFile(s) {
    const exts = ['flac', 'mp3'];
    for (var i = 0; i < exts.length; i++) {
        if (s === exts[i]) {
            return true;
        }
    }
    return false;
}

function titleOfPiece($val) {
    var parent = $val.parents('.hyperlink').first(),
        title = parent.find('.title').first().text();

    var w = title.split('.');
    if (isMusicFile(w[w.length - 1])){
        w.pop();
        title = w.join('.');
    }

    var s = title.split(' ');
    if ($.isNumeric(s[0])) {
        s.splice(0, 1);
        title = s.join(' ');
    }

    return title;
}

function getSelectedCuesheetIds($selectForCuesheet, $makeCuesheet) {
    var active = false;
    var ids = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            if (!active) {
                // first time making active true
                if ($makeCuesheet.val() === '') {
                    $makeCuesheet.val(titleOfPiece($(val)));
                }
            }
            active = true;
            ids.push(val.id);
        }
    });
    return ids;
}

function selectSiblingsInBetween($selectForCuesheet) {
    // if between checked items there are unchecked, check them
    var keys = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            keys.push(key);
        }
    });
    if (keys.length > 1) {
        for (var i = 1; i < keys.length; i++) {
            if (keys[i] - keys[i-1] > 1) {
                for (var j = keys[i-1] + 1; j < keys[i]; j++) {
                    $selectForCuesheet.get(j).checked = true;
                }
            }
        }
    }
}

function selectCheckboxes($selectForCuesheet, $makeCuesheet, mode) {
    var active = false;
    var ids = [];
    $.each($selectForCuesheet, function(key, val) {
        val.checked = mode;
        if (mode) {
            ids.push(val.id);
            if (!active) {
                // first time making active true: use title of piece for cuesheet title
                if ($makeCuesheet.val() === '') {
                    $makeCuesheet.val(titleOfPiece($(val)));
                }
                active = true;
            }
        }
    });
    return ids;
}

function getAlbumComponisten() {
    var items = [];
    $.each($('li.hyperlink.componist'), function(key, li){
        items.push($(li).find('a').text().trim());
    });
    return items;
}

function copyComponist(componist, $makeCuesheet) {
    // const normalizedComponist = componist.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
    var val = $makeCuesheet.val();
    if (val[0] !== ' ' && val[0] !== '-') {val = ' - ' + val;}
    $makeCuesheet.val(componist + val);
}

function similar($selectForCuesheet) {
    var titles = [];
    var ids = [];
    var common = '';
    var active = false;
    var old_common = '';
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            active = true;
        }
        if (active) {
            val.checked = false;
            ids.push(val.id);
            titles.push(titleOfPiece($(val)));
            common = lcs(titles);
            if (titles.length > 2 && common.length < old_common.length - 2) {
                titles.pop();
                ids.pop();
                val.checked = true;
                return false;  // break each()
            }
            old_common = common;
        }
    });
    return {
        titles: titles,
        ids: ids
    };
}

function rtrim(s, a) {
    a.forEach(function(c){
       if (s.substr(s.length - c.length) === c) {
            s = s.substr(0, s.length - c.length);
            s = s.trim();
        }
    });
    return s;
}

function ltrim(s, a) {
    a.forEach(function(c){
       if (s.length < 2) {
           return;
       }
       if (s.substr(0, 1) === c) {
            s = s.substr(1);
            s = s.trim();
        }
    });
    return s;
}

function trimNr(s) {
    s = s.trim();
    s = rtrim(s, ['No.', 'I', '-', ',', '.flac', ':']);
    s = ltrim(s, ['.', '-']);
    return s.trim();
}

function lcs_pieces($selectForCuesheet, $makeCuesheet){
    var titles = [];
    var ids = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            titles.push(titleOfPiece($(val)));
            ids.push(val.id);
        }
    });
    if (titles.length === 1) {
        const data = similar($selectForCuesheet);
        titles = data.titles;
        ids = data.ids;
    }
    $makeCuesheet.val(trimNr(lcs(titles)));
    return ids;
}

function markTestedCuesheets(ids) {
    var pieces = $('.stukken .piece');
    pieces.removeClass('selected');
    ids.forEach(function(id){
        $.each(pieces, function(){
            var $this = $(this);
            if ($this.attr('id') === id) {
                $this.addClass('selected');
            }
        })
    });
}

$(function () {
    function unmarkTestedCuesheets() {
        var pieces = $('.stukken .piece');
        pieces.removeClass('selected');
    }

    function testCheck($selectForCuesheet) {
        var found = false;
        $.each($selectForCuesheet, function(key, val) {
            if (val.checked) {
                found = true;
            }
        });
        return found;
    }

    function testLcs($selectForCuesheet, $makeCuesheet, cuesheetIds) {
        if (!testCheck($selectForCuesheet)) {
            $selectForCuesheet.first().get(0).checked = true; // init following function
        }
        cuesheetIds = lcs_pieces($selectForCuesheet, $makeCuesheet);
        markTestedCuesheets(cuesheetIds);
    }

    /**
     * automatisch cuesheets cre-eren
     * spring naar volgende tot er geen meer zijn
     * restrictie: minimaal drie delen per nieuwe cuesheet (werkt niet)
     * @param $selectForCuesheet
     * @param cuesheetIds
     * @param $makeCuesheet
     * @param $typeahead
     */
    function autoCreate($selectForCuesheet, cuesheetIds, $makeCuesheet, $typeahead) {
        if (!testCheck($selectForCuesheet)) {
            $selectForCuesheet.first().get(0).checked = true; // init following function
            // console.log('checking first piece for automation');
        }
        do {
            cuesheetIds = lcs_pieces($selectForCuesheet, $makeCuesheet);
            if (cuesheetIds.length) {
                console.log(cuesheetIds);
                createCuesheet($makeCuesheet, cuesheetIds, $typeahead);
            }
        } while (cuesheetIds.length);
        location.reload();
    }

    function afterPostMake($makeCuesheet, $typeahead) {
        $makeCuesheet.val('');
        var items = getAlbumComponisten();
        if (items.length === 1) {$typeahead.val(items[0]); }
        else { $typeahead.val('')}
        unmarkTestedCuesheets();
    }

    function createCuesheet($makeCuesheet, cuesheetIds, $typeahead) {
        postMakeCuesheet($makeCuesheet.val(), cuesheetIds, function() {
            afterPostMake($makeCuesheet, $typeahead)});
    }

    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        const $selectForCuesheet = $('.select-for-cuesheet'),
            $makeCuesheet = $('.make-cuesheet'),
            $typeahead = $('.album-componist.typeahead');
        var cuesheetIds = [];

        $selectForCuesheet.click(function (e) {
            if (e.shiftKey) {
                selectSiblingsInBetween($selectForCuesheet);
            }
            cuesheetIds = getSelectedCuesheetIds($selectForCuesheet, $makeCuesheet);
        });
        $makeCuesheet.keydown(function (e) {
            if (e.key === 'Enter') {
                postMakeCuesheet($(e.target).val(), cuesheetIds, function() {
                    afterPostMake($makeCuesheet, $typeahead)});
            }
        });
        $('.test-lcs').click(function(){
            testLcs($selectForCuesheet, $makeCuesheet, cuesheetIds);
        });
        $('.auto-create').click(function(){
            autoCreate($selectForCuesheet, cuesheetIds, $makeCuesheet, $typeahead);
        });
        typeaheadAlbumComponisten($typeahead, $makeCuesheet);
        $('.album-componist-to-make').click(function () {
            copyComponist($typeahead.val(), $makeCuesheet);
        });
        $('.create-cuesheet').click(function(){
            createCuesheet($makeCuesheet, cuesheetIds, $typeahead);
        });
        $('.rename-cuesheet').click(function(){
            // todo: get new name
            var newName = prompt('Nieuwe naam?');
            postRenameCuesheet(this.id, $('#album_id').val(), newName, function() {
                location.reload();
            });
        });
        $('.stukken .check-all').click(function () {
            cuesheetIds = selectCheckboxes($selectForCuesheet, $makeCuesheet, true);
        });
        $('.stukken .check-nothing').click(function () {
            cuesheetIds = selectCheckboxes($selectForCuesheet, $makeCuesheet, false);
        });
        $('.stukken .clear-title').click(function() {
            $makeCuesheet.val('');
        });
    }
});