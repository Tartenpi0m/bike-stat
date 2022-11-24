function today() {
    let d = new Date();
    let currDate = d.getDate();
    let currMonth = d.getMonth()+1;
    let currYear = d.getFullYear();
    return currYear + "-" + ((currMonth<10) ? '0'+currMonth : currMonth )+ "-" + ((currDate<10) ? '0'+currDate : currDate );
}

async function show_div_dashboard(first_time, stat) {
    console.log(stat)
    if(stat == 0) {
        query_jour('last');
    }
    query_period();

    let main_div = document.getElementById("main_div");
    let html_str = await eel.div_dashboard()();
    main_div.innerHTML = html_str;
    if (!first_time) {
        let period_img = document.getElementById("graph_period_img");
        period_img.src = "/cache/distance.png?t=" + new Date().getTime();

    }

    if(stat == 1) {
        console.log("stat = 1 ->")
        let html_str = await eel.div_stat_tmp()()
        document.getElementById("stat_jour").innerHTML = html_str;
    }
}

//used in div_dashboard.html
async function show_div_complete_form() {

    var nb_tour = document.getElementById("nb_tour").value;
    let html_str = await eel.div_complete(nb_tour)();
    let main_div = document.getElementById("main_div");
    main_div.innerHTML = html_str;

    document.getElementById('date_input').value = today();

}

async function show_div_simple_tour_form() {
    let html_str = await eel.div_simple()();
    let main_div = document.getElementById("main_div");
    main_div.innerHTML = html_str;
    document.getElementById('date_input').value = today();
}


async function send_data() {
    let dict = {
        "date" : document.getElementById("date_input").value,
        "go time" : document.getElementById("go_time").value,
        "return time" : document.getElementById("return_time").value,
        "distance tour" : document.getElementById("distance_tour_input").value,
        "distance allez" : document.getElementById("distance_allez_input").value,
        "distance retour" : document.getElementById("distance_retour_input").value
    };
    let i = 1;
    while(document.getElementById("tour_time_"+i) != null) {
        dict["tour " + i] = document.getElementById("tour_time_"+i).value;
        i++;
    }
    dict["nombre tours"] = i -1;

    dict = await eel.receive_data(dict)();

    show_div_dashboard(false, 0);
}

async function send_data_simple() {
    let dict = {
        "date" : document.getElementById("date_input").value,
        "time" : document.getElementById("time").value,
        "distance" : document.getElementById("distance_tour_input").value
    }

    console.log("send_data_simple");
    let data = await eel.receive_data_simple(dict)();
    show_div_dashboard(false, 1);
    show_stat(data);

}

async function show_stat(data) {
    let html_str = await eel.div_stat(data)();
    console.log("show_stat")
    document.getElementById("stat_jour").innerHTML = html_str;
}

async function query_jour(date) {
    await eel.query_jour(date)();
}

async function query_period() {
    await eel.query_period()();
}