import folium
from folium.plugins import MarkerCluster
import geopandas as gpd

# Generate base map
m = folium.Map(location=[60.4518, 22.2666], zoom_start=12, width="100%", height="90%")

# Import data
lintutornit = gpd.read_file('../data/raw/lintutornit.shp', crs='EPSG:3067').to_crs(epsg=4326)

# Add markers
mc = MarkerCluster().add_to(m)

for idx, torni in lintutornit.iterrows():
    # Create tooltip info
    tooltip_html = folium.Html(f"""
    <b>{torni['Paikka']}</b><br>
    Ympäristö: {torni['Ympäristö']}<br>
    Paras ajankohta: {torni['Paras_lint']}<br>
    Tornin korkeus (m): {torni['korkeus_m_']}<br>
    Kerrokset: {torni['tasot']}<br>
    Rakennusvuosi: {torni['rakennusv']}
    """, script=True)

    # Create marker and add to cluster
    folium.Marker([torni['geometry'].y, torni['geometry'].x], popup=folium.Popup(tooltip_html, parse_html=True, min_width=350, max_width=350)).add_to(mc) 

# Create output HTML
html_template = f"""
<!DOCTYPE html>
<html style="height: 100%;">
<head>
    <title>Varsinais-Suomen lintutornit kartalla</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body, html {{
            margin: 0;
            font-family: sans-serif;
        }}
        h1 {{
            text-align: center;
        }}
    </style>
</head>
<body>
    <h1>Varsinais-Suomen lintutornit kartalla</h1>
    <div>
        {m._repr_html_()}
    </div>
</body>
</html>
"""

# Save the modified HTML to a file
with open('../index.html', 'w', encoding='utf-8') as file:
    file.write(html_template)