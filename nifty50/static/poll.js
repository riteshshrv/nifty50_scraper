"use strict";

function append_to_dom(data) {
    // data = "{'gainers': "[{'aa': 1, ..}, ..]", 'losers': "[{'ba': 2, ..}, ..]"}"
    var data = JSON.parse(data);

    if (data.length == 0) {
        return
    }

    var template = document.getElementById('template').innerHTML;
    Mustache.parse(template);

    var gainers_data = JSON.parse(data.gainers);
    var rendered = Mustache.render(template, {'gainer_scrips': gainers_data});

    document.getElementById('gainer_scrips').innerHTML = rendered;

}

function poll() {
    $.ajax({
        url: "get",
        data: {
            "timestamp": (+ new Date() / 1000) | 0
        }
    }).done(function (data) {
        console.log('fetched request');
        append_to_dom(data);
    }).always(function () {
        setTimeout(poll, 18000);
    })
}

$(document).ready(function () {
    poll();
})
