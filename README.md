# Investigating Relationships Between Variables of Education and Affluence
In this project, I took World Bank data, ran some statistical analysis on it, and visualized it to investigate how educational variables
are related to national well-being. This was the final project I devloped for my visualization class.
You can read about the details in the report, watch the demo video, or try the software yourself!

The data processing is done in Python, the server is built on Flask, and the visualization is built on D3.js.

To run the server, simply run `python app.py` in the `app` folder.

## Data Source
http://data.worldbank.org/indicator

## Some fair notices
- You'll notice some correlations are > 1. This is clearly wrong, so keep in mind some calculations are flawed.
However, the relative strengths of the correlations seem to be accurate.
- MDS stands for Multi-Dimensional Scaling, a technique used to show relative multi-dimensional distance between variables.
- The data points are colored by cluster.
