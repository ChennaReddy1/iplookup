from flask import Flask,render_template,request,redirect,url_for,session
import geoip2.database
from flask_wtf import FlaskForm
from wtforms import validators,StringField

app = Flask(__name__)
app.config['SECRET_KEY'] = "thisissecretkeyofiplocater"


@app.route('/', methods=["GET", "POST"])
def ipaddress_fun():
    error = ''
    try:

        if request.method == "POST":

            ipaddress = request.form['ipaddress']
            if ipaddress != None :
                reader = geoip2.database.Reader('./database/data.mmdb')
                response = reader.city(ipaddress)
                session['ipaddress'] = request.form['ipaddress']
                city = format(response.subdivisions.most_specific.name)
                iso = format(response.country.iso_code)
                siso = format(response.subdivisions.most_specific.iso_code)
                postal = format(response.postal.code)
                cityname = format(response.city.name)
                return render_template("table.html", ipaddress = ipaddress,city=city, iso=iso, siso=siso, postal=postal, cityname=cityname)

            else:
                error = "Invalid ipaddress. Try Again."
        return render_template("index.html", error=error)

    except Exception as e:
        return render_template("index.html", error=error)






if __name__ == "__main__" :
    app.run(debug=True)