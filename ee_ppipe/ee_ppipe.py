#! /usr/bin/env python

import argparse
import logging
import os
import ee
import subprocess
from gooey import Gooey, GooeyParser
from gooey import GooeyParser
from batch_copy import copy
from batch_remover import delete
from batch_uploading import upload
from config import setup_logging
from message import display_message
from query import taskquery
from batch_mover import mover
from cleanup import cleanout
from collectionprop import collprop
from taskreport import genreport
from acl_changer import access
from cli_aoi2json import aoijson
from cli_metadata import metadata
from ee_ls import lst
import getpass
import csv
from ee import oauth
import re
import time
import clipboard

def planet_key_entry():
    print("Enter your Planet API Key")
    password=getpass.getpass()
    with open('./pkey.csv','w') as completed:
        writer=csv.writer(completed,delimiter=',',lineterminator='\n')
        writer.writerow([password]) 
def planet_key_from_parser(args):
    planet_key_entry()
def ee_auth_entry():
    auth_url = ee.oauth.get_authorization_url()
    clipboard.copy(auth_url)
    print("Authentication link copied: Go to browser and click paste")
    time.sleep(10)
    print("Enter your GEE API Token")
    password=str(getpass.getpass())
    auth_code=str(password)
    token = ee.oauth.request_token(auth_code)
    ee.oauth.write_token(token)
    print('\nSuccessfully saved authorization token.')
def ee_user_from_parser(args):
    ee_auth_entry()
def create_from_parser(args):
    typ=str(args.typ)
    ee_path=str(args.path)
    os.system("earthengine create "+typ+" "+ee_path)
def aoijson_from_parser(args):
    aoijson(start=args.start,end=args.end,cloud=args.cloud,inputfile=args.inputfile,geo=args.geo,loc=args.loc)
def metadata_from_parser(args):
    metadata(asset=args.asset,mf=args.mf,mfile=args.mfile,errorlog=args.errorlog)

def activatepl_from_parser(args):
    aoi_json=str(args.aoi)
    action_planet=str(args.action)
    asset_type=str(args.asst)
    try:
        os.system("python download.py --query "+args.aoi+" --"+args.action+" "+args.asst)
    except Exception:
        print(' ')
def downloadpl_from_parser(args):
    aoi_json=str(args.aoi)
    action_planet=str(args.action)
    planet_pathway=str(args.pathway)
    asset_type=str(args.asst)
    try:
        os.system("python download.py --query "+args.aoi+" --"+args.action+" "+args.pathway+" "+asset_type)
    except Exception:
        print(' ')
        
def cancel_all_running_tasks():
    logging.info('Attempting to cancel all running tasks')
    running_tasks = [task for task in ee.data.getTaskList() if task['state'] == 'RUNNING']
    for task in running_tasks:
        ee.data.cancelTask(task['id'])
    logging.info('Cancel all request completed')

def cancel_all_running_tasks_from_parser(args):
    cancel_all_running_tasks()
	
def delete_collection_from_parser(args):
    delete(args.id)

def upload_from_parser(args):
    upload(user=args.user,
    source_path=args.source,
    destination_path=args.dest,
    metadata_path=args.metadata,
    nodata_value=args.nodata)
def ft_from_parser(args):
    input_file=str(args.i)
    output_ft=str(args.o)
    os.system("ogr2ft.py -i "+input_file+" -o "+output_ft)
def taskquery_from_parser(args):
    taskquery(destination=args.destination)
def mover_from_parser(args):
	mover(assetpath=args.assetpath,destinationpath=args.finalpath)
def copy_from_parser(args):
	copy(initial=args.initial,final=args.final)
def access_from_parser(args):
	copy(mode=args.mode,asset=args.asset,user=args.user)
def cleanout_from_parser(args):
    cleanout(args.dirpath)
def tasks():
    tasklist=subprocess.check_output("earthengine task list",shell=True)
    taskready=tasklist.count("READY")
    taskrunning=tasklist.count("RUNNING")
    taskfailed=tasklist.count("FAILED")
    print("Running Tasks:",taskrunning)
    print("Ready Tasks:",taskready)
    print("Failed Tasks:",taskfailed)
