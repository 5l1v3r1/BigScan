import os
import argparse
import time
import re

def Ping_scan(ip):
    print '-----------------------------------------------------------------------------------'
    print 'Scan Ip'
    Ping_command = 'nmap -v -sn -PE  --open -n --min-hostgroup 1024 --min-parallelism 1024 -oG '+ dirname+'ip.txt ' +ip
    print Ping_command
    os.system(Ping_command)

def Filter_ip():
    with open(dirname+'ip.txt','r') as f:
        for line in f.readlines()[2:-1]:
            pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
            ips = pattern.findall(line.split('\n')[0])
            with open(dirname+'ip-result.txt','a') as ff:
                 ff.write(ips[0]+'\n')

def Scan_port():
    print '-----------------------------------------------------------------------------------'
    print 'Scan Port'
    Scan_command = 'nmap -v -Pn  -T4 -p- --open -n --min-hostgroup 1024 --min-parallelism 1024 -iL '+dirname+'ip-result.txt  -oX ' +dirname+'port.xml'
    print Scan_command
    os.system(Scan_command)

def output():
    Path = os.getcwd()+'\\'
    os.chdir(Path+'xsltproc\\bin\\')
    os.system('xsltproc.exe -o '+ Path+dirname +'\\index.html beautiful.xsl '+Path+dirname+'\\port.xml')
if __name__ =='__main__':
    parser = argparse.ArgumentParser(description="Nmap scan big ip and port")
    parser.add_argument("-t", "--target", type=str,help = "The target IP")
    args = parser.parse_args()
    if args.target==None:
        print 'usage: python Nmap_big_scan.py -t  192.168.10.70/24'
    else:
        try:
            if '/' in args.target:
                result = args.target.split('/')[0]+'---'+args.target.split('/')[1]
            else:
                result = args.target
            os.mkdir(result)
            dirname = result + '/'
            Ping_scan(args.target)
            Filter_ip()
            Scan_port()
            output()
        except Exception as e:
            print e
            pass
