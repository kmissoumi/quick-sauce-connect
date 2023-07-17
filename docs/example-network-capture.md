## Network Capture with SSL Inspection

- Export your Sauce Environment Variables

```shell
export SAUCE_USERNAME=""
export SAUCE_ACCESS_KEY=""
export SAUCE_REGION="eu-central-1"
```

- Start a sauce connect tunnel using the attached configuration

```shell
sc --config-file ./etc/network-capture.yml
```

- Start Charles Proxy
  - Make sure it is listening on port 8180 (i.e. match the port configured in the sauce connect yml file)
    - Charles App Menu > Proxy > Proxy Settings > Port
  - Enable the SSL
    - Charles App Menu > Proxy > SSL Proxy Settings
      - Enable SSL Proxying
      - Include target domains (or * for all)
      - Exclude host *saucelabs.com for port 443 
 
> DO NOT enable macOS Proxy. Sauce Connect will send the data to Charles.


- On Sauce Labs
  - Start a live session
    - Select simulator + tunnel called `netcap`
    - Start the session
      - Open the browser to http://chls.pro/ssl
      - Download a configuration profile
    - Install certificate.
      - Home button > Settings App > General > Device Management > Select Charles Profile > Select Install Three Times > Done
    - Enable CA Trust
      - Home button > Settings App > General > About > Certificate Trust Settings > Toggle Charles Certificate > Continue
