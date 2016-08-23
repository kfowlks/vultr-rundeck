# Vultr Rundeck Resource Dump 

This program reads the server instance information from [vultr](https://my.vultr.com/) using their API and converts the output to a rundeck compatible resources.xml file format. In order to use the program, you'll need a valid vultr account along with an API key. 

You can find more information on enabling the API functionality from the link below. 

https://my.vultr.com/settings/#settingsapi

###Reference
Rundeck resource xml format http://rundeck.org/1.5.2/manpages/man5/resource-v13.html

###Requires
Under CYGWIN run the below to install pip
```bash
  python -m ensurepip
 ```
This code relies on the following python module: https://pypi.python.org/pypi/vultr/0.1.2

```bash
pip install vultr
 ```
 
### Version
0.0.1

### Running the program 

    ```bash
            $ python dump-rundeck-resources.py -k [Vultr-API-Key]
    ```
            or 
    ```bash
            export VULTR_KEY=APIKEY
            
            $ python dump-rundeck-resources.py
            
            $ python dump-rundeck-resources.py > /var/rundeck/projects/rundeck-production/etc/resources.xml
    ```


