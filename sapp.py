import bottle
import beaker.middleware
from bottle import route, redirect, post, run, request, hook
from instagram import client, subscriptions
from sys import argv

bottle.debug(True)

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)

CONFIG = {
    'client_id': 'aa18575b408b4dbd9039319de55d0bed',
    'client_secret': '06a7bfba726941fc8dbec9ebff369958',
    'redirect_uri': 'https://instaclient.herokuapp.com/oauth_callback'
}

unauthenticated_api = client.InstagramAPI(**CONFIG)
reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.TAG, process_tag_update)

@route('/')
def home():
    try:
        access_token = '3034913826.1677ed0.ad37bc63b4b145b3aea55b699d8885d2'
        if not access_token:
            return 'Could not get access token'
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
    except Exception as e:
        print(e)
  
    nav_menu = ("<h1>Python Instagram</h1>"
                "<ul>"
                    "<li><a href='/liked'>User Liked Media</a> Get a list of a user's most recent liked media</li>"                   
                "</ul>")
    return nav_menu


@route('/liked')
def user_likes():
    content = "<h2>User Liked Media</h2>"
    access_token = request.session['access_token']
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        media_feed, next = api.user_media_feed()
        photos = []
        for media in media_feed:
            photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
            if(media.type == 'video'):
                photos.append('<video controls width height="150"><source type="video/mp4" src="%s"/></video>' % (media.get_standard_resolution_url()))
            else:
                photos.append('<img src="%s"/>' % (media.get_standard_resolution_url())
	counter = 1
        while next and counter < 3:
            media_feed, next = api.user_media_feed(with_next_url=next)
            for media in media_feed:
                photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
            counter += 1
        content += ''.join(photos)
    except Exception as e:
        print(e)
    return "%s %s <br/>Remaining API Calls = %s/%s" % (get_nav(),content,api.x_ratelimit_remaining,api.x_ratelimit)

bottle.run(app=app, host='0.0.0.0', port=argv[1], reloader=True)
