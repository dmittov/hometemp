/**
 * Created by Dmitry Mittov <mittov@gmail.com> on 2/6/16.
 */

function draw(data) {
    var svg = d3.select('#d3').append('p');
    svg.text(data);
}

$( document ).ready(function() {
    $.getJSON('day/home_DHT22', draw);
});
