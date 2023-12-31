import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
def gen_heatmap(data):
    center_lat, center_long = data['Latitude'].mean(), data['Longitude'].mean()
    mymap = folium.Map(location=[center_lat, center_long], zoom_start=15)

    # Add HeatMap layer to the map
    heat_data = list(zip(data['Latitude'], data['Longitude'], data['PRED_CT']))
    folium.TileLayer('cartodbpositron').add_to(mymap)
    folium.TileLayer('openstreetmap').add_to(mymap)
    HeatMap(heat_data).add_to(mymap)
    # Create a MarkerCluster layer
    marker_cluster = MarkerCluster().add_to(mymap)
    # Add individual markers to the cluster layer
    for lat, lon, count in heat_data:
        folium.Marker([lat, lon], tooltip=f'Plastic Count: {count}').add_to(marker_cluster)
    # legend creation
    legend_html = f'''
    <div style="position: fixed;
                top: 10px; left: 10px; width: 150px; height: 100px;
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color: white;
                ">
    &nbsp; Plastic Count Legend <br>
    &nbsp; <div style="width: 20px; height: 20px; background-color: red; display: inline-block;border: 1px solid black; border-radius: 20px"></div> : High Plastic<br>
    &nbsp; <div style="width: 20px; height: 20px; background-color: orange; display: inline-block;border: 1px solid black; border-radius: 20px"></div> : Mid Plastic<br>
    &nbsp; <div style="width: 20px; height: 20px; background-color: green; display: inline-block;border: 1px solid black; border-radius: 20px"></div> : Low Plastic
    </div>
    '''

    mymap.get_root().html.add_child(folium.Element(legend_html))
    #   folium.LayerControl().add_to(mymap)
    #   mid_count = (min(data['PRED_CT']) + max(data['PRED_CT'])) / 2
    #   legend_html = f'''
    #  <div style="position: fixed;
    #              bottom: 50px; left: 50px; width: 150px; height: 100px;
    #              border:2px solid grey; z-index:9999; font-size:14px;
    #              background-color: white;
    #              ">
    #  &nbsp; Plastic Count Legend <br>
    #  &nbsp; Low Plastic: &lt; {mid_count} <i style="background:{'green'};opacity:0.7;"></i><br>
    #  &nbsp; High Plastic: &gt;= {mid_count} <i style="background:{'red'};opacity:0.7;"></i>
    #   </div>
    #  '''
    #   mymap.get_root().html.add_child(folium.Element(legend_html))

    #   # Add tooltip to show plastic count and color indication on hover
    #   for lat, lon, count in heat_data:
    #       color_indication = "High Plastic" if count >= mid_count else "Low Plastic"
    #       folium.Marker([lat, lon], tooltip=f'Plastic Count: {count}, Color: {color_indication}').add_to(mymap)

    # Save the map as an HTML file
    mymap.save('templates/heatmap_plastic.html')
    print("heatmap written to heatmap_plastic.html")  