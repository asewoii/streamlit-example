from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import random

# Fungsi untuk membuat graf jaringan dari data CSV
def create_social_network_graph_csv(csv_data):
    G = nx.Graph()
    for index, row in csv_data.iterrows():
        G.add_edge(row['name'], row['genre'])
    return G

# Fungsi untuk menggambar graf jaringan sosial menggunakan Plotly
def draw_social_network_graph(G):
    pos = nx.spring_layout(G, seed=42, k=0.2)  # Atur parameter k untuk jarak antara nodes
    edge_x = []
    edge_y = []
    edge_labels = []  # Tambahkan list untuk menyimpan label edge

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_labels.append(f"{edge[0]} - {edge[1]}")  # Simpan label edge
    
    # Fungsi untuk menghasilkan warna acak dalam format hex
    def random_color_hex():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color_hex = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        return color_hex

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5 + 0.5 * len(G[edge[0]]), color='grey'),  # Sesuaikan ketebalan edge dengan bobot
        hoverinfo='text',  # Tampilkan informasi tooltip
        text=edge_labels,  # Isi tooltip dengan label edge
        mode='lines',
        name='Edges',
        textposition='middle center'  # Atur posisi teks label pada tengah edge
    )

    node_x = []
    node_y = []
    node_text = []  # Tambahkan list untuk menyimpan teks node (nama karakter atau genre)

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node} ({len(G[node])} edges)")  # Simpan teks node dengan jumlah edges

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',  # Menggunakan mode 'markers+text' untuk menampilkan teks di node
        hoverinfo='text',  # Tampilkan informasi tooltip
        text=node_text,  # Tambahkan teks nama node
        textposition='middle center',  # Atur posisi teks label pada tengah node
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=[10 + 2 * len(G[node]) for node in G],  # Sesuaikan ukuran node dengan degree centrality
            color=[random_color_hex() for node in G],  # Berikan warna acak pada setiap node
            colorbar=dict(
                thickness=15,
                title='Degree',
                xanchor='left',
                titleside='right'
            )
        ),
        name='Nodes',
        textfont=dict(color='white')  # Ubah warna teks nama node menjadi hitam
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        title="Graf Jaringan Sosial",
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    )
                    )

    # Tambahkan shapes untuk background pada nama node
    node_shapes = []
    for node in G.nodes():
        x, y = pos[node]
        node_shapes.append({
            'type': 'circle',
            'xref': 'x',
            'yref': 'y',
            'x0': x - 0.05,
            'y0': y - 0.05,
            'x1': x + 0.05,
            'y1': y + 0.05,
            'fillcolor': 'rgba(0, 0, 0, 0)',  # Atur latar belakang transparan
            'opacity': 1.0,  # Atur tingkat transparansi latar belakang
            'line': {
                'color': 'rgba(0, 0, 0, 0)'  # Hilangkan garis tepi
            }
        })

    fig.update_layout(shapes=node_shapes)

    st.plotly_chart(fig)

# Fungsi utama untuk analisis jaringan sosial
def social_network_analysis_csv(csv_file):
    data = pd.read_csv(csv_file)
    G = create_social_network_graph_csv(data)
    st.write("Informasi Jaringan Sosial:")
    st.write(f"Jumlah Node: {nx.number_of_nodes(G)}")
    st.write(f"Jumlah Edge: {nx.number_of_edges(G)}")
    st.write("\nTop 5 Node dengan Degree Tertinggi:")
    sorted_degrees = sorted(G.degree, key=lambda x: x[1], reverse=True)[:5]
    for node, degree in sorted_degrees:
        st.write(f"{node}: {degree}")
    st.write("\nGraf Jaringan Sosial:")
    draw_social_network_graph(G)

if __name__ == "__main__":
    csv_file = "c:/Users/HP/Desktop/tugas-moenawar-uas/jadi-gk-jadi/tugas_uas_moenawar_pasti/csv/anime.csv"
    st.title("Analisis Jaringan Sosial dengan Plotly")
    social_network_analysis_csv(csv_file)
    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
