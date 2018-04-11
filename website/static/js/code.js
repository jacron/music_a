/**
 * Created by orion on 08/10/2017.
 */
'use strict';

$(function () {

    const
    KEYWORDS = {
        K: {
            prefix: 'K ',
            codes: ['K. ', 'K.', 'K ', 'K']
        },
        BWV: {
            prefix: 'bwv ',
            codes: ['BWV ', 'BWV.', 'Bwv ', 'BWV']
        },
        gold: {
            prefix: 'gold ',
            codes: ['variation ', 'Variation ', 'Variatio ']
        },
        KV: {
            prefix: 'KV ',
            codes: ['K. ', 'K.', 'K ', 'KV ', 'KV', 'K']
        },
        D: {
            prefix: 'D ',
            codes: [ 'D ', 'D']
        }
    },
    CELLO_SUITES_NAMES =['Prelude|Prélude|Praeludium', 'Allemande', 'Courante', 'Sarabande',
                'Menuet|Bourree|Gavotte', 'Gigue'],
    ROMANS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'],
    LEFT_TRIMS = ['#', 'No.', 'Nr.', 'No', 'no.'],
    RIGHT_TRIMS = [',', '.', ':'];

    function celloSuites() {
        for (var i = 0; i < CELLO_SUITES_NAMES.length; i++) {
            const name = CELLO_SUITES_NAMES[i],
                w = name.split('|');
            for (var j = 0; j < w.length; j++) {
                if (v.indexOf(w[j]) === 0) {
                    return i + 1;
                }
            }
        }
        return null;
    }
    function prop(v) {
        // special for cello suites (Bach): convert names to numbers
        var cello_suites = false;
        if (cello_suites) {
            var n = celloSuites(v);
            if (n) { return n; }
        }
        // trim right
        RIGHT_TRIMS.forEach(function(last){
            if (v.substr(v.length-1, 1) === last) {
                v = v.substr(0, v.length-1);
            }
        });
        // trim left
        LEFT_TRIMS.forEach(function(first){
            if (v.indexOf(first) === 0) {
                v = v.substr(first.length);
            }
        });
        // convert roman digits
        const pos = ROMANS.indexOf(v);
        if (pos !== -1) {
            return pos + 1;
        }
        if ($.isNumeric(v)) {
            return v;
        }
    }

    function parseCode(text, prefix) {
        var proposal = '';
        const w = text.split(" ");
        // skip the first (number?) word, so i = 1
        var nrs = [];
        for (var i = 1; i < w.length; i++) {
            var p = prop(w[i]);
            if (p) {
                nrs.push(p);
            }
        }
        if (nrs.length === 1) {
            return proposal + nrs[0];
        }
        // negeer het tweede getal, bijv. 'BWV 1010'
        if (nrs.length > 2) {
            return proposal + nrs[0] + '_' + nrs[2];
        }
        if (nrs.length > 1) {
            return proposal + nrs[0] + '_' + nrs[1];
        }
        return proposal;
    }

    function long_parse(proposal, text) {
        const w = text.split(" ");
        var nrs = [];
        // skip first word, is already parsed
        for (var j = 1; j < w.length; j++) {
            var p = prop(w[j]);
            if (p) {
                nrs.push(p);
            }
        }
        if (nrs.length) {
            proposal += '_' + nrs[0];
            // proposal = nrs[0];
        } else {
            // speciaal geval, e.g. 'BWV1004'
            for (var k = 1; k < w.length; k++) {
                var word = w[k];
                if (word.substr(0, 3).toLowerCase() === 'bwv') {
                    var n = word.substr(3);
                    while (n.substr(0,1) === '0') {
                        n = n.substr(1);
                    }
                    return proposal + n;
                }
            }
            if (nrs.length) {
                proposal += '_' + nrs[0];
                // proposal = nrs[0];
            }
        }
        return proposal;
    }

    function parseKCode(text, keywords, short) {
        var proposal = '';
        for (var i = 0; i < keywords.length; i++) {
            const keyword = keywords[i],
                pos = text.indexOf(keyword);
            if (pos !== -1) {
                if (short) {
                    return parseInt(text.substr(pos + keyword.length));
                }
                proposal += parseInt(text.substr(pos + keyword.length));
                text = text.substr(pos + keyword.length);
                break;
            }
        }
        if (!short) {
            return long_parse(proposal, text);
        }
    }

    function addCodeAll($this) {
        $('.add-code.first').each(function(){
            addCode($(this), true);
        });
        $('.saved').removeClass('saved');
        $this.addClass('saved');
    }

    function postCode(id, code, $this, $code, nomark) {
        ajaxPost({
            cmd: 'add_code',
            id: id,
            code: code
        }, function() {
            if (!nomark) {
                $('.saved').removeClass('saved');
                $this.addClass('saved');
            }
            $code.text('<' + code + '>');
        });
    }

    function addCode($this, nomark) {
        const
            id = $this.attr('id'),
            doPrompt = $this.attr('prompt'),
            hyperlink = $this.parents('.hyperlink'),
            $code = hyperlink.find('.code'),
            $title = hyperlink.find('.title'),
            text = $title.text(),
            keywords = KEYWORDS.gold; // choose your keywords here
        let proposal;

        proposal = parseKCode(text, keywords.codes, true);
        // proposal = parseCode(text, 'gold ');
        let code = keywords.prefix + proposal;
        // alternative: if there already is a code, use that
        if ($code.text().length) {
            // console.log($code.text().trim());
            code = $code.text().trim().replace('<', '').replace('>', '');
        }
        if (doPrompt && doPrompt === 'true') {
            code = prompt('Code', code);
            if (code === null) {  // escape
                return;
            }
        } else {
            if (!proposal.length) {  // empty code
                return;
            }
        }
        postCode(id, code, $this, $code, nomark);
    }

    function removeCodeAll($this) {
        $('.add-code.first').each(function(){
            removeCode($(this));
        });
        $('.saved').removeClass('saved');
        $this.addClass('saved');
    }

    function removeCode($this) {
        ajaxPost({
            cmd: 'remove_code',
            id: $this.attr('id')
        }, function() {
            $('.add-code').removeClass('saved');
            $this.removeClass('selected');
            $this.addClass('saved');
            const hyperlink = $this.parents('.hyperlink'),
                $code = hyperlink.find('.code');
            $code.text('<None>');
        });
    }

    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        $('.add-code').click(function() {
            addCode($(this));
        });
        $('.remove-code').click(function() {
            removeCode($(this));
        });
        $('.add-code-all').click(function() {
            addCodeAll($(this));
        });
        $('.remove-code-all').click(function() {
            removeCodeAll($(this));
        });
    }
});