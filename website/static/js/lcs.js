/**
 * Created by orion on 12/11/2017.
 *
 * "LCS"
 *
 * A new implementation that works just as well as the classical one, after
 * earlier implementations that I made in Java and python,
 * finding the Longest Common Substring in an array of strings.
 */

'use strict';

function getSmallest(lines) {
    let small = '';
    lines.forEach(function(line){
        if (small.length < line.length) {
            small = line;
        }
    });
    return small;
}

function lcs(lines) {
    const small = getSmallest(lines);
    let common = '';
    let temp_common = '';
    for (let i=0; i< small.length; i++) {
        const c = small[i];
        temp_common += c;
        $.each(lines, function(key, line) {
            if (line.indexOf(temp_common) === -1) {
                temp_common = c;
                $.each(lines, function(key2, line2) {
                    if (line2.indexOf(temp_common) === -1) {
                        temp_common = '';
                        return false;  // break each()
                    }
                });
                return false;  // break each()
            }
        });
        if (temp_common !== '' && temp_common.length > common.length) {
            common = temp_common;
        }
    }
    return common;
}
