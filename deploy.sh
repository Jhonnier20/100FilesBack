echo "------------ Running the enviroment ------------"
waitress-serve  --port=2010 --call 'flaskr:create_app'