import altair as alt
import pandas as pd
import os
import json
import urllib2
from pandas.io.json import json_normalize

def loadData():
    '''loads the data source for restaurant cuisine by zip code provided by the course'''

    source = urllib2.urlopen("https://raw.githubusercontent.com/lingyielia/D3-visual/master/data/nyc_restaurants_by_cuisine.json")
    nyc_cuisine = json.loads(source.read().decode())

    #now let's make our json file a workable dataframe
    df = json_normalize(nyc_cuisine)
    df.columns = ["cuisine"] + ["".join(element.split(".")) for element in df.columns[1:-1]] + ["total"]
    return df #should be dataframe for cuisine and counts for every zipcode


def draw_chart(data, zipcode):
    # color expression, highlights bar on mouseover
    color_expression    = "highlight._vgsid_==datum._vgsid_"
    color_condition     = alt.ConditionalPredicateValueDef(color_expression, "SteelBlue")

    #highlight bar when mouse is hovering
    highlight_selection = alt.selection_single(name="highlight", empty="all", on="mouseover")
    try:
        data = pd.concat([data["cuisine"], data["perZip"+zipcode]], axis=1).nlargest(25, "perZip"+zipcode)
        maxCount = int(data["perZip"+zipcode].max())
    except KeyError:
        maxCount = 1
        data = pd.DataFrame([{"cuisine":"", "perZip"+zipcode:0}])

    return alt.Chart(data) \
              .mark_bar(stroke="Black") \
              .encode(
                  alt.X("perZip"+zipcode+":Q",
                  axis=alt.Axis(title="Number of Restaurants"),
                    scale=alt.Scale(domain=(0,maxCount))),
                  alt.Y("cuisine:O", axis=alt.Axis(title="Cuisine Type"),
                    sort=alt.SortField(field="perZip"+zipcode,
                    op="argmax")),
                  alt.ColorValue("LightGrey",
                  condition=color_condition),
              ).properties(
                selection = highlight_selection,
              )
 
