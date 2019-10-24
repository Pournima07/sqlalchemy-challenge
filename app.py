from flask import Flask, jsonify
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect

app = Flask(__name__)

@app.route("/")
def Home():
    print(" server recd request from consumer")
    return(
            f"Welcome to Hawaii Climate App!<BR>"
            f"Available Routes:<br>"
            f"/api/v1.0/precipitation<br>"
            f"/api/v1.0/stations<br>"
            f"/api/v1.0/tobs<br>"
            f"api/v1.0/<start><br>"
            f"api/v1.0/<end><br>"
    )


@app.route("/precipitation")
def show_precip():
    print(" server recd request to show precipitation from consumer")

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)

    session = Session(engine)
    Measurement = Base.classes.measurement

    qry = session.query(Measurement).filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= '2016-08-23').all()

    dict = {}
    for m in qry:
        dict[m.date] = m.prcp

    return jsonify(dict)

@app.route("/stations")
def show_stations():
    print(" server recd request to show stations from consumer")

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)

    session = Session(engine)
    Measurement = Base.classes.measurement
    Station = Base.classes.station

    qry = session.query(Station.station, Station.name).all()

    
    dict = {}
    for stat in qry:
        dict [stat.station] = stat.name

    return jsonify (dict)

@app.route("/tobs")
def show_tobs():
    print(" server recd request to show tobs from consumer")

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)

    session = Session(engine)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = dt.datetime.strptime(last_date,'%Y-%m-%d')
    one_yr_back = dt.datetime(latest_date.year-1, latest_date.month, latest_date.day, 0, 0)

    print(f"Latest date is {latest_date}")
    print(f"one_yr_back is {one_yr_back}")
    
    
    one_yr_data = session.query(Measurement).filter(Measurement.date <= latest_date).filter(Measurement.date > one_yr_back)
    
    dict = {}
    for m in one_yr_data:
        dict[m.date] = m.tobs

    return jsonify(dict)

@app.route("/Temp/<start_date>")
def show_Temp(start_date):
    print(" server recd request to show temp from consumer")
    print (start_date)
    
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)

    session = Session(engine)
    Measurement = Base.classes.measurement
    # Station = Base.classes.station
    

    qry = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date)
    qry_data = qry.all()    

    return jsonify(qry_data)

@app.route("/Tempend/<start_date>/<end_date>")
def show_Tempend(start_date, end_date):
    print(" server recd request to show temp from consumer")
    print(start_date, end_date)
    
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)

    session = Session(engine)
    Measurement = Base.classes.measurement
    #Station = Base.classes.station

    qry = session.query(Measurement.station,func.sum(Measurement.prcp)).filter(Measurement.date <= end_date).\
        filter(Measurement.date >= start_date).group_by(Measurement.station)

    qry_data = qry.all()               
  
    return jsonify(qry_data)




# ##########################3

# @app.route("/")
# def Home():
#     Print(" server recd request from consumer")
#     return(
#             "Welcome to Hawaii Climate App!"
# )
# @app.route("/about")
# def about():
#     return(
#                 f "Available Routes:"
#                   "/api/v1.0/precipitation"
# )
          
# #Return a JSON list of stations from the dataset.
# dict = ({fill the info})
# @app.route('/jasonRoute')
# def jason(dict)
#     Print(" server recd about request from consumer")
#     return josonify ("/api/v1.0/stations")          

if __name__=="__main__":
    app.run(debug = False)