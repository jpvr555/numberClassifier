import requests
import argparse

# Check what mode we are on and call the appropriate function 
def main():
    parser = argparse.ArgumentParser(description='Client for number classifier server.')
    host =  argparse.ArgumentParser(add_help=False)
    host.add_argument('-s', '--host', help='hostname of the server', nargs='?', default='localhost')
    host.add_argument('-p', '--port', help='port number for the server', nargs='?', default='8085')
    sp = parser.add_subparsers()
    sp.required = True
    sp.dest = 'command'
    sp_list = sp.add_parser('list', help='fetch all previous results from the server', parents=[host])
    sp_send = sp.add_parser('send', help='send file to server for inference', parents=[host])
    sp_send.add_argument('-f', '--filepath', help='path of the file to be sent', required=True)
    args = parser.parse_args()

    if(args.command == 'list'):
        list_results(args)
    elif(args.command == 'send'):
        send_file(args)

# Imply return the json list from the API
def list_results(args):
    url = 'http://{h}:{p}/v1/inference'.format(h=args.host, p=args.port)

    r = requests.get(url)
    if(r.ok):
        print(r.text)
    else:
        print('Error getting list of results. Got status: {}'.format(r.status_code))

# Upload a file for classification and display the results.
def send_file(args):
    url = 'http://{h}:{p}/v1/inference'.format(h=args.host, p=args.port)
    files = {'file_name': open(args.filepath,'rb')}

    r = requests.post(url, files=files)
    if(r.ok):
        print(r.text)
    else:
        print('Error sending file. Got status: {}'.format(r.status_code))

if __name__ == '__main__':
    main()
