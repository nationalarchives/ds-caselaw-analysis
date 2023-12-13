import re
import json
import sys
from datetime import datetime, timedelta
from urllib import parse
import pandas as pd
from crawlerdetect import CrawlerDetect


SESSION_TIMEOUT = 25 * 60

judgment_url_regex = "^/[a-z]+(/[a-z]+)*/[0-9]+(/[0-9]+)*/?$"
search_url_regex = "^/judgments/(advanced_)?search/?$"

if  __name__ == '__main__':

    infile = sys.argv[0]
    outfile = sys.argv[1]

    logs = pd.read_csv(infile, sep="\t")

    searches_and_judgments = logs[
        logs["cs-uri-stem"].str.match(judgment_url_regex)
        | logs["cs-uri-stem"].str.match(search_url_regex)
    ]

    query_keys = ['court', 'query','party', 'from_year', 'from_day', 'neutral_citation', 'specific_keywords', 'from_month', 'to_day', 'to_month', 'to_year', 'judge', 'from', 'to', 'order']
    def same_query(params1, params2):
        for key in query_keys:
            if key in params1 and key in params2:
                if params1[key] != params2[key]:
                    return False
            elif key in params1 and key not in params2:
                return False
            elif key not in params1 and key in params2:
                return False
        return True

    crawler_detect = CrawlerDetect()
    searches = []
    sessions = {}
    for (_ix, row) in searches_and_judgments.iterrows():
        if not crawler_detect.isCrawler(parse.unquote(row["cs(User-Agent)"])):
            ip = row["c-ip"]
            path = row["cs-uri-stem"]
            if re.match(search_url_regex, path):
                query = parse.parse_qs(row["cs-uri-query"])
                if (ip in sessions and not same_query(query, sessions[ip]["query"])) or (ip not in sessions):
                    search = { "query": query, "documents": [], "timestamp": datetime.fromisoformat("%sT%s" % (row["date"], row["time"])) }
                    sessions[ip] = search
                    searches.append(search)
            elif re.match(judgment_url_regex, path):
                if ip in sessions and datetime.fromisoformat("%sT%s" % (row["date"], row["time"])) - sessions[ip]["timestamp"] <= timedelta(seconds=SESSION_TIMEOUT):
                    sessions[ip]["documents"].append(row["cs-uri-stem"])

    with open("", "w") as file:
        json.dump(searches, outfile)