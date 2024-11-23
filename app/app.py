import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
from navigation import show_navigation


@st.cache_resource
def get_df():
    df = pd.read_csv("../data/understat_all_players_data.csv")
    return df


def create_radar_chart(player_name, df):
    metrics = [
        "goals",
        "xG",
        "assists",
        "xA",
        "shots",
        "key_passes",
        "xGChain",
        "xGBuildup",
    ]
    metric_names = [
        "Goals",
        "xG",
        "Assists",
        "xA",
        "Shots",
        "Key Passes",
        "xGChain",
        "xGBuildup",
    ]

    player_data = df[df["player_name"] == player_name]
    if player_data.empty:
        st.write(f"Player {player_name} not found.")
        return None
    player_data = player_data.iloc[0]

    max_values = df[metrics].max()
    player_values = player_data[metrics] / max_values
    player_values = player_values.fillna(0)

    fig = go.Figure(
        data=go.Scatterpolar(
            r=player_values.tolist() + [player_values.tolist()[0]],
            theta=metric_names + [metric_names[0]],
            fill="toself",
            name=player_name,
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        title=f"Performance Radar Chart for {player_name}",
    )
    return fig


def create_comparison_radar_chart(player1, player2, df):
    metrics = [
        "goals",
        "xG",
        "assists",
        "xA",
        "shots",
        "key_passes",
        "xGChain",
        "xGBuildup",
    ]
    metric_names = [
        "Goals",
        "xG",
        "Assists",
        "xA",
        "Shots",
        "Key Passes",
        "xGChain",
        "xGBuildup",
    ]

    data = []
    max_values = df[metrics].max()

    for player_name, color in zip([player1, player2], ["blue", "red"]):
        player_data = df[df["player_name"] == player_name]
        if player_data.empty:
            st.write(f"Player {player_name} not found.")
            continue
        player_data = player_data.iloc[0]
        player_values = player_data[metrics] / max_values
        player_values = player_values.fillna(0)
        data.append(
            go.Scatterpolar(
                r=player_values.tolist() + [player_values.tolist()[0]],
                theta=metric_names + [metric_names[0]],
                fill="toself",
                name=player_name,
            )
        )

    if data:
        fig = go.Figure(data=data)
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title=f"Performance Comparison: {player1} vs {player2}",
        )
        return fig
    else:
        st.write("Could not create comparison chart due to missing player data.")
        return None


def find_similar_players(player_name, df, metrics, top_n=5):
    scaler = StandardScaler()
    X = scaler.fit_transform(df[metrics])

    if player_name not in df["player_name"].values:
        st.write(f"Player {player_name} not found.")
        return None

    idx = df[df["player_name"] == player_name].index[0]

    distances = cdist([X[idx]], X, metric="euclidean")[0]

    similar_indices = distances.argsort()
    similar_indices = similar_indices[similar_indices != idx]
    similar_indices = similar_indices[:top_n]

    similar_players = df.iloc[similar_indices]["player_name"].values
    return similar_players


st.set_page_config(page_title="Player Performance Dashboard", layout="wide")
st.sidebar.header("Filter Players")


def main():
    if "df" not in st.session_state:
        df = get_df()
        df_subset = df.sample(100)
        st.session_state.df = df_subset

    menu_items = {
        "🏠 Home": ("pages.page1", "Home Page"),
        ":pig: Pyg": ("pages.pyg", "Pyg"),
        "📞 Contact": ("pages.page3", "Contact Us"),
    }

    # Show the navigation sidebar and load the selected page
    show_navigation(menu_items)


if __name__ == "__main__":
    main()
