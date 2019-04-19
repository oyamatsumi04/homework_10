#dependencies
from flask import Flask, jsonify
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#setup
engine = create_engine("sqlite:///hawaii.sqlite")

#initialize
app = Flask(__name__)

#import data
measurements = pd.DataFrame(pd.read_csv("hawaii_measurements.csv"))
stations = pd.DataFrame(pd.read_csv("hawaii_stations.csv"))

# isolate date and precipitation, convert to dict to prepare for delivery
prcp = measurements[['date', 'prcp']].set_index('date').to_dict()

# convert station dataframe to dictionary
stat = stations.to_dict(orient='index')

# convert temperature information to dictionary
temp = measurements[['date', 'tobs']].set_index('date').to_dict()

# convert date field in measurements to make searchable
new_measurements = measurements
new_measurements.date = new_measurements.date.map(lambda x: x.replace("-", "")).astype(int)

@app.route("/api/v1.0")
def index():
    return "Home."

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp['prcp'])

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def start(start):
    start = int(start.replace('-', ''))
    end = new_measurements.date.max()
    subset_meas = new_measurements[(new_measurements.date >= start) & (new_measurements.date <= end)]
    max_temp = subset_meas.tobs.max()
    min_temp = subset_meas.tobs.min()
    avg_temp = subset_meas.tobs.mean()
    print('For date range selected, the expected high is', max_temp, 'the expected low is', min_temp, 'the average is', avg_temp)
    return jsonify({'Max': str(max_temp),
                    'Min': str(min_temp),
                    'Avg': str(avg_temp)})

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start = int(start.replace('-', ''))
    end = int(end.replace('-', ''))
    subset_meas = new_measurements[(new_measurements.date >= start) & (new_measurements.date <= end)]
    max_temp = subset_meas.tobs.max()
    min_temp = subset_meas.tobs.min()
    avg_temp = subset_meas.tobs.mean()
    return jsonify({"Maximum Temperature": str(max_temp),
                    "Minimum Temperature": str(min_temp),
                    "Average Temperature": str(avg_temp)})



if __name__ == "__main__":
    app.run(debug=True)