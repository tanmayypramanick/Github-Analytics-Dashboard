
# Import all the required packages 
import os
from flask import Flask, jsonify, request, make_response, Response
from flask_cors import CORS
import json
import dateutil.relativedelta
from dateutil import *
from datetime import date
import pandas as pd
import requests
from datetime import datetime as dt
# Initilize flask app
app = Flask(__name__)
# Handles CORS (cross-origin resource sharing)
CORS(app)
 
# Add response headers to accept all types of  requests
def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods",
                         "PUT, GET, POST, DELETE, OPTIONS")
    return response

# Modify response headers when returning to the origin
def build_actual_response(response):
    response.headers.set("Access-Control-Allow-Origin", "*")
    response.headers.set("Access-Control-Allow-Methods",
                         "PUT, GET, POST, DELETE, OPTIONS")
    return response

'''
API route path is  "/api/forecast"
This API will accept only POST request
'''


@app.route('/api/github', methods=['POST'])
def github():
    body = request.get_json()
    # Extract the choosen repositories from the request
    repo_name = body['repository']
    print("repo_name", repo_name)
    # Add your own GitHub Token to run it local
    token = os.environ.get(
        'GITHUB_TOKEN', 'key')
    GITHUB_URL = f"https://api.github.com/"
    print("API Called by Shubham")
    headers = {
        "Authorization": f'token {token}'
    }
    params = {
        "state": "open"
    }
    repository_url = GITHUB_URL + "repos/" + repo_name
    # Fetch GitHub data from GitHub API
    repository = requests.get(repository_url, headers=headers)
    # Convert the data obtained from GitHub API to JSON format
    repository = repository.json()

    
    stars_count=[]
    fork_count=[]
    if repo_name[0] == 'X':
        repo_list = repo_name.split()
        repo_list.pop(0)
        for i in repo_list:
            GITHUB_URL = f"https://api.github.com/"
            headers = {
            "Authorization": f'token {token}'
            }
            params = {
            "state": "open"
            }
            repository_url = GITHUB_URL + "repos/" + i
            # Fetch GitHub data from GitHub API
            repository = requests.get(repository_url, headers=headers)
            # Convert the data obtained from GitHub API to JSON format
            repository = repository.json()
            stars_count.append([i.split("/")[1], repository["stargazers_count"]])
        json_response_stars = {
        "stars": stars_count
        }
        print("from flask /api/github, json_response_stars",json_response_stars)
        return jsonify(json_response_stars)

    if repo_name[0] == 'Y':
        repo_list = repo_name.split()
        repo_list.pop(0)
        for i in repo_list:
            GITHUB_URL = f"https://api.github.com/"
            headers = {
            "Authorization": f'token {token}'
            }
            params = {
            "state": "open"
            }
            repository_url = GITHUB_URL + "repos/" + i
            # Fetch GitHub data from GitHub API
            repository = requests.get(repository_url, headers=headers)
            # Convert the data obtained from GitHub API to JSON format
            repository = repository.json()
            fork_count.append([i.split("/")[1], repository["forks_count"]])
        json_response_fork = {
        "forks": fork_count
        }
        print("from flask /api/github, json_response_fork",json_response_fork)

        return jsonify(json_response_fork)  

        for issue in response.get("items", []):
            created_at = issue.get("created_at", "")[:10]
            closed_at = issue.get("closed_at", None)
            issues_response.append({
                "issue_number": issue.get("number"),
                "created_at": created_at,
                "closed_at": closed_at[:10] if closed_at else None,
                "state": issue.get("state", "unknown")
            })
    today = date.today()

    issues_reponse = []
    pull_req_response = []
    commit_response = []
    branch_response = []
    releases_response = []
    contributors_response = []
    print("REPO: ",repo_name)
    #Get Contributors
    n=0
    for i in range(1):
        
        query_url = GITHUB_URL + "repos/" + repo_name + "/contributors" + "?anon=1"
        # requsets.get will fetch requested query_url from the GitHub API
        search_contributors = requests.get(query_url, headers=headers, params=params)
        # Convert the data obtained from GitHub API to JSON format
        search_contributors = search_contributors.json()
        #print(search_contributors)

        contributor_items = []
        contributor_items = search_contributors
        if contributor_items is None:
            continue
        for contributor in contributor_items:
            label_name = []
            data = {}
            current_contributor = contributor
            #print(type(current_contributor))
            # Get issue number
            #print("pulls: \n",current_contributor)
            n=n+1
            data['contributor_number'] = n
            #data['contributions'] = current_contributor["contributions"]
            data['contributor_name'] = current_contributor.get("login") #GET ALL the contributors
            contributors_response.append(data)
        print("contributor:\n", )

 
     # Process weekly and monthly data
    df = pd.DataFrame(issues_response)
    weekly_created = df['created_at'].groupby(pd.to_datetime(df['created_at']).dt.to_period('W')).size().to_dict()
    monthly_created = df['created_at'].groupby(pd.to_datetime(df['created_at']).dt.to_period('M')).size().to_dict()

    n=0
    for i in range(1):
        
        last_month = today + dateutil.relativedelta.relativedelta(months=-1)
        ranges = 'created:' + str(last_month) + '..' + str(today)
        per_page = 'per_page=100'
        search_query = per_page + "&" + ranges

        # Append the search query to the GitHub API URL 
        query_url = GITHUB_URL + "repos/" + repo_name + "/releases?" + search_query
        # requsets.get will fetch requested query_url from the GitHub API
        search_releases = requests.get(query_url, headers=headers, params=params)
        # Convert the data obtained from GitHub API to JSON format
        search_releases = search_releases.json()
        #print(search_releases)

        releases_items = []
        releases_items = search_releases
        if releases_items is None:
            continue
        for releases in releases_items:
            label_name = []
            data = {}
            current_release = releases
            # Get issue number
            #print("pulls: \n",current_release)
            n=n+1
            data['release_number'] = n
            # Get created date of issue
            data['created_at'] = current_release["created_at"][0:10]
            #Get release name
            data['name'] = current_release["name"]
            # Get Author of issue
            #data['Author'] = current_release["author"]["login"]
            releases_response.append(data)
        
        

        today = last_month
    print("release:\n")
    today = date.today()

    #GET COMMITS DATA
    n=0
    # Iterating to get issues for every month for the past 2 months
    for i in range(60):
        per_page = 'per_page=100'
        page = 'page='
        search_query = per_page+ "&" + page + f'{i}'
        #repo_name = 'langchain-ai/langchain'
        # Append the search query to the GitHub API URL 
        query_url = GITHUB_URL + "repos/" + repo_name + "/commits?" + search_query
        # requsets.get will fetch requested query_url from the GitHub API
        search_commits = requests.get(query_url, headers=headers, params=params)
        # Convert the data obtained from GitHub API to JSON format
        search_commits = search_commits.json()
        #print(search_commits)

        commits_items = []
        commits_items = search_commits
        if commits_items is None:
            continue
        for commit_req in commits_items:
            label_name = []
            data = {}
            current_commit = commit_req
            # Get issue number
            #print("pulls: \n",current_commit)
            created_at_date = dt.strptime(current_commit["commit"]["committer"]["date"][0:10], "%Y-%m-%d")
            max_date = dt.strptime("2022-11-19", "%Y-%m-%d")
            if created_at_date > max_date:
                n=n+1
                data['commit_number'] = n
                # Get created date of issue
                data['created_at'] = current_commit["commit"]["committer"]["date"][0:10]
                commit_response.append(data)
        
    print("commit:\n")
    
    #GET PULL REQUESTS
    for i in range(2):
        per_page = 'per_page=100'
        page = 'page='
        search_query = 'langchain-ai/langchain' + '/pulls?state=all' + "&" + per_page+ "&" + page + f'{i}'
        # Append the search query to the GitHub API URL 
        query_url = GITHUB_URL + "repos/" + search_query
        # requsets.get will fetch requested query_url from the GitHub API
        search_pull_requests = requests.get(query_url, headers=headers, params=params)
        # Convert the data obtained from GitHub API to JSON format
        search_pull_requests = search_pull_requests.json()
        pull_items = []
        pull_items = search_pull_requests
        if pull_items is None:
            continue
        for pull_req in pull_items:
            label_name = []
            data = {}
            current_pull_req = pull_req
            # Get issue number
            created_at_date = dt.strptime(current_pull_req["created_at"][0:10], "%Y-%m-%d")
            max_date = dt.strptime("2022-11-19", "%Y-%m-%d")
            if created_at_date > max_date:
                data['pull_req_number'] = current_pull_req["number"]
                # Get created date of issue
                data['created_at'] = current_pull_req["created_at"][0:10]
                if current_pull_req["closed_at"] == None:
                    data['closed_at'] = current_pull_req["closed_at"]
                else:
                    # Get closed date of issue
                    data['closed_at'] = current_pull_req["closed_at"][0:10]
                for label in current_pull_req["labels"]:
                    # Get label name of issue
                    label_name.append(label["name"])
                data['labels'] = label_name
                # It gives state of issue like closed or open
                data['State'] = current_pull_req["state"]
                # Get Author of issue
                data['Author'] = current_pull_req["user"]["login"]
                pull_req_response.append(data)
        
    print("pulls:\n")
    
    #Fetch ISSUES DATA
    today = date.today()
    for i in range(24):
        last_month = today + dateutil.relativedelta.relativedelta(months=-1)
        types = 'type:issue'
        repo = 'repo:' + repo_name
        ranges = 'created:' + str(last_month) + '..' + str(today)
        # By default GitHub API returns only 30 results per page
        # The maximum number of results per page is 100
        # For more info, visit https://docs.github.com/en/rest/reference/repos 
        per_page = 'per_page=100'
        # Search query will create a query to fetch data for a given repository in a given time range
        search_query = types + ' ' + repo + ' ' + ranges

        # Append the search query to the GitHub API URL 
        query_url = GITHUB_URL + "search/issues?q=" + search_query + "&" + per_page
        print("arpit query_url: ",query_url)
        # requsets.get will fetch requested query_url from the GitHub API
        search_issues = requests.get(query_url, headers=headers, params=params)
        # Convert the data obtained from GitHub API to JSON format
        search_issues = search_issues.json()
        
       
        issues_items = []
        try:
            # Extract "items" from search issues
            issues_items = search_issues.get("items")
        except KeyError:
            error = {"error": "Data Not Available"}
            resp = Response(json.dumps(error), mimetype='application/json')
            resp.status_code = 500
            return resp
        if issues_items is None:
            continue
        for issue in issues_items:
            label_name = []
            data = {}
            current_issue = issue
            # Get issue number
            
            data['issue_number'] = current_issue["number"]
            # Get created date of issue
            data['created_at'] = current_issue["created_at"][0:10]
            if current_issue["closed_at"] == None:
                data['closed_at'] = current_issue["closed_at"]
            else:
                # Get closed date of issue
                data['closed_at'] = current_issue["closed_at"][0:10]
            for label in current_issue["labels"]:
                # Get label name of issue
                label_name.append(label["name"])
            data['labels'] = label_name
            # It gives state of issue like closed or open
            data['State'] = current_issue["state"]
            issues_reponse.append(data)

        today = last_month
    print("issues:\n")
    df = pd.DataFrame(issues_reponse)

    # Daily Created Issues
    df_created_at = df.groupby(['created_at'], as_index=False).count()
    dataFrameCreated = df_created_at[['created_at', 'issue_number']]
    dataFrameCreated.columns = ['date', 'count']
    print("DATAFrame: ",dataFrameCreated)


    '''
    Weekly Created Issues
    Format the data by grouping the data by month
    ''' 
    created_at = df['created_at']
    week_issue_created = pd.to_datetime(
        pd.Series(created_at), format='%Y-%m-%d')
    week_issue_created.index = week_issue_created.dt.to_period('w')
    week_issue_created = week_issue_created.groupby(level=0).size()
    week_issue_created = week_issue_created.reindex(pd.period_range(
        week_issue_created.index.min(), week_issue_created.index.max(), freq='w'), fill_value=0)
    week_issue_created_dict = week_issue_created.to_dict()
    week_created_at_issues = []
    for key in week_issue_created_dict.keys():
        array = [str(key), week_issue_created_dict[key]]
        week_created_at_issues.append(array)
    print("Weekly Created Issues\n")
    '''
    Weekly Closed Issues
    Format the data by grouping the data by month
    ''' 
    
    closed_at = df['closed_at'].sort_values(ascending=True)
    week_issue_closed = pd.to_datetime(
        pd.Series(closed_at), format='%Y-%m-%d')
    week_issue_closed.index = week_issue_closed.dt.to_period('w')
    week_issue_closed = week_issue_closed.groupby(level=0).size()
    week_issue_closed = week_issue_closed.reindex(pd.period_range(
        week_issue_closed.index.min(), week_issue_closed.index.max(), freq='w'), fill_value=0)
    week_issue_closed_dict = week_issue_closed.to_dict()
    week_closed_at_issues = []
    for key in week_issue_closed_dict.keys():
        array = [str(key), week_issue_closed_dict[key]]
        week_closed_at_issues.append(array)



    created_at_body = {
        "issues": issues_reponse,
        "type": "created_at",
        "repo": repo_name.split("/")[1]
    }
    closed_at_body = {
        "issues": issues_reponse,
        "type": "closed_at",
        "repo": repo_name.split("/")[1]
    }
    pull_request_body = {
        "pull": pull_req_response,
        "type": "pull_request",
        "repo": repo_name.split("/")[1]
    }
    commits_body = {
        "pull": commit_response,
        "type": "commits",
        "repo": repo_name.split("/")[1]
    }
    branch_body = {
        "pull": branch_response,
        "type": "branch",
        "repo": repo_name.split("/")[1]
    }
    release_body = {
        "pull": releases_response,
        "type": "release",
        "repo": repo_name.split("/")[1]
    }
    contributors_body = {
        "pull": contributors_response,
        "type": "contributors",
        "repo": repo_name.split("/")[1]
    }

    # Update your Google cloud deployed LSTM app URL (NOTE: DO NOT REMOVE "/")
    # prod https://lstm-nwsi2llnxa-uc.a.run.app/
    
    LSTM_API_URL = "https://lstm-506260022184.us-central1.run.app/api/forecast"
    LSTM_API_URL_FINAL = "https://lstm-506260022184.us-central1.run.app/"
    # change
    # LSTM_API_URL = "http://localhost:8080/api/forecast"
    # LSTM_API_URL_FINAL = "http://localhost:8080/"
  
    #Tensorflow
    #print("CC:", created_at_body)
    
    created_at_response = requests.post(LSTM_API_URL,
                                        json=created_at_body,
                                        headers={'content-type': 'application/json'})

        # Process weekly and monthly data
    df = pd.DataFrame(issues_response)
    weekly_created = df['created_at'].groupby(pd.to_datetime(df['created_at']).dt.to_period('W')).size().to_dict()
    monthly_created = df['created_at'].groupby(pd.to_datetime(df['created_at']).dt.to_period('M')).size().to_dict()

    pull_request_response = requests.post(LSTM_API_URL_FINAL+"api/pulls",
                                       json=pull_request_body,
                                       headers={'content-type': 'application/json'})
   
    commits_respnse = requests.post(LSTM_API_URL_FINAL+"api/commits",
                                       json=commits_body,
                                       headers={'content-type': 'application/json'})
    
    closed_at_response = requests.post(LSTM_API_URL,
                                       json=closed_at_body,
                                       headers={'content-type': 'application/json'})
    
    #stats model
    created_at_response_stat = requests.post(LSTM_API_URL_FINAL+"api/statmis",
                                        json=created_at_body,
                                        headers={'content-type': 'application/json'})


    pull_request_response_stat = requests.post(LSTM_API_URL_FINAL+"api/statmpull",
                                       json=pull_request_body,
                                       headers={'content-type': 'application/json'})

   
    commits_respnse_stat = requests.post(LSTM_API_URL_FINAL+"api/statmcommits",
                                       json=commits_body,
                                       headers={'content-type': 'application/json'})

    
    closed_at_response_stat = requests.post(LSTM_API_URL_FINAL+"api/statmisc",
                                       json=closed_at_body,
                                       headers={'content-type': 'application/json'})


    
    #fb profet api routes
    created_at_response_fb = requests.post(LSTM_API_URL_FINAL+"api/fbprophetis",
                                        json=created_at_body,
                                        headers={'content-type': 'application/json'})


    pull_request_fb_rpnse = requests.post(LSTM_API_URL_FINAL+"api/fbprophetpull",
                                       json=pull_request_body,
                                       headers={'content-type': 'application/json'})

   
    commits_fb_respnse = requests.post(LSTM_API_URL_FINAL+"api/fbprophetcommits",
                                       json=commits_body,
                                       headers={'content-type': 'application/json'})

    
    closed_at_fb_response = requests.post(LSTM_API_URL_FINAL+"api/fbprophetisc",
                                       json=closed_at_body,
                                       headers={'content-type': 'application/json'})

 
      # Final response structure
    json_response = {
        "contributors": contributors_response,
        "releases": releases_response,
        "branches": branch_response,
        "commits": commit_response,
        "pull_requests": pull_req_response,
        "issues": issues_response,
        "weekly_created_issues": weekly_created,
        "monthly_created_issues": monthly_created
    }
    json_response = {
        "created": created_at_issues,
        "created_weekly": week_created_at_issues,
        "closed": closed_at_issues,
        "closed_weekly": week_closed_at_issues,
        "starCount": repository["stargazers_count"],
        "forkCount": repository["forks_count"],
        "stat_createdAtImageUrls": {
            **created_at_response_stat.json(),
        },
        "stat_closedAtImageUrls": {
            **closed_at_response_stat.json(),
        },
        "stat_pullReqImageUrls": {
            **pull_request_response_stat.json(),
        },
        "stat_commitsImageUrls": {
            **commits_respnse_stat.json(),
        },

        "fb_createdAtImageUrls": {
            **created_at_response_fb.json(),
        },
        "fb_closedAtImageUrls": {
            **closed_at_fb_response.json(),
        },
        "fb_pullReqImageUrls": {
            **pull_request_fb_rpnse.json(),
        },
        "fb_commitsImageUrls": {
            **commits_fb_respnse.json(),
        },

        "createdAtImageUrls": {
            **created_at_response.json(),
        },
        "closedAtImageUrls": {
            **closed_at_response.json(),
        },
        "pullReqImageUrls": {
            **pull_request_response.json(),
        },
        "commitsImageUrls": {
            **commits_respnse.json(),
        },
    }
    print("json_response, ", json_response)
    # Return the response back to client (React App)
    return jsonify(json_response)


# Run flask app server on port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)