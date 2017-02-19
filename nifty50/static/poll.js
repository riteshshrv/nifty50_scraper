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
    var losers_data = JSON.parse(data.losers);
    var gainers_template = Mustache.render(template, {'scrips': gainers_data});
    var losers_template = Mustache.render(template, {'scrips': losers_data});

    document.getElementById('gainer_scrips').innerHTML = gainers_template;
    document.getElementById('loser_scrips').innerHTML = losers_template;

}

function poll() {
    $.ajax({
        url: "get",
        data: {
            "timestamp": (+ new Date() / 1000) | 0
        }
    }).done(function (data) {
        append_to_dom(data);
    }).always(function () {
        // Keep polling every 5 minutes
        var polling_interval = 5 * 60 * 1000;
        setTimeout(poll, polling_interval);
    })
}

$(document).ready(function () {
    poll();
})
