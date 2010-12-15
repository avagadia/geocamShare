
import hashlib
import urllib2
import os
import os.path as op
import sys
import time
import stat
import re
from StringIO import StringIO

from PIL import Image, ImageDraw, ImageFont, ImageOps
from django.conf import settings
from django.contrib.auth.models import User

AVATAR_DIR = '%s/shareTracking/media/avatars' % settings.CHECKOUT_DIR
GRAVATAR_DIR = '%s/gravatars' % AVATAR_DIR
CACHE_DIR = '%s/cache' % AVATAR_DIR
PLACARD_FRESH = '%s/shareTracking/media/mapIcons/placard.png' % settings.CHECKOUT_DIR

# time to wait before retry after failed gravatar fetch
GRAVATAR_FAIL_RETRY_SECONDS = 24*60*60

# time to wait before refresh after successful gravatar fetch
GRAVATAR_SUCCESS_REFRESH_SECONDS = 24*60*60

def mkdirP(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def fetchGravatarImage(email, fname):
    '''Grabs the Gravatar image for the given email address and writes it to fname.
    Returns False on error.'''
    hex = hashlib.md5(email.strip().lower()).hexdigest()
    url = 'http://www.gravatar.com/avatar/%s.jpg?d=404' % hex
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print >>sys.stderr, 'fetch %s -- failed to reach a server' % url
            print >>sys.stderr, 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print >>sys.stderr, 'fetch %s -- server couldn\'t fulfill request' % url
            print >>sys.stderr, 'Error code: ', e.code
        return False
    mkdirP(os.path.dirname(fname))
    out = file(fname, 'w')
    out.write(response.read())
    out.close()
    return True
    
def getAge(fname):
    mtime = os.stat(fname)[stat.ST_MTIME]
    return time.time() - mtime

def getGravatarPath(userName, email):
    """Returns a path on local disk that points to the gravatar icon for
    the given user, or None if we couldn't fetch one.  Caches past query
    results for efficiency."""
    failFname = '%s/%s-fail.txt' % (GRAVATAR_DIR, userName)
    successFname = '%s/%s.jpg' % (GRAVATAR_DIR, userName)

    if os.path.exists(successFname):
        if getAge(successFname) < GRAVATAR_SUCCESS_REFRESH_SECONDS:
            return successFname
        else:
            os.unlink(successFname)

    if os.path.exists(failFname):
        if getAge(failFname) < GRAVATAR_FAIL_RETRY_SECONDS:
            return None
        else:
            os.unlink(failFname)

    mkdirP(os.path.dirname(failFname))
    file(failFname, 'w').close()
    status = fetchGravatarImage(email, successFname)
    if status:
        os.unlink(failFname)
        return successFname
    else:
        return None

def parse_params(params):
    color = None
    if 'color' in params:
        if re.match(r'^[0-9a-fA-F]{6}$', params['color']):
            color = params['color'].lower()

    scale = None
    if 'scale' in params:
        try:
            scale = float(params['scale'])
        except ValueError:
            pass

    stale = False
    if 'stale' in params:
        stale = True

    return (color, scale, stale)

def renderAvatar(request, userName):
    # Parse junk
    (color, scale, stale) = parse_params(request.REQUEST)

    # See if we can return cached image
    image_name = userName
    if color:
        image_name += "_%s" % color
    if scale:
        image_name += "_%s" % scale
    if stale:
        image_name += '_stale'
    image_name += '.png'
    full_path = op.join(CACHE_DIR, image_name);
    if op.exists(full_path):
        return open(full_path, 'r').read()

    placard = Image.open(PLACARD_FRESH)

    # Colorize base placard
    if color:
        placard.load()
        bands = placard.split()
        placardGray = placard.convert("L")
        placardColored = ImageOps.colorize(placardGray, 
                                           "#000000", 
                                           "#" + color);
        placard = placardColored.convert("RGBA");
        placard.putalpha(bands[3]);

    # Find avatar, gravatar or lettered image
    avatar = None
    avatar_file = op.join(AVATAR_DIR, "%s.png" % userName)
    if op.exists(avatar_file):
        avatar = Image.open(avatar_file)
    else:
        featureUser = User.objects.get(username=userName)
        gravPath = getGravatarPath(userName, featureUser.email)
        if gravPath:
            avatar = Image.open(gravPath)
        else:
            avatar = Image.new("RGB", (8, 8), "#FFFFFF")
            font = ImageFont.load_default()
            draw  = ImageDraw.Draw(avatar)
            draw.text((1, -2), userName.upper()[0], font=font, fill=0)
            del draw
    
    # Paste generated/opened image into placard
    avatar = avatar.resize((36,36))
    placard.paste(avatar, (10, 8))
    
    # Optionally scale image
    if scale:
        new_size = (int(placard.size[0] * scale),
                    int(placard.size[1] * scale))
        placard = placard.resize(new_size)
    
    # Save image in cache
    placard.save(full_path, "PNG")

    # Send image to browser
    strio = StringIO()
    placard.save(strio, "PNG")
    return strio.getvalue()
