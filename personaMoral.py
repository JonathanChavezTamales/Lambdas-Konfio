import json
from botocore.vendored import requests
import os

def lambda_handler(event, context):
    
    res = ""
    body = json.loads(event["body"])
    
    legal_name = body["legalName"]
    date_founded = body["dateFounded"] 
    rfc = body["rfc"]
    
    #TT
    puntos_buro = requests.get(f"http://6ec13db8.ngrok.io/api/buro/moral/?rfc={rfc}").json()["score_bc"]
    puntos_sat = requests.get(f"http://6ec13db8.ngrok.io/api/sat/moral/?rfc={rfc}").json()["score_sat"]

    puntos_total = (puntos_buro+puntos_sat)/2
    
    puntos_total = int(puntos_total)

    monthly_earnings = int(body["monthlyEarnings"])
    loan = int(body["loan"])
    term_in_months = int(body["termInMonths"])
    
    
    if monthly_earnings >= loan*0.083 and puntos_total > 85:
        res = "A"
    elif monthly_earnings > loan*0.041 and puntos_total > 60:
        res = "B"
    elif monthly_earnings > loan*0.021 and puntos_total > 45:
        res = "C"
    elif monthly_earnings <= loan*0.021 and puntos_total <= 45:
        res = "D"
        
    


    #Metadata
    client_ip = event["headers"]["X-Forwarded-For"]
    city = requests.get(f"http://api.ipstack.com/{client_ip}?access_key={os.environ['IPSTACK_KEY']}").json()["city"]
    
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(json.dumps({"category":res}))
    }

