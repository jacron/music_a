/**
 * Created by orion on 15/10/2017.
 */

'use strict';

function addInstrument($select) {
    const data = {
        cmd: 'add_instrument',
        instrumentid: $select.val(),
        albumid: $select.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

function newInstrument($input) {
    const data = {
        cmd: 'new_instrument',
        name: $input.val(),
        albumid: $input.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

function removeInstrument($this) {
        const data = {
        cmd: 'remove_instrument',
        id: $this.attr('id'),
        albumid: $('#album_id').val()
        // albumid: $this.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

$(function() {
   // instrument
   $('button.select-instrument').click(function () {
       addInstrument($('select.select-instrument'));
   });
   $('button.add-instrument').click(function() {
       newInstrument($('input.add-instrument'));
   });
   $('input.add-instrument').keydown(function(e) {
       if (e.key === 'Enter') {
        newInstrument($('input.add-instrument'));
       }
   });
   $('select.select-instrument').keydown(function(e){
       if (e.key === 'Enter') {
        addInstrument($('select.select-instrument'));
       }
   });
   $('.instrument .remove').click(function(){
       removeInstrument($(this));
   });

});