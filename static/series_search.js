//Setting an onKeyup even on the subredditName textinput so we can query subreddit names based on user input and return top predicted result
let source = document.getElementById("subredditName");
console.log(source.name);
source.onkeyup = getSubreddits;

let hostURL = "http://" + window.location.host;

async function getData(url) {
    const response = await fetch(url);

    return response.json();
}


async function getSubreddits(e){

    let url_to_use = hostURL +  "/subredditEndpoint?SearchTerm=" + e.target.value;

    //fetch(url_to_use).then(r =>  r.json().then(data => ({status: r.status, body: data}))).then(obj => console.log(obj));

    let subreddits = await getData(url_to_use);

    //fetch(url_to_use).then(response => response.json()).then(data => console.log(data));
    //fetch(url_to_use).then(response => response.json()).then(data => subreddits = data).then(obj => console.log(obj));

    subreddits = Object.keys(subreddits);

    let newHTML = "";

    for(let i=0; i<subreddits.length; i++){
        newHTML += "<option value=\"" + String(subreddits[i]) + "\"></option>";
    }
    
    let options = document.getElementById("subredditNameOptions");
    options.innerHTML = newHTML;
}

async function TVShowSearch() {

    let seriesTitle = document.getElementById("seriesTitle").value;
    console.log(seriesTitle);

    let url_to_use = hostURL + "/searchSeries?SeriesTitle=" + seriesTitle;
    console.log(url_to_use);

    let seriesSearchLoadingDisplay = document.getElementById("seriesSearchLoading");
    seriesSearchLoadingDisplay.style.display = "block";

    let seriesSearchResult = await getData(url_to_use);
    console.log(seriesSearchResult);

    let newHTML = "";
    for(const property in seriesSearchResult){
        console.log("Title: "  + property + " ID: " + seriesSearchResult[property])
    }

    let count = 1;
    for(const property in seriesSearchResult){
        newHTML += "<li class=\"list-group-item\"  name=\""+seriesSearchResult[property]+"\" onclick=\"SeriesEpisodeInfoSearch(this)\">(" + count + ") " + property + "</li>";
        count = count+1;
    }

    seriesSearchLoadingDisplay.style.display = "none";

    let searchResults = document.getElementById("seriesSearchResult");
    searchResults.style.display = "block";

    let options = document.getElementById("seriesSearchResultList");
    options.innerHTML = newHTML;


}

async function SeriesEpisodeInfoSearch(e){
    console.log("In Series Episode Info Search");
    console.log(e.getAttribute("name"));

    //hide the series name search results
    let searchResults = document.getElementById("seriesSearchResult");
    searchResults.style.display = "none";

    //show spinner
    let seriesSearchLoadingDisplay = document.getElementById("seriesSearchLoading");
    seriesSearchLoadingDisplay.style.display = "block";


    let series_ID = e.getAttribute("name");
    //console.log(series_ID);
    let url_to_use = hostURL + "/episodeInfoSearch?SeriesID=" + series_ID;
    let episodeInfoSearchResult = await getData(url_to_use);

    console.log(episodeInfoSearchResult);

    let total_seasons = episodeInfoSearchResult["totalSeasons"];

    let all_episodes = episodeInfoSearchResult["seriesEpisodes"];

    console.log(total_seasons);
    console.log(all_episodes);


    let newHTML = "<p>Showing Seasons and Episodes for chosen series:</p>";
    newHTML+= "<ul class=\"nav nav-tabs\" id=\"myTab\" role=\"tablist\">";

    for(let i=1; i<=total_seasons; i++){
        let current_season = "season" + String(i);
        newHTML+='<li class="nav-item" role="presentation">';
        newHTML+='<button class="nav-link" id="'+current_season+'-tab" data-bs-toggle="tab" data-bs-target="#'+current_season+'" type="button" role="tab" aria-controls="'+current_season+'" aria-selected="true"> Season ' + String(i) + '</button>'
        newHTML+="</li>";
    }
    newHTML+="</ul>";


    newHTML+='<div class="tab-content" id="myTabContent">';
    for(let i=1; i<=total_seasons; i++){
        let current_season = "season" + String(i);
        newHTML+='<div class="tab-pane fade" id="'+current_season+'" role="tabpanel" aria-labelledby="'+current_season+'-tab">';
        newHTML=="<br>"
        
        episodesForSeason = all_episodes[current_season];
        console.log("Episodes For Season");
        console.log(episodesForSeason);
        for(let value in episodesForSeason){
            console.log("Individual Episode");
            let episode = episodesForSeason[value];
            console.log(episode);
            newHTML+='<p draggable="true" ondragstart="drag(event)" data-date="'+episode["released"]+'">S'+episode["seasonNumber"]+'E'+episode["episodeNumber"]+' - '+episode["title"] +' : ['+episode["released"]+']</p>';
            //newHTML+='<p>S1 E1 - [Title] : [Release Date]</p>';
        }

        newHTML+='</div>';
    }

    newHTML+='</div>';


    //remove the spinner
    seriesSearchLoadingDisplay.style.display = "none";

    //update the html to show episode details
    let options = document.getElementById("episodeSearchResult");
    options.innerHTML = newHTML;

    //set season 1 to be the active tab
    document.getElementById("season1-tab").classList.add("active");
    document.getElementById("season1").classList.add("show");
    document.getElementById("season1").classList.add("active");
}