'use strict';

function ajaxPost(data, cb) {
    const url = '/ajax/';
    const headers = {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        headers: headers,
        dataType: 'json'
    }).done(function(response){
        console.log(response);
        if (cb) {
            cb(response);
        }
    }).fail(function(err) {
        console.log(err);
        if (cb) {
            cb(err);
        }
    });
}

$(function(){
    var socket = new WebSocket('ws://' + window.location.host + '/chat/');
    function addToLog(data) {
        const logger = document.getElementById('logger');
        if (logger) {
            if (logger.value.length) {
                logger.value += '\n';
            }
            logger.value += data.msg;
            logger.scrollTop = logger.scrollHeight;
        } else {
            switch(data.mode) {
                case 'info':
                    console.log(data.msg);
                    break;
                case 'error':
                    console.error(data.msg);
                    break;
                case 'warning':
                    console.warn(data.msg);
                    break;

            }
        }
    }

    socket.onopen = function open() {
        const msg = 'WebSockets connection created.';
        addToLog({'msg': msg, 'mode': 'info'});
    };

    socket.onmessage = function message(e) {
        // console.log(e);
        addToLog(JSON.parse(e.data));
        if (e.data.mode === 'error' && e.data.id) {
            var album = $('li.hyperlink[id=' + e.data.id + ']');
            if (album.length) {
                console.log('album', album);
                album.addClass('error');
            }
        }
    };

    if (socket.readyState === WebSocket.OPEN) {
        socket.onopen();
    }
    $('.test').click(function(){
        ajaxPost({
            'cmd': 'test'
        });
    })

});
