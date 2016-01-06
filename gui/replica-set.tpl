<!DOCTYPE html>
%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<html>
    <head>
        <meta charset ="utf-8"/>
        <meta http-equiv="refresh" content="30">
        <style>
            table ,th,td {
            border :1px solid black ;
            border-collapse: collapse;
            }
            th, td {
                padding: 10px;
            }
        </style>
        <title>{{title}}</title>
    </head>

    <body style="background-color:lightgrey">
        <p>
            <a href="http://localhost:8889/Standalone">Standalone</a>
            <a href="http://localhost:8889/Replica-set">Replicaset</a>
            <a href="http://localhost:8889/Sharding">Sharding</a>
        </p>

        <h1 style="float:center;color:green">{{db_type}}</h1>
            <table style="float:left;width:49%">
                <caption style="color:brown","font-family:verdana","font-size:500%">PRIMARY -port {{primary_port}} Student collection</caption>
                <tr>
                    %for col in student_column:
                        <th>{{col}}</th>
                    %end
                </tr>
                %for row in data:
                    <tr >
                        %print len(student_column)
                        %print row
                        %for col in range(0,len(student_column)):
                            %if student_column[col] =="course":
                                <td style ="color:red">{{row[col]}}</td>
                            %else:
                                <td style ="color:blue">{{row[col]}}</td>
                            %end
                        %end
                    </tr>
                %end
            </table>
             <table style="float:right;width:49%">
                <caption style="color:brown","font-family:verdana","font-size:300%">SECONDERY -port {{secendary_port}} Student collection </caption>
                <tr>
                    %for col in student_column:
                        <th>{{col}}</th>
                    %end
                </tr>
                %for row in secendary_data:
                    <tr >
                        %for col in range(0,len(student_column)):

                            %if student_column[col] =="course":
                                <td style ="color:red">{{row[col]}}</td>
                            %else:
                                <td style ="color:blue">{{row[col]}}</td>
                            %end
                        %end
                    </tr>
                %end
            </table>


        <br> <br><br> <br>
   </body>
</html