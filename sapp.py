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
    'redirect_uri': 'https://instaclient.herokuapp.com/'
}

unauthenticated_api = client.InstagramAPI(**CONFIG)
#reactor = subscriptions.SubscriptionsReactor()
#reactor.register_callback(subscriptions.SubscriptionType.TAG, process_tag_update)

@route('/')
def user_likes():
    content = "<h2>User Liked Media</h2>"
    access_token = '3034913826.1677ed0.ad37bc63b4b145b3aea55b699d8885d2'
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        media_feed, next = api.user_liked_media()
        photos = []
        for media in liked_media:
            photos.append('<div style="float:left;">')
            if(media.type == 'video'):
                photos.append('<video controls width height="150"><source type="video/mp4" src="%s"/></video>' % (media.get_standard_resolution_url()))
            else:
                photos.append('<img src="%s"/>' % (media.get_low_resolution_url()))
            photos.append("<br/> <a href='/media_like/%s'>Like</a>  <a href='/media_unlike/%s'>Un-Like</a>  LikesCount=%s</div>" % (media.id,media.id,media.like_count))
        content += ''.join(photos)
    except Exception as e:
        print(e)
#    return True
    #return "%s %s <br/>Remaining API Calls = %s/%s" % (get_nav(),content,api.x_ratelimit_remaining,api.x_ratelimit)

bottle.run(app=app, host='0.0.0.0', port=argv[1], reloader=True)
