from flask import Flask, url_for, render_template, send_from_directory,request, Response, send_file
import jinja2.exceptions
import json
row=1
row2=1
row3=1
sitecode=''
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kustorun', methods=['POST', 'GET'])
def direct():
    from scripts import kusto
    time=request.form.get('HOURS')
    ip=request.form.get('ip')
    hname=request.form.get('Hostname')
    fdate=request.form.get('fdate')
    todate=request.form.get('todate')
    key=request.form.get('Command')
    scount=request.form.get('scount')
    print(time,ip,hname,fdate,todate,key,scount)
    string='''Syslog
        | where TimeGenerated >= ago ({x})
        | where TimeGenerated > startofday(datetime("{y}")) and TimeGenerated < endofday(datetime("{z}"))
        | where Computer contains "{a}"
        | where SyslogMessage contains "{b}"
        | summarize count by {c}'''.format(x=time,y=fdate,z=todate,a=ip,b=key,c=scount)
    print(string)
    kusto.kq(time,fdate,todate,ip,key,scount)
    return render_template("temp/kusto/out.html")

@app.route('/<pagename>')
def admin(pagename):
    if(pagename=='NetworkDiagramIndex'):
        with open("scripts/sitelist","r") as file1:
            content = file1.read()
            content1=content.split('\n')
        f = open('scripts/listofsitename.json') 
        data = json.load(f)
        return render_template("NetworkDiagramIndex.html", content = content1,data=data)
    if pagename=='kustoquery':
        options=[]
        with open("summarize_options.txt","r") as locn:
            content = locn.read()
            options=content.split('\n')
        return render_template(pagename+".html", content = options )   
    elif pagename=='check':
        f = open('static/frontend_new.json') 
        data = json.load(f)
        return render_template(pagename+".html",data=data) 
    else:
        return render_template(pagename+'.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
	return send_from_directory('static/', resource)

@app.route('/test')
def test():
    return '<strong>It\'s Alive!</strong>'

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(e):
    return not_found(e)

@app.errorhandler(404)
def not_found(e):
    return '<strong>Page Not Found!</strong>', 404

@app.route('/sshrun', methods=['POST'])
def run():
    try:
        import multiprocessing
        Pool = multiprocessing.Pool
        from scripts import ssh
        if request.method == 'POST':
            data = request.form
            data1 = ssh.inputvar(data["Hostname"],data["Command1"],data["Command2"],data["Command3"])
            if len(data1) > 60:
                nprocs = 60
            else:
                nprocs = len(data1)
            with Pool(nprocs) as p:
                data2 = p.map(ssh.runt, data1)
            print(data2, sep=",")
        return render_template("ssh2.html",form = data2)
    except Exception as e:
        return render_template("table2.html",table = e)

@app.route('/checkrun', methods=['POST', 'GET'])
def direct_check():
    from scripts import f_checklist
    import pandas as pd
    import numpy as np
    import xlsxwriter
    global sitecode
    site=request.form['site']
    sitecode=site.split(' ', 1)[0] 
    f_checklist.check(sitecode)
    print("done")
    out1 = pd.read_excel('checklist.xlsx', sheet_name='sheet1')
    #out2 = pd.read_excel('checklist.xlsx', sheet_name='neighbor')
    out3 = pd.read_excel('checklist.xlsx', sheet_name='ethernetInterfaces')
    out4 = pd.read_excel('checklist.xlsx', sheet_name='etherChannels')
    return render_template("check_new.html",devicedata=out1.values.tolist(),etherChannels=out4.values.tolist(),ethernetInterfaces=out3.values.tolist())
@app.route('/fullreport', methods=['POST','GET'])    
def fullreport():
    import pandas as pd
    global sitecode
    print(sitecode)
    out1 = pd.read_excel('checklist.xlsx', sheet_name='sheet1')
    out2 = pd.read_excel('checklist.xlsx', sheet_name='neighbor')
    out3 = pd.read_excel('checklist.xlsx', sheet_name='ethernetInterfaces')
    out4 = pd.read_excel('checklist.xlsx', sheet_name='etherChannels')
    return render_template('checklist_out.html',  primary=[out1.to_html(classes='data')], prim_titles=out1.columns.values,
                            neigh=[out2.to_html(classes='data')],neigh_titles=out2.columns.values,etherInf=[out3.to_html(classes='data')],
                            etherInf_titles=out3.columns.values,etherChanl=[out4.to_html(classes='data')],etherChanl_titles=out4.columns.values)
@app.route('/down', methods=['POST','GET'])    
def down():
    global sitecode
    #site=request.form['site']
    #sitecode=site.split(' ', 1)[0]
    return send_file('checklist.xlsx',
                         mimetype='text/csv',
                         attachment_filename=sitecode+'1.xlsx',
                         as_attachment=True)
@app.route("/networkdiagram",methods = ["POST","GET"])  
def networkdiagram():  
    if request.method == "POST":  
            
            try:  
                sitename = request.form['sitename']
                sitename=sitename.split("-")[0]
                sitename=sitename.replace(" ","")
                print(sitename)
                from scripts import networkmain
                dic,hi,tr=networkmain.networkdiagram1(sitename)
                #print(dic)
                return render_template('temp/NetworkDiagram/tree.html',mulparents=dic,hi=hi,tr=tr)
                    


            except  Exception as e:
                print(str(e))
     
    
if __name__ == "__main__":
    app.run(debug= 1)