




# Local Host Testing with Sauce Connect


- Export your Sauce Environment Variables

```
export SAUCE_USERNAME=""
export SAUCE_ACCESS_KEY=""
export SAUCE_REGION="eu-central"
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
flask --app app/hello run --port 7777
```

<br>

- Start Sauce Connect

```
sc --config-file sauce-connect-localdev.yml
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
<br>
<br>

> _[Reference Document from Sauce Labs Testing Against Localhost][20]_  
>  
>  
> _This source code is licensed under the MIT license found in the LICENSE file in the root directory of this source tree_


[Live Testing EU]: https://app.eu-central-1.saucelabs.com/live/web-testing
[20]: https://docs.saucelabs.com/secure-connections/sauce-connect/setup-configuration/specialized-environments/#testing-mobile-devices-against-localhost