def tasks_from_parser(args):
    tasks()
def genreport_from_parser(args):
    genreport(report=args.r)
def collprop_from_parser(args):
    collprop(imcoll=args.coll,prop=args.p)
def lst_from_parser(args):
    lst(location=args.location,typ=args.type,items=args.items,f=args.folder)
spacing="                               "
from gooey import Gooey, GooeyParser
@Gooey(dump_build_config=True, program_name="Planet and EE Pipeline")
def main(args=None):
    setup_logging()
    parser = GooeyParser(description='Planet and EE Pipeline')
    subparsers = parser.add_subparsers()
    ##Planet Assets Tools
    parser_planet_key = subparsers.add_parser('planet_key', help='Enter your planet API Key')
    parser_planet_key.set_defaults(func=planet_key_from_parser)
    
    parser_aoijson=subparsers.add_parser('aoijson',help='Convert KML/SHP/WKT/GeoJSON file to aoi.json file with structured query for use with Planet API 1.0')
    parser_aoijson.add_argument('--start', default='Start date in YYYY-MM-DD',help='Start date in YYYY-MM-DD?',widget='DateChooser')
    parser_aoijson.add_argument('--end', default='End date in YYYY-MM-DD',help='End date in YYYY-MM-DD?',widget='DateChooser')
    parser_aoijson.add_argument('--cloud', default='Maximum Cloud Cover(0-1)',help='Maximum Cloud Cover(0-1) representing 0-100')
    parser_aoijson.add_argument('--inputfile',default='Choose a KML/SHP/geojson/WKT file or Landsat WRS',choices=['KML', 'SHP','GJSON','WKT','WRS'],help='Choose a KML/SHP/geojson/WKT file or Landsat WRS')
    parser_aoijson.add_argument('--geo', default='map.geojson/aoi.kml/aoi.shp/aoi.wkt file or 6 digit WRS PathRow',help='map.geojson/aoi.kml/aoi.shp/aoi.wkt file',widget="MultiFileChooser")
    parser_aoijson.add_argument('--loc', help='Location where aoi.json file is to be stored',widget="MultiDirChooser")
    parser_aoijson.set_defaults(func=aoijson_from_parser)

    parser_activatepl=subparsers.add_parser('activatepl',description='Tool to query and/or activate Planet Assets')
    parser_activatepl.add_argument('--aoi',default='Choose JSON file to be used with Planet API/Created Earlier',help='Choose JSON file created earlier',widget="MultiFileChooser")
    parser_activatepl.add_argument('--action',choices=['check', 'activate'],help='Check/activate')
    parser_activatepl.add_argument('--asst',choices=['PSOrthoTile analytic','PSOrthoTile analytic_dn','PSOrthoTile visual','PSScene4Band analytic','PSScene4Band analytic_dn','PSScene3Band analytic','PSScene3Band analytic_dn','PSScene3Band visual','REOrthoTile analytic','REOrthoTile visual'],help='PSOrthoTile analytic,PSOrthoTile analytic_dn,PSOrthoTile visual,PSScene4Band analytic,PSScene4Band analytic_dn,PSScene3Band analytic,PSScene3Band analytic_dn,PSScene3Band visual,REOrthoTile analytic,REOrthoTile visual')
    parser_activatepl.set_defaults(func=activatepl_from_parser)

    parser_downloadpl=subparsers.add_parser('downloadpl',help='Tool to download Planet Assets')
    parser_downloadpl.add_argument('--aoi', default='Choose JSON file to be used with Planet API/Created Earlier',help='Choose JSON file created earlier',widget="MultiFileChooser")
    parser_downloadpl.add_argument('--action', default='download',help='choose download')
    parser_downloadpl.add_argument('--asst',choices=['PSOrthoTile analytic','PSOrthoTile analytic_dn','PSOrthoTile visual','PSScene4Band analytic','PSScene4Band analytic_dn','PSScene3Band analytic','PSScene3Band analytic_dn','PSScene3Band visual','REOrthoTile analytic','REOrthoTile visual','PSOrthoTile analytic_xml','PSOrthoTile analytic_dn_xml','PSOrthoTile visual_xml','PSScene4Band analytic_xml','PSScene4Band analytic_dn_xml','PSScene3Band analytic_xml','PSScene3Band analytic_dn_xml','PSScene3Band visual_xml','REOrthoTile analytic_xml','REOrthoTile visual_xml'],help='PSOrthoTile analytic,PSOrthoTile analytic_dn,PSOrthoTile visual,PSScene4Band analytic,PSScene4Band analytic_dn,PSScene3Band analytic,PSScene3Band analytic_dn,PSScene3Band visual,REOrthoTile analytic,REOrthoTile visual')
    parser_downloadpl.add_argument('--pathway',default='Folder where you want to save assets',help='Folder Path where PlanetAssets are saved example ./PlanetScope ./RapidEye',widget="MultiDirChooser")
    parser_downloadpl.set_defaults(func=downloadpl_from_parser)

    parser_metadata=subparsers.add_parser('metadata',help='Tool to tabulate and convert all metadata files from Planet or Digital Globe Assets')
    parser_metadata.add_argument('--asset', default='PS',choices=['PSO','PSO_DN','PSO_V','PS4B','PS4B_DN','PS3B','PS3B_DN','PS3B_V','REO','REO_V','DGMS','DGP'],help='RapidEye/PlantScope/DigitalGlobe MS/DigitalGlobe Pan(RE/PS/DGMS/DGP)?')
    parser_metadata.add_argument('--mf', default='Metadata folder',help='Metadata folder',widget="MultiDirChooser")
    parser_metadata.add_argument('--mfile',default='Metadata filename browse and create file and click open',help='Metadata filename to be exported with Path.csv',widget="MultiFileChooser")
    parser_metadata.add_argument('--errorlog',default='Error log browse and create file and click open',help='Errorlog to be exported along with Path.csv',widget="MultiFileChooser")
    parser_metadata.set_defaults(func=metadata_from_parser)

    ##Earth Engine Tools
    parser_ee_user = subparsers.add_parser('ee_user', help='Get Earth Engine API Key & Paste it back to Command line/shell to change user')
    parser_ee_user.set_defaults(func=ee_user_from_parser)

    parser_create = subparsers.add_parser('create',help='Allows the user to create an asset collection or folder in Google Earth Engine')
    parser_create.add_argument('--typ', help='Specify type: collection or folder', required=True)
    parser_create.add_argument('--path', help='This is the path for the earth engine asset to be created full path is needsed eg: users/johndoe/collection', required=True)
    parser_create.set_defaults(func=create_from_parser)
    
    parser_upload = subparsers.add_parser('upload', help='Batch Asset Uploader to Earth Engine.')
    required_named = parser_upload.add_argument_group('Required named arguments.')
    required_named.add_argument('-u', '--user', help='Google account name (gmail address).', required=True)
    required_named.add_argument('--source', help='Path to the directory with images for upload.', required=True)
    required_named.add_argument('--dest', help='Destination. Full path for upload to Google Earth Engine, e.g. users/pinkiepie/myponycollection', required=True)
    optional_named = parser_upload.add_argument_group('Optional named arguments')
    optional_named.add_argument('-m', '--metadata', help='Path to CSV with metadata.')
    optional_named.add_argument('--nodata', type=int, help='The value to burn into the raster as NoData (missing data)')
    parser_upload.set_defaults(func=upload_from_parser)

    parser_lst = subparsers.add_parser('lst',help='List assets in a folder/collection or write as text file')
    parser_lst.add_argument('--location', help='This it the location of your folder/collection', required=True)
    parser_lst.add_argument('--type', help='Whether you want the list to be printed or output as text', required=True)
    parser_lst.add_argument('--items', help="Number of items to list")
    parser_lst.add_argument('--folder',help="Folder location for report to be exported")
    parser_lst.set_defaults(func=lst_from_parser)

    parser_tasks=subparsers.add_parser('tasks',help='Queries currently running, enqued,failed')
    parser_tasks.set_defaults(func=tasks_from_parser)
    
    parser_taskquery=subparsers.add_parser('taskquery',help='Queries currently running, enqued,failed ingestions and uploaded assets')
    parser_taskquery.add_argument('--destination',default='users/folder/collection',help='Full path to asset where you are uploading files')
    parser_taskquery.set_defaults(func=taskquery_from_parser)

    parser_genreport=subparsers.add_parser('report',help='Create a report of all tasks and exports to a CSV file')
    parser_genreport.add_argument('--r',default='Folder Path where the reports will be saved',help='Folder Path where the reports will be saved',widget="MultiDirChooser")
    parser_genreport.set_defaults(func=genreport_from_parser)

    parser_cancel = subparsers.add_parser('cancel', help='Cancel all running tasks')
    parser_cancel.set_defaults(func=cancel_all_running_tasks_from_parser)
    
    parser_mover=subparsers.add_parser('mover',help='Moves all assets from one collection to another')
    parser_mover.add_argument('--assetpath',default='users/folder/collection1',help='Existing path of assets')
    parser_mover.add_argument('--finalpath',default='users/folder/collection2',help='New path for assets')
    parser_mover.set_defaults(func=mover_from_parser)

    parser_copy=subparsers.add_parser('copy',help='Copies all assets from one collection to another: Including copying from other users if you have read permission to their assets')
    parser_copy.add_argument('--initial',default='users/folder/collection1',help='Existing path of assets')
    parser_copy.add_argument('--final',default='users/folder/collection2',help='New path for assets')
    parser_copy.set_defaults(func=copy_from_parser)

    parser_collprop=subparsers.add_parser('collprop',help='Sets Overall Properties for Image Collection')
    parser_collprop.add_argument('--coll',default='users/folder/collection',help='Path of Image Collection')
    parser_collprop.add_argument('--p',default='system:description=Description',help='system:description=Description|system:title=title')
    parser_collprop.set_defaults(func=collprop_from_parser)
    
    parser_ft = subparsers.add_parser('access',help='Sets Permissions for Images, Collection or all assets in EE Folder Example: python ee_permissions.py --mode "folder" --asset "users/john/doe" --user "jimmy@doe.com:R"')
    parser_ft.add_argument('--mode', default='folder|collection|image',choices=['folder','collection','image'],help='This lets you select if you want to change permission or folder/collection/image', required=True)
    parser_ft.add_argument('--asset', default='users/folder/collection',help='This is the path to the earth engine asset whose permission you are changing folder/collection/image', required=True)
    parser_ft.add_argument('--user', default='john@doe.com:R',help="""This is the email address to whom you want to give read or write permission Usage: "john@doe.com:R" or "john@doe.com:W" R/W refers to read or write permission""", required=True)
    parser_ft.set_defaults(func=access_from_parser)

    parser_delete = subparsers.add_parser('delete', help='Deletes collection and all items inside. Supports Unix-like wildcards.')
    parser_delete.add_argument('id', default='users/folder/collection',help='Full path to asset for deletion. Recursively removes all folders, collections and images.')
    parser_delete.set_defaults(func=delete_collection_from_parser)
    
    parser_ft = subparsers.add_parser('convert2ft',help='Uploads a given feature collection to Google Fusion Table.')
    parser_ft.add_argument('--i', help='input feature source (KML, SHP, SpatiLite, etc.)', required=True,widget="MultiFileChooser",default='input feature source (KML, SHP, SpatiLite, etc.)')
    parser_ft.add_argument('--o', help='output Fusion Table name', required=True)
    parser_ft.add_argument('--add_missing', help='add missing features from the last inserted feature index', action='store_true', required=False, default=False)
    parser_ft.set_defaults(func=ft_from_parser)

    parser_cleanout=subparsers.add_parser('cleanout',help='Clear folders with datasets from earlier downloaded')
    parser_cleanout.add_argument('--dirpath',help='Folder you want to delete after all processes have been completed',widget="MultiDirChooser")
    parser_cleanout.set_defaults(func=cleanout_from_parser)

    args = parser.parse_args()

    ee.Initialize()
    args.func(args)
    display_message()
def here_is_smore():
  pass


if __name__ == '__main__':
  main()
