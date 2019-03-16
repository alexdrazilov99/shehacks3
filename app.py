import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates", static_url_path='/static')
file=open("LongTermFixed.txt", "r")

stock_orig = []
date_orig = []

for line in file:
    line=file.readline()
    line=line.split()
    stock_orig.append(float(line[2].strip('"')))
    date_orig.append(line[1].strip('"'))

# Averaging/smoothing out data
numStock=len(stock_orig)
numIterations=numStock//15

stock_odd=stock_orig[:-1]
stock_even=stock_orig[:]

for i in range(1, numIterations):
    if i%2==1:
        for j in range(numStock-1):
            stock_odd[j]=(stock_even[j]+stock_even[j+1])/2
    else:
        stock_even[0]=stock_orig[0]
        for j in range(numStock-2):
            stock_even[j+1]=(stock_odd[j]+stock_odd[j+1])/2
        stock_even[-1]=stock_orig[-1]

#Slope calculations
numWeeks=5
somethingHappened=False
nextSteps=""

slope=[]

for i in range(numWeeks):
    slope.append((stock_even[-1*i]-stock_even[-1*(i+1)])/(i+1))

for i in range(numWeeks):
    slope.append((stock_even[-1*i]-stock_even[-1*(i+1)])/(i+1))

for i in range(numWeeks-1):
    if slope[i]>0 and slope[i+1]<=0:
        nextSteps="Buy now! Stocks have likely reached a minimum."
        somethingHappened=True
    elif slope[i]<=0 and slope[i+1]>0:
        nextSteps="Sell now! Stocks have likely reached a maximum."
        somethingHappened=True

if somethingHappened==False:
    if slope[-1]>0:
        nextSteps="Stocks going up, stay tuned."
    elif slope[-1]<0:
        nextSteps="Stocks going down, stay tuned."
    else:
        nextSteps="Stocks have plateaued, stay tuned."

@app.route('/')
def index():
    return render_template("index.html", nextSteps=nextSteps, data=stock_even, labels=date_orig)


if __name__ == "__main__":
    app.run(debug=True)
