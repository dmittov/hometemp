/**
 * Created by Dmitry Mittov <mittov@gmail.com> on 2/6/16.
 */

function load_data(chart) {
    return function(data) {
        chart.load({columns: data});
    }
}

$( document ).ready(function() {
    var chart = c3.generate({
        bindto: '#chart',
        data: {
            columns: [],
            axes: {
                humidity: 'y2'
            },
            type: 'spline',
            colors: {
                humidity: '#0099ff',
                temp: '#ff5050'
            }
        },
        axis: {
            y2: {
                show: true
            }
        }
    });
    $.getJSON('day/home_DHT22', load_data(chart));
});
