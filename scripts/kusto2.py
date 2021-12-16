def kq():
    import requests
    import pandas as pd,json
    URL = "https://prod-10.westus2.logic.azure.com:443/workflows/7fca7ed7da304ba9847a44a4d0c091ed/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=yIcXPK55gwWVNQMO6saFo6idyvfg0h3klfaCVRZUzxo"
    r = requests.post(url = URL, params = {})
    string2=r.text
    df = pd.DataFrame(json.loads(string2))
    print (df)
    return df.to_html(classes="table table-striped table-bordered table-hover", table_id="dataTables-example")