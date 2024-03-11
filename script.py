import json
from datetime import datetime, timedelta
from random import randint

# Function to create TimeSeriesPoint objects
def create_timeseries_points(date, pk):
    return {
        "model": "gpts.timeseriespoint",
        "pk": pk,
        "fields": {
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "count": randint(100, 500)
        }
    }

# Generate 20 different dates
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(20)]

# Fixture data for views and upvotes
fixture_data = []

# Counter for unique IDs
timeseries_counter = 1
activity_summary_counter = 1

# GPT model ID
gpt_model_id = 2

# Generate fixture data for views and upvotes
for date in dates:
    views_data = create_timeseries_points(date, timeseries_counter)
    upvotes_data = create_timeseries_points(date, timeseries_counter + 1)
    
    fixture_data.append(views_data)
    fixture_data.append(upvotes_data)
    
    # Increment timeseries counter
    timeseries_counter += 2

# Fixture data for associating with ActivitySummary
activity_summary_data = {
    "model": "gpts.activitysummary",
    "pk": activity_summary_counter,
    "fields": {
        "id": gpt_model_id,
        "upvotes": list(range(2, 41, 2)),
        "views": list(range(1, 41, 2))
    }
}

fixture_data.append(activity_summary_data)

# Increment activity summary counter
activity_summary_counter += 1

# Dump fixture data to a file
with open("fixture.json", "w") as f:
    json.dump(fixture_data, f, indent=4)
