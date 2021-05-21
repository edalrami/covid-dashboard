# covid-dashboard
This repo contains the files needed to create the plotly dashboard found on https://edalrami-covid-dash.herokuapp.com/
The original files used for development were `VaccineVisualizations.html` and `VaccineVisualizations.ipynb` before being
reformatted into the necessary format for a dash application in `app.py` and `plots.py`. The reason why I primarily decided
to utilize plotly and dash for this project was because I wanted to create a visual story that was dynamic in its nature,
and could summarize the effects of the vaccinations on the death/case counts in every state along with a general overview 
of the entire US. Plotly provided better control over the specifics of the visuals and allowed me to create a basic story
that is interactive for the most part. If one of the visuals doesn't update it's simply because there wasn't data provided. 
I put this dashboard together rather quickly, but in the future it will have callbacks that display warnings/error messages to
null or missing data. **The html file won't always render in github so I highly recommend downloading `VaccineVisualizations.html`**.
This will allow you to see the sample visuals I made in context with my report, and have a better understadning of the dashboard as well.


- **Covid-19 Vaccinations Data US**: Data Folder
- **assets**: folder containing CSS styling files for app.py
- **VaccineVisualizations.html**: HTML render of Jupyter Notebook report
- **VaccineVisualizations.ipynb**: Jupyter Notebook where I summarize my findings and created the functions that generated plotly graph_objects used in the dash app
- **app.py**: Main application framework file. Run `python app.py` if you want to run it locally. Otherwise visit https://edalrami-covid-dash.herokuapp.com/ to see it live
- **plots.py**: Python script with all plot generation functions
- **requirements.txt**: Dash Application dependencies



