import plotly
import plotly.express as px

def compareFranchises(df, how):
    '''
    df: dataframe;
    how: 'relative' uses relative point values, 'absolute' uses actual point projections
    '''
    if how=='relative':
        main_stat = 'rel_proj'
        second_stat = 'pts_proj'
    elif how=='absolute':
        main_stat = 'pts_proj'
        second_stat = 'rel_proj'        
    fig = px.bar(df.loc[(df['starters'].notna())&(df['franchise_name'].notna())], 
                x="franchise_name", 
                y=main_stat, 
                color="position", 
                text='full_name', 
                color_discrete_map={
                    "QB": "hsla(210, 60%, 25%, 1)", 
                    "RB": "hsla(12, 50%, 45%, 1)", 
                    "WR": "hsla(267, 40%, 45%, 1)", 
                    "TE": "hsla(177, 68%, 36%, 1)", 
                    "PK": "hsla(14, 30%, 40%, 1)", 
                    "DEF": "hsla(35, 70%, 65%, 1)"}, 
                category_orders={
                    "pos": ["QB", "RB", "WR", "TE", "PK", "DEF"]},
                hover_name="full_name",
                hover_data={
                    main_stat:True, second_stat:True,
                    'full_name':False, 'position':False, 'franchise_name':False
                    },
                labels={
                    "franchise_name":"Franchise",
                    "rel_proj":"Relative Value",
                    'pts_proj':"Predicted Points",
                }
                )
    fig.update_layout(
                barmode='stack', 
                xaxis={'categoryorder':'total descending'},
                plot_bgcolor='rgba(0,0,0,0)',
                title="Franchise Comparison",
                font_family="Skia",
                showlegend=False
                )
    return fig


def liveScoring(df):
    # Sort values to put franchises and players in order of expected live score
    df = df.sort_values(by='expectedLiveScore', ascending=False, ignore_index=True)
    # Order franchises along x-axis by total expected live score
    fran_rank = df.groupby('franchise_name').sum().sort_values(by='expectedLiveScore', ascending=False)
    sorter = fran_rank.index
    df['franchise_name'] = df['franchise_name'].astype("category")
    df['franchise_name'].cat.set_categories(sorter, inplace=True)
    df.sort_values(["franchise_name"], inplace=True)
    # Create bar chart
    fig = px.bar(df, 
                x="franchise_name", 
                y="expectedLiveScore", 
                color="playerName", 
                color_discrete_sequence=list(df['color']),
                category_orders={
                    "pos": ["QB", "RB", "WR", "TE", "PK", "DF"]},
                text='playerName', 
                hover_name="playerName",
                hover_data={
                    'expectedLiveScore':True, 
                    'scoreTotal':True, 
                    'liveScore':True,
                    'playerName':False, 
                    'pos':False, 
                    'franchiseAbbrev':False
                    },
                labels={
                    "franchise_name":"Franchise",
                    "liveScore":"Current Score",
                    "expectedLiveScore":"Projected Score",
                    "scoreTotal":"Initial Prediction"
                }
                )
    fig.update_layout(
                barmode='stack', 
                xaxis={'categoryorder':'total descending'},
                plot_bgcolor='rgba(0,0,0,0)',
                title="Live Scoring",
                font_family="Skia",
                showlegend=False
                )
    return fig
