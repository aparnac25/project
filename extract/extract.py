#!/usr/bin/env python

"""
A package to parse a PDF for GPS coordinates (currently only DMS format), convert to decimal degrees, 
and plot to a map
"""

# packages to import
from tika import parser 
import pandas as pd 
import os
import re
import folium

#function to convert to decimal degrees
def decimaldegree(degree, minutes, seconds, hemisphere):
    """
    This function converts GPS coordinates in degrees, minutes, seconds 
    to decimal degrees
    """
    if hemisphere.lower() in ["w", "s", "west", "south"]:
        factor = -1.0
    elif hemisphere.lower() in ["n", "e", "north", "east"]:
        factor = 1.0
    else:
        raise ValueError("invalid hemisphere")

# check the order of operations in your code
    return factor * (float(degree) + float(minutes)/60 + float(seconds)/3600)

#define a function that will parse pdf, return coordinates, and return map and coordinates dataframe
def extract(pdf_path):
    """
    This function will parse the PDF into a string and from there it will extract 
    out gps coordiantes from the document and save a csv of GPS coordinates and 
    map 
    """
    # opening up PDF with tika parser
    parsed_pdf = parser.from_file(pdf_path)
    
    # saving content of PDF
    pdf_data = parsed_pdf['content'] 

    # get rid of all white space from parsed PDF
    cleaned_data = "".join(pdf_data.split())

    # pattern for gps coordinates
    pattern_1 = re.compile('''(\d{1,3}°\d{1,3}′\d{1,3}.\d{1,3}′′[A-Za-z],\d{1,3}°\d{1,3}′\d{1,3}.\d{1,3}′′[A-Za-z])''')
    pattern_2 = re.compile('''(\d{1,3}°\d{1,3}'[A-Za-z],\d{1,3}°\d{1,3}'[A-Za-z])''') 
    
    # match the pattern to the parsed data.
    gps_coords = pattern_1.findall(cleaned_data)
    
    # split list into latitude and longitude
    split_coords = []

    for elem in gps_coords:
        lst = elem.split(",")
        lst2 = [lst[0], lst[1]]
        split_coords.append(lst2)

    # convert dictionary to data frame 
    coords_df = pd.DataFrame(split_coords, columns=['Latitude', 'Longitude'])
    
    # split strings in data frame to degrees, minutes, seconds
    coords_df[['Lat_deg']] = coords_df['Latitude'].str.split("°").str[0]
    coords_df[['Lat_min']] = coords_df['Latitude'].str.split("°").str[1].str.split("′").str[0]
    coords_df[['Lat_sec']] = coords_df['Latitude'].str.split("′").str[1].str.split("′′").str[0]
    coords_df[['Lat_hem']] = coords_df['Latitude'].str.split("′′").str[1]
    coords_df[['Lon_deg']] = coords_df['Longitude'].str.split("°").str[0]
    coords_df[['Lon_min']] = coords_df['Longitude'].str.split("°").str[1].str.split("′").str[0]
    coords_df[['Lon_sec']] = coords_df['Longitude'].str.split("′").str[1].str.split("′′").str[0]
    coords_df[['Lon_hem']] = coords_df['Longitude'].str.split("′′").str[1]
    
    # apply that function along to rows, using lambda to specify the columns to use as input
    coords_df['Lat_dd'] = coords_df.apply(
        lambda row: decimaldegree(row['Lat_deg'], row['Lat_min'], row['Lat_sec'], row['Lat_hem']),
        axis=1, result_type='expand'
        )
    
    coords_df['Lon_dd'] = coords_df.apply(
        lambda row: decimaldegree(row['Lon_deg'], row['Lon_min'], row['Lon_sec'], row['Lon_hem']),
        axis=1, result_type='expand'
        )
    
    # plot the GPS points from coords_df
    # create the map
    pdf_map = folium.Map(coords_df[['Lat_dd', 'Lon_dd']].mean().values.tolist())
    
    # markers for points in map
    for lat, lon in zip(coords_df['Lat_dd'], coords_df['Lon_dd']):
        folium.Marker([lat, lon]).add_to(pdf_map)
    
    # constrain the map    
    sw = coords_df[['Lat_dd', 'Lon_dd']].min().values.tolist()
    ne = coords_df[['Lat_dd', 'Lon_dd']].max().values.tolist()
    pdf_map.fit_bounds([sw, ne]) 
    
    # display map
    display(pdf_map) # display doesnt work for command line interface ('show()' also doesn't work. No simple fix found), webbrowser python package!
        
    # save map
    pdfmapsavepath = os.path.realpath("../documents/pdf_map.html")
    pdf_map.save(pdfmapsavepath)
    
    # define path to user root for csv file of gps coordinates can save
    path = os.path.realpath("../documents/pdf_gps.csv")
    
    #save the csv
    coords_df.to_csv(path)
    

if __name__== '__main__':    
    extract(pdf_path)
    