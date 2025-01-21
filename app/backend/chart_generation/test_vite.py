import altair as alt
import json
from altair_saver import save

# Load the JSON spec
with open('bar_aggregate_count.vl.json', 'r') as file:
    spec = json.load(file)

# Create the chart from the spec
chart = alt.Chart.from_dict(spec)
chart.show()
# Save as PNG
#save(chart, 'chart.png')

chart.save('chart.html')
