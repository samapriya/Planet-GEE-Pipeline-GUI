# Planet GEE Pipeline GUI

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.817610.svg)](https://doi.org/10.5281/zenodo.817610)
[![JetStream](https://img.shields.io/badge/SupportedBy%3A-JetStream-brightgreen.svg)](https://jetstream-cloud.org/)
[![Planet](https://img.shields.io/badge/SupportedBy%3A-Planet%20Ambassador%20Program-brightgreen.svg)](https://www.planet.com/products/education-and-research/)

The Planet Pipeline GUI came from the actual CLI (command line interface tools) to enable the use of tools required to access control and download planet labs assets (PlanetScope and RapidEye OrthoTiles) as well as parse metadata in a tabular form which maybe required by other applications.

![GUI](http://i.imgur.com/ld9xJu6.gif)
## Table of contents
* [Installation](#installation)
* [Usage examples](#usage-examples)
* [Planet Tools](#planet-tools)
	* [Planet Key](#planet-key)
    * [AOI JSON](#aoi-json)
    * [Activate or Check Asset](#activate-or-check-asset)
    * [Download Asset](#download-asset)
    * [Metadata Parser](#metadata-parser)
* [Earth Engine Tools](#earth-engine-tools)
	* [EE User](#ee-user)
	* [Create](#create)
    * [Upload a directory with images and associate properties with each image:](#upload-a-directory-with-images-and-associate-properties-with-each-image)
	* [Upload a directory with images with specific NoData value to a selected destination:](#upload-a-directory-with-images-with-specific-nodata-value-to-a-selected-destination)
	* [Task Query](#task-query)
	* [Task Query during ingestion](#task-query-during-ingestion)
	* [Task Report](#task-report)
    * [Delete a collection with content:](#delete-a-collection-with-content)
	* [Assets Move](#assets-move)
	* [Assets Copy](#assets-copy)
	* [Assets Access](#assets-access)
	* [Set Collection Property](#set-collection-property)
	* [Convert to Fusion Table](#convert-to-fusion-table)
	* [Cleanup Utility](#cleanup-utility)
	* [Cancel all tasks](#cancel-all-tasks)
* [Credits](#credits)
## Installation
We assume Earth Engine Python API is installed and EE authorised as desribed [here](https://developers.google.com/earth-engine/python_install). We also assume Planet Python API is installed you can install by simply running 
```
pip install planet
```
Further instructions can be found [here](https://www.planet.com/docs/api-quickstart-examples/cli/) 

You require two important packages for this to run
```
WxPython(which is what the GUI is built on)
for windows(Tested in Windows 10)
https://wxpython.org/download.php
pip install wxPython

for linux(Tested in Ubuntu 16)
sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu utopic main restricted universe"  
sudo apt-get update
apt-cache search python-wxgtk3.0
sudo apt-get install python-wxgtk3.0
```
This toolbox also uses some functionality from GDAL
For installing GDAL in Ubuntu
```
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install gdal-bin
```
For Windows I found this [guide](https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows) from UCLA

## Usage examples
Usage examples have been segmented into two parts focusing on both planet tools as well as earth engine tools, earth engine tools include additional developments in CLI which allows you to recursively interact with their python API. To run the tool open a command prompt window or terminal and type

```
python ee_ppipe.py
```
For windows user there is now a whole executable that you can double click and start in the folder windows executable. This tool does not require admin privileges since I created this for use by everyone.

## Planet Tools
The Planet Toolsets consists of tools required to access control and download planet labs assets (PlanetScope and RapidEye OrthoTiles) as well as parse metadata in a tabular form which maybe required by other applications.

### Planet Key
This tool basically asks you to input your Planet API Key using a password prompt this is then used for all subsequent tools

![planet_key](http://i.imgur.com/tv3FENS.gif)

If using on a private machine the Key is saved as a csv file for all future runs of the tool.
 
### AOI JSON
The aoijson tab within the toolset allows you to create filters and structure your existing input file to that which can be used with Planet's API. The tool requires inputs with start and end date, along with cloud cover. You can choose from multiple input files types such as KML, Zipped Shapefile, GeoJSON, WKT or even Landsat Tiles based on PathRow numbers. The geo option asks you to select existing files which will be converted into formatted JSON file called aoi.json. If using WRS as an option just type in the 6 digit PathRow combination and it will create a json file for you.

![aoijson](http://i.imgur.com/1lLXKDP.gif)

### Activate or Check Asset
The activatepl tab allows the users to either check or activate planet assets, in this case only PSOrthoTile and REOrthoTile are supported because I was only interested in these two asset types for my work but can be easily extended to other asset types. This tool makes use of an existing json file sturctured for use within Planet API or the aoi.json file created earlier

![activatepl](http://i.imgur.com/n2rdw6M.gif)

### Download Asset
Having metadata helps in organising your asstets, but is not mandatory - you can skip it.
The downloadpl tab allows the users to download assets. The platform can download Asset or Asset_XML which is the metadata file to desired folders.One again I was only interested in these two asset types(PSOrthoTile and REOrthoTile) for my work but can be easily extended to other asset types.

![downloadpl](http://i.imgur.com/muFYdqo.jpg)

### Metadata Parser
The metadata tab is a more powerful tool and consists of metadata parsing for PlanetScope OrthoTile RapiEye OrthoTile along with Digital Globe MultiSpectral and DigitalGlobe PanChromatic datasets. This was developed as a standalone to process xml metadata files from multiple sources and is important step is the user plans to upload these assets to Google Earth Engine. The combine Planet-GEE Pipeline tool will be made available soon for testing.

![metadata](http://i.imgur.com/lpYPrSv.jpg)

##Earth Engine Tools
The ambition is apart from helping user with batch actions on assets along with interacting and extending capabilities of existing GEE CLI. It is developed case by case basis to include more features in the future as it becomes available or as need arises. This is also a seperate package for earth engine users to use and can be downloaded [here](https://github.com/samapriya/gee_asset_manager_addon)

### EE User
This tool is designed to allow different users to change earth engine authentication credentials. The tool invokes the authentication call and copies the authentication key verification website to the clipboard which can then be pasted onto a browser and the generated key can be pasted back
![eeuser](http://i.imgur.com/LkMIZuc.jpg)

### Create
This tool allows you to create a collection or folder in your earth engine root directory. The tool uses the system cli to achieve this and this has been included so as to reduce the need to switch between multiple tools and CLI.
![create](http://i.imgur.com/BCyCyUj.png)			   

### Upload a directory with images to your myfolder/mycollection and associate properties with each image:

![upload](http://i.imgur.com/O7jgpBV.jpg)

The script will prompt the user for Google account password. The program will also check that all properties in path_to_metadata.csv do not contain any illegal characters for GEE. Don't need metadata? Simply skip this option.

### Task Query
This script counts all currently running and ready tasks along with failed tasks.

![taskquery](http://i.imgur.com/tnEJS5h.jpg)

### Task Query during ingestion
This script can be used intermittently to look at running, failed and ready(waiting) tasks during ingestion. This script is a special case using query tasks only when uploading assets to collection by providing collection pathway to see how collection size increases.

![taskquery_ingestion](http://i.imgur.com/XX17Yvn.jpg)

	
### Task Report
Sometimes it is important to generate a report based on all tasks that is running or has finished. Generated report includes taskId, data time, task status and type

![taskreport](http://i.imgur.com/lcllphp.jpg)

### Delete a collection with content:

The delete is recursive, meaning it will delete also all children assets: images, collections and folders. Use with caution!

![delete](http://i.imgur.com/WESpx2O.jpg)

### Assets Move
This script allows us to recursively move assets from one collection to the other.

![assets-move](http://i.imgur.com/Wprb0wA.jpg)

### Assets Copy
This script allows us to recursively copy assets from one collection to the other. If you have read acess to assets from another user this will also allow you to copy assets from their collections.

![assets-copy](http://i.imgur.com/4DYfu9x.jpg)

### Assets Access
This tool allows you to set asset acess for either folder , collection or image recursively meaning you can add collection access properties for multiple assets at the same time.

![assets-access](http://i.imgur.com/t0ncujT.jpg)

### Set Collection Property
This script is derived from the ee tool to set collection properties and will set overall properties for collection. 

![collectionprop](http://i.imgur.com/nIhw4DC.jpg)


### Convert to Fusion Table
Once validated with gdal and google fusion table it can be used to convert any geoObject to google fusion table. Forked and contributed by Gennadii [here](https://github.com/gena/ogr2ft). The scripts can be used only with a specific google account

![ogrft](http://i.imgur.com/frRaQuZ.jpg)

### Cleanup Utility
This script is used to clean folders once all processes have been completed. In short this is a function to clear folder on local machine.

![cleanup](http://i.imgur.com/WOVzk3A.jpg)

### Cancel all tasks
This is a simpler tool, can be called directly from the earthengine cli as well

![cancel](http://i.imgur.com/bTT9vRI.jpg)


# Credits
[JetStream](https://jetstream-cloud.org/) A portion of the work is suported by JetStream Grant TG-GEO160014.

Also supported by [Planet Labs Ambassador Program](https://www.planet.com/markets/ambassador-signup/)
