from flask import Flask,render_template,request, redirect
import urllib2
import json
import numpy              as np
import pandas             as pd
from bokeh.plotting import figure, show, output_server
from bokeh.embed import components
#import matplotlib.pyplot  as plt

app = Flask(__name__)

app.vars={}
ticker = 'XXXX'

@app.route('/index_page',methods=['GET','POST'])
def index_page():
    if request.method == 'GET':
        return render_template('getTicker.html')
    else:
        #request was a POST        
        #app.vars['ticker'] = request.form['ticker_symbol']
        global ticker
        ticker  =  request.form['ticker_symbol']
		
        #f = open('ticker_choice.txt','w')
     	#f.write('Name: %s\n'%(app.vars['ticker']))
        #f.close()
		
        return redirect('/get_quandl_data')
    #return ticker
	
@app.route('/get_quandl_data')
def quandl_search():
  api_key = '/data.csv?api_key=7JMJ6VpnxSDZXi_iJmUj' 
  url = 'https://www.quandl.com/api/v3/datasets/WIKI/'
        
  try:      
    data = urllib2.urlopen("%s%s%s" % (url, ticker, api_key)).read()
    fc = open('temp_file.csv' , 'w')
    fc.write(data)
    fc.close()
 
    es = pd.read_csv('temp_file.csv', parse_dates=['Date'])
    ticker_close = np.array(es['Close'])
    ticker_volum = np.array(es['Volume'])
    ticker_dates = np.array(es['Date'], dtype=np.datetime64)
  
    window_size = 30
    window = np.ones(window_size)/float(window_size)
    ticker_close_avg = np.convolve(ticker_close, window, 'same')
    ticker_volum_avg = np.convolve(ticker_volum, window, 'same')

  #  output_file("stocks.html", title="Day 8 Task")
  #  output_notebook()
    TOOLS = 'pan, wheel_zoom, resize, reset'
# Create a new plot
    p = figure(tools=TOOLS, width=800, height=350, x_axis_type="datetime")

# add renderers
    p.circle(ticker_dates, ticker_close, size=4, color='darkgrey', alpha=0.2, legend='close')
    p.line(ticker_dates, ticker_close_avg, color='navy', legend='avg')

# Set Attributes
    p.title = "%s One-Month Average" % (ticker)
    p.legend.location = "top_left"
    p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'

    show(p)

    script, div = components(p)
    return render_template('graph.html', script=script, div=div)
  
  except urllib2.HTTPError, err:
    if err.code == 404:
      print "This symbol is not avaiable on Quandl Wiki"
    else:
      print "Oops!! Something is wrong ... sorry"
	  
	
if __name__ == "__main__":
    app.run(debug=True)