# sys module for command line arguments.
# collection module for sorted dictionary.
import sys
import collections

URL = ""

def extract_info(filename):
    """This function will read the .jtl file and extract the necessery fields (testcase, status)
    and create a dictionary with those feilds."""
    output = {}
    required_fields = []
    with open(filename, 'r') as curr_file:
        for row in curr_file:
            temp = row.split(",")
            required_fields.append([temp[2], temp[8]]) 
    p=0
    n=0
    for each_field in required_fields[1:]:
        temp = each_field[0].split('_')
        if each_field[1] == 'true':
            p += 1
        else:
            n += 1
        URL = "https://local.refer.com" if each_field[1] == 'false' else ""
        if temp[0] in output:
            output[temp[0]].append(["_".join(temp[1:]), each_field[1], URL])
        else:
            output[temp[0]] = [["_".join(temp[1:]), each_field[1], URL]]
    print(p,n)
    print("[Success] File ",filename," successfully read.")
    return collections.OrderedDict(sorted(output.items()))
    
def create_html(file_name, content, html_file_name):
    """This function will generate a html table form the content provided"""

    html_start = """<html><head><title>JTL Output Log</title>
    <style>body{ margin: 0 auto;width: 700px;font-family: sans-serif;
    margin-top: 10px;}.red{background-color: #ff9f9f}.green{background-color: #6edc8e}
    table{border-collapse: seperate;border-radius:10%;}a{text-decoration: none;}
    th,td {border: 1px solid #cecfd5;padding: 5px 15px;}
    .block{font-weight: bold;} h2,p{text-align:center;}
    .even{background-color: #f0f0f0;}
    th{background: #395870;color: #fff;}</style></head><body>
    <p>File name: <b>"""
    html_start += file_name + "</b></p>"
    html_body = "<center><table><tr><th>Test Case #</th><th>Use Case</th><th>Status</th><th>URL</th></tr>"
    flag = True
    for key, val in content.items():
        rowspan = len(val)
        i = -1
        while i < rowspan:
            if i == -1:
                if flag:
                    pos = "even"
                    flag = not flag
                else:
                    pos = "odd"
                    flag = True
                html_body += "<tr><td  class=\"block " + pos
                html_body += "\" rowspan=\"" + str(rowspan) + "\">"
                html_body += str(key).capitalize() + "</td>"
            else:
                css_class = "red" if val[i][1] == 'false' else 'green'
                status = "Passed" if val[i][1] == 'true' else "Failed"
                if i > 0:
                    html_body += "<tr>"
                html_body += "<td class=\"" + css_class + "\">" + val[i][0] + "</td>"
                html_body += "<td class=\"" + css_class + "\">" + status + "</td>"
                html_body += "<td class=\"" + css_class + "\">" + "<a href=\"\">"
                html_body += val[i][2] + "</a></td></tr>"
            i += 1
    html_end = "</table></center></body></html>"
    with open(html_file_name, "w") as html_file:
        html_file.write(html_start + html_body + html_end)

# Starting point
def main(args):
    """This function will get the arguments from the command file and extract the key values
       from the .jtl file and return as a python dictionary"""
    if len(args) != 1:
        print("[Error] Wrong number of arguments.")
        print("[Suggestion] Usage > $python reader.py filename.jtl")
        exit(-1)
    filename = args[0]
    html_file_name = "error_log.html"
    content = extract_info(filename)
    create_html(filename, content, html_file_name)
    print("[Done] The log file " + html_file_name + " is generated as output.")

if __name__ == '__main__':
    # passing all the command line arguments to the main function,
    # argv[0] conatins the file name iteself so no need for that.
    main(sys.argv[1:])
