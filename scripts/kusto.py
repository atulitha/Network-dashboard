def kq(time,fdate,todate,ip,key,scount):
    import requests
    q1=q2=q3=q4=q5=''
    if time!='':
        q1='\n | where TimeGenerated >= ago({x})'.format(x=time)
    if fdate!='' and todate!='':
        q2='\n | where TimeGenerated > startofday(datetime("{y}")) and TimeGenerated < endofday(datetime("{z}"))'.format(y=fdate,z=todate)
    if ip!='':
        q3='\n | where Computer contains "{a}"'.format(a=ip) 
    if key!='':
        if "," in key:
            words=key.split(",") 
            q4='\n | where SyslogMessage contains '
            for i in range(0,len(words)-1):
                w1='"{o}"'.format(o=words[i].replace(" ",''))
                q4=q4+w1+","
            q4=q4+'"{o}"'.format(o=words[len(words-1)].replace(" ",''))
        else:
            q4='\n | where SyslogMessage contains "{b}"'.format(b=key)
    if scount!='' and scount is not None:
        q5= '\n | summarize count() by {c}'.format(c=scount)    
    query=  'Syslog'+q1+q2+q3+q4+q5
    print(query)
    URL = "https://prod-10.westus2.logic.azure.com:443/workflows/7fca7ed7da304ba9847a44a4d0c091ed/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=yIcXPK55gwWVNQMO6saFo6idyvfg0h3klfaCVRZUzxo"
    #payload = "Syslog\r\n| where TimeGenerated >= ago(1m)\r\n| distinct Computer"
    headers = {
    'Content-Type': 'text/plain'
    }
    #response = requests.request("POST", url, headers=headers, data=payload)
    r = requests.request("POST",url = URL,headers=headers,data=query)
    string2=r.text
    print(r.text)
    string2=string2.replace("<table>",'')
    string3="</body>\n</html>"
    string1='''<!DOCTYPE html>
                <html>
                <head>
                    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.24/css/jquery.dataTables.min.css">
                    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/fixedheader/3.1.8/css/fixedHeader.dataTables.min.css">
                    
                    <style>
                        table {
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                        }

                        td, th {
                          border: 1px solid #dddddd;
                          text-align: left;
                          padding: 8px;
                        }

                        tr:nth-child(even) {
                          background-color: #dddddd;
                        }


                        thead input {
                                width: 100%;
                            }
                    </style>
                <script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-3.5.1.js"></script>
                <script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"></script>
                <script type="text/javascript" language="javascript" src="https://cdn.datatables.net/fixedheader/3.1.8/js/dataTables.fixedHeader.min.js"></script>
                <script>
                $(document).ready(function() {
                    // Setup - add a text input to each footer cell
                    
                    $('#example thead tr').clone(true).appendTo( '#example thead' );
                    $('#example thead tr:eq(1) th').each( function (i) {
                        var title = $(this).text();
                        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
                 
                        $( 'input', this ).on( 'keyup change', function () {
                            if ( table.column(i).search() !== this.value ) {
                                table
                                    .column(i)
                                    .search( this.value )
                                    .draw();
                            }
                        } );
                    } );
                 
                    var table = $('#example').DataTable( {
                        
                        orderCellsTop: true,
                        fixedHeader: true
                        
                    } );
                } );
                </script>
                    </head>
                <body>
                <table id="example" class="display" style="width:100%">'''

    #string2=r
    #string2=string2.replace("<table>",'')
    #string3="</body></html>"
    h=open("templates/temp/kusto/out.html",'w')
    h.write(string1+string2+string3)
    h.close()
