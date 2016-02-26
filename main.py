import tweepy, json, requests, random, string, HTMLParser

def search(searchstring):
    query = {'q': searchstring}
    search_dump = requests.get("http://ajax.googleapis.com/ajax/services/search/web?v=1.0", params=query).text
    results = json.loads(search_dump)
    response_data = results['responseData']
    return response_data

def rand_string(length):
    return ''.join(random.choice(string.lowercase + string.uppercase) for i in range(length))

def main():
    CONSUMER_KEY = find_setting('consumer_key')
    CONSUMER_SECRET = find_setting('consumer_secret')
    ACCESS_KEY = find_setting('access_key')
    ACCESS_SECRET = find_setting('access_key_secret')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    h = HTMLParser.HTMLParser()
    while True:
        search_query = search('site:youtube.com/watch "youtube.com/watch?v=%s"' % rand_string(5))
        if search_query:
            if not search_query['results']:
                print "Trying to find YouTube link..."
            else:
                youtube_link = search_query['results'][0]
                video_title = h.unescape(youtube_link['titleNoFormatting']).replace(' - YouTube', '')
                first_url = youtube_link['unescapedUrl']
                break;
        else:
            break;

    try:
        status_body = "\"%s\" #YouTube\n%s" % (video_title, first_url)
        if len(status_body) > 140:
            print "Body too long :("
        else:
            api.update_status(status=status_body)
        print "Posted status '%s'" % first_url
    except:
        print "Could not post tweet"

# Thanks to this wonderful tutorial http://www.decalage.info/en/python/configparser, this was easy
def settings():
    settings = {}
    settings_file = open("/home/django/random-yt/custom/youtube_settings.txt")
    for line in settings_file:
        if "#" in line:
            line, comment = line.split("#", 1)
        if "=" in line:
            setting, value = line.split("=", 1)

            setting = setting.strip()
            value = value.strip()

            settings[setting] = value
    settings_file.close()
    return settings

def find_setting(key):
    try:
        return settings()[key]
    except KeyError:
        print "Key '%s' not found in settings file, please check again." % key
        sys.exit(0)

if __name__ == '__main__':
    main()
