# open_proxy_validator

Python program to iterate through and check a list of proxies. Try ti connect to a website
via a socks proxy. Considers a proxy valid if requests.get status code == 200. 


#### Usage:

    Usage: proxy_test.py [options] arg
    
    Options:
      -h, --help            show this help message and exit
      -f FILENAME, --proxy_lst=FILENAME
                            read proxies from FILENAME
      -v, --verbose         
      -d, --very_verbose    Debug / Very Verbose mode
      -p, --print_content   Print html content from requests

#### Formats:

input file:

<pre>
11.14.215.44:1111:socks4
12.14.215.44:222:socks5
...
</pre>

output format (for use with browsers, or selenium, etc):

<pre>
socks4://11.14.215.44:1111
socsk5://12.14.215.44:222
</pre>
