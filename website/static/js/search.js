/**
 * Created by orion on 14/11/2017.
 */

'use strict';

$(function () {
    function prepareTypeQuery(type) {
        const $typeahead = $('.search .' + type + ' .typeahead.tt-input'),
            li = $typeahead.parents('li').first(),
            qq = li.find('.query');  // typeahead class
        var val = '';
        if (qq.length === 0) {
            // console.log('Empty query for type ' + type);
            return null;
        }
        var count = 0, id = 0;
        $.each(qq, function(){
            const q = $(this);
            console.log('q', q.text());

            if (val.length) { val += ','; }
            id = getId(q.text());
            val += id;
            count++;
        });
        console.log('val', val);
        $('.search input[name=' + type + ']').val(getId(val))
        return {
            type: type,
            count: count,
            id: id
        };
    }
    function prepareQueries() {
        // prepare for subnit, by putting query values in the hidden fields
        // or, if just one item is searched, navigate to the matching album list
        const types = ['componist', 'performer', 'tag', 'instrument'],
            title = $('[name=title]').val();
        var done_types = [], done_type;
        types.forEach(function(type) {
            done_type = prepareTypeQuery(type);
            if (done_type) {
                done_types.push(done_type);
            }
        });
        if (!title && done_types.length === 1 && done_types[0].count === 1) {
            document.location = '/' + done_types[0].type + '/' + done_types[0].id;
            return false;
        }
        return true;
    }

    function getId(s) {
        var pos = s.lastIndexOf('_');
        return s.substr(pos + 1);
    }

    function clearSearch($this) {
        const $li = $this.parent('li').first();
        $li.find('.typeahead.tt-input').val('');
    }

    function insertQueryElement($typeahead, val, input) {
        const
            clear =
            $('<span>')
                .text('x')
                .addClass('clear')
                .on('click', function(e){
                    const clear = $(e.target),
                        q2 = clear.prev('.query'),
                        li = q2.parent('li');
                    q2.remove();
                    clear.remove();
                }),
            q =
            $('<i>')
                .text(val)
                .addClass('query');

        q.insertAfter(input);
        clear.insertAfter(q);
        $typeahead.typeahead('val', '');
    }

    function impl_query_typeahead(items, type) {
        const $typeahead = $('.search .' + type + ' .typeahead'),
            li = $typeahead.parent('li'),
            input = li.find('input').last();
        $typeahead.typeahead(typeaheadSettings,
            { source: match(items) }
        ).bind('typeahead:select', function(e, suggestion){
            insertQueryElement($typeahead, suggestion, input);
        }).keydown(function(e){
            if (e.key === 'Enter') {
                // e.preventDefault();  // prevent submit
            }
            if (e.key === 'Escape') {
                $typeahead.typeahead('val', '');
            }
        });
    }

    function typeAheadSearch(cmdGet, nameField, type) {
        ajaxGet({
            cmd: cmdGet
        }, function(response){
            var items = [];
            response.forEach(function(item) {
                items.push(item[nameField] + '_' + item.ID);
            });
            impl_query_typeahead(items, type);
        });
    }

    if ($('.search').length) {
        typeAheadSearch('instruments', 'Name', 'instrument');
        typeAheadSearch('performers', 'FullName', 'performer');
        typeAheadSearch('componisten', 'FullName', 'componist');
        typeAheadSearch('tags', 'Name', 'tag');
        $('.search [type=submit]').click(function() {
            return prepareQueries();
        });
        $('.search .clear').click(function(){
            clearSearch($(this));
        });
    }});

