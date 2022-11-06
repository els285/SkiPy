import geojson
import geopandas
df = geopandas.read_file("export.geojson")

# print(df["properties"].to_string())
# exit()
# print(df[df["piste:name"]!=None])
with open("export.geojson") as f:
    gj = geojson.load(f)
features = gj['features']

named_pistes = {}
for f in features:
    if "name" in f["properties"] and f["properties"]["piste:type"]=="downhill":
        named_pistes[f["properties"]["name"]] = f
# print((named_pistes).keys()))
print(len(named_pistes))
# print(named_pistes["Borsat"])