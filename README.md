# `extract`

`extract` is a Python package that parses through a PDF and find GPS coordiantes. This pacakge will extract out GPS coordinates, convert them to decimal degree format and then plot them to an interactive map. In addition, a csv file of the GPS coordiantes will be outputed and saved to the This program will accomplish three things: (1) read a PDF and extract sample location names and GPS coordinates; (2) convert to decimal deggrees format, and (3) plot converted coordinates to a map. 

---
## In development 

The following packages are needed to run the extract package: 

-``tika`` Java version 7 is needed

-``pandas``

-``re``

-``os``

-``follium`` 

To install the following pacakges use 

```
conda install tika pandas re os follium
```

To contribute to the development of `extract`, you can clone this repository using the follwoing commands: 

```
git clone git@github.com:aparnac25/extract.git
cd ./extract
```

### Minimal Working Example

To play around with the code open notebooks/extract-dev.ipynb. To open: 

```
jupyter notebook --no-browser
```

and type in local host address into browser of choice

### Currently not working 

Currently the `pip install` is not working. Hopefully soon one can use below code to run on command line in the future.

```
cd ./extract
pip install -e .
```



