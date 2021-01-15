## NotACast RSS feed cleaner

This code removes duplicate entries from the 
[NotACast Podcast](https://notacastasoiaf.podbean.com) 
Patreon feed, which are quite annoying as a subscriber.

### Usage

The cleaner is running as a service at:

* [https://api.mattryall.net/notacast/notacast-clean.rss?auth=...](https://api.mattryall.net/notacast/notacast-clean.rss?auth=...)

Just stick your Patreon auth token at the end of the URL and away you go. 
I don't log or store the tokens anywhere on my side.

You can also run it yourself, if you prefer. Instructions on how to do that below.

#### Running the script

The most basic way is just to run the script at the command line.
You need to provide a PATREON_AUTH environment variable
and run `src/clean_notacast.py`:

```bash
$ PATREON_AUTH=... python3 src/clean_notacast.py 
```

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

You need to configure AWS credentials via environment variables, then run `deploy.py`:

```
$ export AWS_ACCESS_KEY_ID=...
$ export AWS_SECRET_ACCESS_KEY=...
$ export AWS_DEFAULT_REGION=ap-southeast-1
```

You'll need to manually create a Python 3.x Lambda in AWS, then update the 
ARN in the code to match it.

