
## Quick Sauce Connect
Sauce Connect configuration examples. These examples are intended to demonstrate via a few scenarios the flexibility of this tool.


<br>

> If this is the first time using Sauce Connect, the [Quick Start Guide for Sauce Connect][docs-104] is a helpful reference to supplement these examples.
>
> For comprhensive usage, the [CLI docs for _saucectl run_][docs-105], lists all runtime parameters.
> 
> _Network egress to the Sauce API and platform is needed to start a Sauce Connect tunnel. The [Sauce Connect FAQ][docs-101] and [Sauce Labs Endpoints][docs-102] have details._


<br>

### No. 1 — Local Host Testing with Sauce Connect
  - _You have a development environment running on your workstation. It is only accessible locally and you would like to use Sauce Labs Cross Browser and Devices to test against localhost._


_[Reference Document — Sauce Labs Testing Against Localhost][docs-103]_  

- Export your Sauce Environment Variables

```
export SAUCE_USERNAME=""
export SAUCE_ACCESS_KEY=""
export SAUCE_REGION="eu-central-1"
```

<br>

- Add an alternate name for the localhost interface (loopback 127.0.0.1)

```        
sudo vi /private/etc/hosts
grep localdev /private/etc/hosts

127.0.0.1       localhost localdev
```


<br>

- Start your local http/s server, or use the simple Flask app provided below


```
python3 -m venv venv
. venv/bin/activate
pip install Flask
flask --app app/hello run --port 7777 --debug
```

<br>

- Start Sauce Connect

```
sc run --config-file ./etc/sc-localdev.yml
```


- Open the [Sauce Labs Live Testing][Live Testing EU] URL
- Select the type of session.
  - Desktop, Mobile Real, or Mobile Virtual.
- Select the sauce-connect tunnel.
  - It should be `<SAUCE_USERNAME>/localdev`
- Start your session.
- Enter the URL `http://localdev:7777` and test against your local host's resources!
  - Validated on Browsers, Devices, Emulators, and Simulators.


<br>

---


### No. 2 — [Network Capture with SSL Inspection](./docs/example-network-capture.md)

### No. 3 — Localisation Testing (Uses WonderProxy)
  - _You have to test your app or website when used in various countries._
  - Ensure you have a WonderProxy Username, Password, and access to the endpoints.

```shell
export SAUCE_USERNAME=""
export SAUCE_ACCESS_KEY=""
export SAUCE_REGION="eu-central-1"
export WONDERPROXY_USER=""
export WONDERPROXY_PASS=""

# Start a Tunnel in Canada
sc --config-file ./etc/sc-wonderproxy-ca.yml --proxy-userpwd "${WONDERPROXY_USER}:${WONDERPROXY_PASS}"

# Start a Tunnel in Australia
sc --config-file ./etc/sc-wonderproxy-au.yml --proxy-userpwd "${WONDERPROXY_USER}:${WONDERPROXY_PASS}"
```

- Open the [Sauce Labs Live Testing][Live Testing EU] URL
  - Select the type of session.
    - Desktop, Mobile Real, or Mobile Virtual.
  - Select the sauce-connect tunnel.
    - It should be `geo-ip-[TWO DIGIT COUNTRY CODE]`
      - e.g. `geoip-ca`, `geoip-au`
  - Start your session.



[Live Testing EU]: https://app.eu-central-1.saucelabs.com/live/web-testing
[docs-101]: https://docs.saucelabs.com/secure-connections/sauce-connect/faq/#what-outbound-ports-do-i-need-open-for-sauce-connect-proxy
[docs-102]: https://docs.saucelabs.com/basics/data-center-endpoints/#data-center-endpoints
[docs-103]: https://docs.saucelabs.com/secure-connections/sauce-connect-5/guides/localhost-proxying/
[docs-104]: https://docs.saucelabs.com/secure-connections/sauce-connect/quickstart
[docs-105]: https://docs.saucelabs.com/dev/cli/sauce-connect-5/run/


<br>

---
_This source code is licensed under the MIT license found in the LICENSE file in the root directory of this source tree_