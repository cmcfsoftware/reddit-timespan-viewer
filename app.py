from tracemalloc import start
from flask import Flask, render_template, url_for, request, jsonify
import datetime
import requests
import re
import json
import config

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "GET":
        return render_template("index.html")
    else:
        print("Post Request")

        subredditName = request.form["SubredditName"]
        start_date = start_date_readable = request.form["date1"]
        end_date = end_date_readable = request.form["date2"]

        print("Printing start and end dates")
        print(start_date)
        print(end_date)


        if(start_date):
            day, month, year = start_date.split(",")[0].split("/")
            start_date = int(datetime.datetime(int(year),int(month),int(day)).timestamp())
        
        if(end_date):
            day, month, year = end_date.split(",")[0].split("/")
            end_date = int(datetime.datetime(int(year),int(month),int(day)).timestamp())

        #day, month, year = start_date.split(",")[0].split("/")

        #start_date_epoch = datetime.datetime(int(year),int(month),int(day)).timestamp()

        #day, month, year = end_date.split(",")[0].split("/")

        #end_date_epoch = datetime.datetime(int(year),int(month),int(day)).timestamp()


        url = "https://api.pushshift.io/reddit/search/submission/?size=100&sort_type=score&sort=desc&subreddit=" + subredditName
        url += "&after="+str(start_date) if start_date else ""
        url += "&before="+str(end_date) if end_date else ""


        #from subreddit name, start and end epoch generate api url then return to results page

        #print(start_date_epoch)
        #print(end_date_epoch)
        print(url)

        url_response = requests.get(url)
        url_response = url_response.json()["data"]

        #print(len(url_response))
        print(url_response)

        print(len(url_response))

        url_response = {
            "start_date":start_date_readable,
            "end_date":end_date_readable,
            "data":url_response
        }

        print(len(url_response))


        return render_template("search_result.html", response = url_response)


@app.route("/data")
def data():
    return render_template("data.html")


@app.route("/searchResult")
def search_result():

    url_response = []
    return render_template("search_result.html", response = url_response)


#JSON endpoint for getting subreddit infor for subreddit name autocomplete
@app.route("/subredditEndpoint", methods=["POST", "GET"])
def subreddit_endpoint():

    if request.method == "GET":

        textfile = open("subreddits_subscribers.txt", 'r')
        filetext = textfile.read()
        textfile.close()

        regex_string = "^(?i)" + request.args.get('SearchTerm') + ".*$"
        matches = re.findall(regex_string, filetext, re.MULTILINE)

        split_matches = [[a, int(b)] if b != "None" else [a, -1] for a,b in [x.split(",") for x in matches]]

        split_matches.sort(key=lambda x: x[1], reverse=True)

        result_dict = {}

        for pair in split_matches[:5]:
            result_dict[pair[0]] = pair[1]

        return jsonify(result_dict) 

    else:

        textfile = open("subreddits_subscribers.txt", 'r')
        filetext = textfile.read()
        textfile.close()

        regex_string = "^" + request.form["SearchTerm"] + ".*$"
        matches = re.findall(regex_string, filetext, re.MULTILINE)

        split_matches = [[a, int(b)] if b != "None" else [a, -1] for a,b in [x.split(",") for x in matches]]

        split_matches.sort(key=lambda x: x[1], reverse=True)

        result_dict = {}

        for pair in split_matches[:5]:
            result_dict[pair[0]] = pair[1]

        result_dict

        return json.dumps(result_dict) 

#JSON endpoint for getting series information
@app.route("/searchSeries", methods=["POST", "GET"])
def series_search_result():
    if request.method == "GET":

        series_title_lookup = request.args.get('SeriesTitle')

        #remove whitespace if present
        series_title_lookup = series_title_lookup.replace(" ", "")

        url = "https://imdb-api.com/en/API/SearchSeries/" + config.API_KEY + "/" + series_title_lookup


        url_response = requests.get(url) #removed for testing will bring back
        url_response = url_response.json()["results"]
        

        series_search_results = {}
 
        for series in url_response[0:5]:
            series_search_results[series["title"]] = series["id"]

        return jsonify(series_search_results)
    else:
        return "Test Post"


@app.route("/episodeInfoSearch", methods=["POST", "GET"])
def episode_info_search():

    if request.method == "GET":
        print("In GET")

        series_ID = request.args.get('SeriesID')

        url_for_getting_total_seasons = "https://imdb-api.com/en/API/Title/" + config.API_KEY + "/" + series_ID
        url_response_for_total_seasons = requests.get(url_for_getting_total_seasons)
        seasons_list = url_response_for_total_seasons.json()["tvSeriesInfo"]["seasons"]
        total_seasons = max(list(map(int, seasons_list)))

        series_episodes = {}

        for i in range(1, total_seasons+1):

            individual_season_URL = "https://imdb-api.com/en/API/SeasonEpisodes/" + config.API_KEY + "/"  +series_ID+"/"+str(i)
            url_response = requests.get(individual_season_URL)
            season_episodes = url_response.json()["episodes"]

            #str(datetime.datetime.strptime(episode["released"], '%d %b. %Y').strftime("%d/%m/%Y"))

            current_season_episodes = []
            for episode in season_episodes:
                print(datetime.datetime.strptime(episode["released"], '%d %b. %Y').strftime("%d/%m/%Y"))
                #str(datetime.datetime.strptime(episode["released"], '%d %b. %Y').strftime("%d/%m/%Y"))
                formated_release_date = str(datetime.datetime.strptime(episode["released"], '%d %b. %Y').strftime("%d/%m/%Y"))

                useful_episode_info = {
                    "seasonNumber":episode["seasonNumber"],
                    "episodeNumber":episode["episodeNumber"],
                    "title":episode["title"],
                    "released":formated_release_date
                }

                current_season_episodes.append(useful_episode_info)
            
            current_series_string = "season" + str(i)
            series_episodes[current_series_string] = current_season_episodes
   

        response_object = {
            "totalSeasons":total_seasons,
            "totalEpisodes":len(series_episodes),
            "seriesEpisodes":series_episodes
        }

        return jsonify(response_object)
    else:
        return "Test Post"


if __name__ == "__main__":
    app.run(debug=True)