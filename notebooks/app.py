import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist

df_all = pd.read_csv('understat_all_players_data.csv')

df_all.fillna(0, inplace=True)

def create_radar_chart(player_name, df):
    metrics = [
        'goals', 'xG', 'assists', 'xA', 'shots', 'key_passes',
        'xGChain', 'xGBuildup'
    ]
    metric_names = [
        'Goals', 'xG', 'Assists', 'xA', 'Shots', 'Key Passes',
        'xGChain', 'xGBuildup'
    ]
    
    player_data = df[df['player_name'] == player_name]
    if player_data.empty:
        st.write(f"Player {player_name} not found.")
        return None
    player_data = player_data.iloc[0]
    
    max_values = df[metrics].max()
    player_values = player_data[metrics] / max_values
    player_values = player_values.fillna(0)
    
    fig = go.Figure(data=go.Scatterpolar(
        r=player_values.tolist() + [player_values.tolist()[0]],
        theta=metric_names + [metric_names[0]],
        fill='toself',
        name=player_name
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        title=f"Performance Radar Chart for {player_name}"
    )
    return fig

def create_comparison_radar_chart(player1, player2, df):
    metrics = [
        'goals', 'xG', 'assists', 'xA', 'shots', 'key_passes',
        'xGChain', 'xGBuildup'
    ]
    metric_names = [
        'Goals', 'xG', 'Assists', 'xA', 'Shots', 'Key Passes',
        'xGChain', 'xGBuildup'
    ]
    
    data = []
    max_values = df[metrics].max()
    
    for player_name, color in zip([player1, player2], ['blue', 'red']):
        player_data = df[df['player_name'] == player_name]
        if player_data.empty:
            st.write(f"Player {player_name} not found.")
            continue
        player_data = player_data.iloc[0]
        player_values = player_data[metrics] / max_values
        player_values = player_values.fillna(0)
        data.append(go.Scatterpolar(
            r=player_values.tolist() + [player_values.tolist()[0]],
            theta=metric_names + [metric_names[0]],
            fill='toself',
            name=player_name
        ))
    
    if data:
        fig = go.Figure(data=data)
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title=f"Performance Comparison: {player1} vs {player2}"
        )
        return fig
    else:
        st.write("Could not create comparison chart due to missing player data.")
        return None

def find_similar_players(player_name, df, metrics, top_n=5):
    scaler = StandardScaler()
    X = scaler.fit_transform(df[metrics])
    
    if player_name not in df['player_name'].values:
        st.write(f"Player {player_name} not found.")
        return None
    
    idx = df[df['player_name'] == player_name].index[0]
    
    distances = cdist([X[idx]], X, metric='euclidean')[0]
    
    similar_indices = distances.argsort()
    similar_indices = similar_indices[similar_indices != idx]
    similar_indices = similar_indices[:top_n]
    
    similar_players = df.iloc[similar_indices]['player_name'].values
    return similar_players

st.title("Player Performance Dashboard")

st.sidebar.header("Filter Players")
teams = ['All Teams'] + sorted(df_all['team_title'].unique())
selected_team = st.sidebar.selectbox("Select a team:", options=teams)

if selected_team != 'All Teams':
    players = df_all[df_all['team_title'] == selected_team]['player_name'].unique()
else:
    players = df_all['player_name'].unique()

player_name = st.sidebar.selectbox("Select a player:", players)

tab1, tab2, tab3 = st.tabs(["Player Stats", "Compare Players", "Similar Players"])

with tab1:
    st.header(f"Performance Metrics for {player_name}")

    player_data = df_all[df_all['player_name'] == player_name]
    stats_to_display = [
        'games', 'time', 'goals', 'xG', 'assists', 'xA', 'shots',
        'key_passes', 'yellow_cards', 'red_cards', 'npg', 'npxG',
        'xGChain', 'xGBuildup'
    ]
    player_stats = player_data[stats_to_display].T
    player_stats.columns = ['Value']
    st.table(player_stats)

    radar_chart = create_radar_chart(player_name, df_all)
    if radar_chart:
        st.plotly_chart(radar_chart)

with tab2:
    st.header("Compare Players")
    player1 = st.selectbox("Select first player:", players, key='player1')
    player2 = st.selectbox("Select second player:", players, key='player2')

    if player1 and player2:
        comparison_chart = create_comparison_radar_chart(player1, player2, df_all)
        if comparison_chart:
            st.plotly_chart(comparison_chart)

with tab3:
    st.header("Find Similar Players")

    similarity_metrics = [
        'goals', 'xG', 'assists', 'xA', 'shots', 'key_passes'
    ]

    similar_players = find_similar_players(player_name, df_all, similarity_metrics)

    if similar_players is not None:
        st.write(f"Players similar to {player_name}:")
        for sp in similar_players:
            st.write(f"- {sp}")
