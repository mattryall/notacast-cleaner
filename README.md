## NotACast RSS feed cleaner

This is a service for removing duplicate entries in the 
[NotACast Podcast](https://notacastasoiaf.podbean.com) 
Patreon feed, which are quite annoying as a subscriber.

It pulls down the Patreon feed using your subscriber auth token, and makes
the following changes:

* Keeps the earliest item with a particular title, so you don't get duplicates
for the public and subscriber releases of the same podcast
* Updates the channel URL and title so your podcast player can distinguish
between this clean feed and the normal one.

This should make it suitable as a drop-in replacement for your normal
Patreon feed.

### Usage

I'm running this as a service which you can use at:

* [https://api.mattryall.net/notacast/notacast-clean.rss?auth=](https://api.mattryall.net/notacast/notacast-clean.rss?auth=)

Just stick your Patreon auth token at the end of this URL and add it to your 
podcast client instead of the normal Patreon feed.

Your Patreon auth token is not stored anywhere except if there's an error and
the URL needs to be logged. These logs are accessible only to me, and kept for
30 days before being deleted.

If you prefer, you can run it yourself. Instructions on how to do that below.

### Running the script

The most basic way is just to run the script at the command line.
You need to provide a PATREON_AUTH environment variable
and run `src/clean_notacast.py`:

```bash
$ PATREON_AUTH=... python3 src/clean_notacast.py 
```

This will download the RSS feed from the Patreon

### Development notes

#### Setup

I've developed the project with Python 3.8 and 3.9, but should work with any 3.x version.

I recommended setting up a Python virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

You can then open the project in PyCharm for development.

#### Deployment to AWS Lambda

You'll need to manually create a Python 3.x Lambda in AWS, then update the 
ARN in the code to match it.

Then deployment can be done by configuring AWS credentials in environment 
variables, and running `deploy.py`:

```
(venv) $ export AWS_ACCESS_KEY_ID=...
(venv) $ export AWS_SECRET_ACCESS_KEY=...
(venv) $ export AWS_DEFAULT_REGION=ap-southeast-1
(venv) $ python deploy.py
2021-01-15 20:59:57,404 [INFO] __main__ Adding: src/clean_notacast.py -> clean_notacast.py
2021-01-15 20:59:57,404 [INFO] __main__ Adding: src/lambda_function.py -> lambda_function.py
2021-01-15 20:59:57,405 [INFO] __main__ Updating lambda...
2021-01-15 20:59:57,434 [INFO] botocore.credentials Found credentials in environment variables.
2021-01-15 20:59:57,704 [INFO] __main__ Updated lambda successfully
```
