#!/usr/bin/env python
# server

Site = 'Cipher Site'

Timezone = 'America/Toronto'

Colors = '''
    base03:    #002b36;
    base02:    #073642;
    base01:    #586e75;
    base00:    #657b83;
     base0:    #839496;
     base1:    #93a1a1;
     base2:    #eee8d5;
     base3:    #fdf6e3;
    yellow:    #b58900;
    orange:    #cb4b16;
       red:    #dc322f;
   magenta:    #d33682;
    violet:    #6c71c4;
      blue:    #268bd2;
      cyan:    #2aa198;
     green:    #859900;
''' # - http://ethanschoonover.com/solarized

Analytics = '''<script>


</script>'''



SASS_Code = '''


'''

post_page_html_public = '''

'''

list_page_html_public = '''

'''

list_page_html_admin = '''

'''

manage_page_html = '''

'''

# - HTML Page Code
publish_page_html = '''
<style>
.form_wrap { margin-left: 55px; margin-top: 35px; outline: 1px solid #eee; width: 345px; padding: 45px; }
tr { height: 32px; }
td.label { font-size: 14px; text-align: right; padding-right: 10px; }
input[type="text"] { width: 200px; height: 16px; }
</style>
<div class="page_html">
 <header class="hi"><span class="color_b">Fill Out The Form</span></header>
  <article class="form_wrap">
    <form action="../../add_form" enctype="multipart/form-data" method="post">
      <table>
        <tr>
          <td class="label">Email Addess</td>
          <td class="input"><input type="text" name="email_address" /></td>
        </tr>
        <tr>
          <td class="label">User Name</td>
          <td class="input"><input type="text" name="user_name" /></td>
        </tr>
        <tr>
          <td></td>
          <td style="text-align:right"><input type="submit" value="Sign Up" /></td>
        </tr>
      </table>
    </form>
  </article><!-- - /form_wrap - -->
</div><!-- - /page_html - -->
'''


posts_page_html = '''
Blog
'''


# - System
import os
import urllib
import wsgiref.handlers
import webapp2
import json
# - 
from google.appengine.api import users
from google.appengine.api import mail
# -
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
# -
from urlparse import urlparse
# -
import time
import datetime
from pytz.gae import pytz


class Blog_db(db.Model):
    addTime = db.DateTimeProperty(auto_now_add=True)
    data_id = db.StringProperty()
  #
    post_title = db.StringProperty()
    post_body = db.TextProperty()

class addBlog_db(webapp2.RequestHandler):
    def post(self):
        date_time = datetime.datetime.now(pytz.timezone(Timezone)).strftime("%Y%m%d_%H%M%S")
        # UTC Time
        data_id = date_time
        item = Form_db(key_name=data_id)
        item.data_id = data_id
      # - -
        item.post_title = self.request.get('post_title')
        item.post_body = self.request.get('post_body')
      #
        item.put()
        time.sleep(1)
        self.redirect('/posts')

class deleteData(webapp2.RequestHandler):
    def get(self):
        page_address = self.request.uri
        base = os.path.basename(page_address)
        data_id = base.split('?')[1]
        if users.is_current_user_admin():
            item = db.Query(Form_db).filter('data_id =', data_id).get()
        item.delete()
        time.sleep(1)
        self.redirect('../../list/entries')


class publicSite(webapp2.RequestHandler):
    def get(self):
      # - page url
        page_address = self.request.uri
        # Universal Resource Identifier
        # vs. URL : similar, type of URI, a location rather than identifier 
        path_layer = urlparse(page_address)[2].split('/')[1]
        # split is a python method
        # working w/ data, manipulating DB, in and out, render
        # components = array = datatype lists
        # 2 is the path, all the slashes are splitting, turining string into array, grab the 2nd (1) 
        base = os.path.basename(page_address)
        # changes ~~~ w/ combination of CSS in 27 of public
      # - user
        user = users.get_current_user()
        if users.get_current_user(): # - logged in
            login_key = users.create_logout_url(self.request.uri)
            gate = 'Sign out'
            user_name = user.nickname()
        else: # - logged out
            login_key = users.create_login_url(self.request.uri)
            gate = 'Sign in'
            user_name = 'No User'
      # - app data
        app = Site
        page_name = 'Main'
        page_id = 'main'
        analytics = Analytics
        page_html = main_page_html
        admin = ''
        if users.is_current_user_admin():
            admin = 'true'

        if path_layer == 'posts':
            page_id = 'posts'
            page_name = 'Posts'
            page_html = posts_page_html

 
               
      # - template
        objects = {
            'Site': app,
            'analytics': analytics,
            'login_key': login_key,
            'gate': gate,
            'user_name': user_name,
            'admin': admin,
          # -
            'path_layer': path_layer,
            'base': base,
            'page_name': page_name,
            'page_id': page_id,
            'page_html': page_html,
            
        }
      # - render
        path = os.path.join(os.path.dirname(__file__), 'html/publicSite.html')
        self.response.out.write(template.render(path, objects))


class listData(webapp2.RequestHandler):
    def get(self):
        page_address = self.request.uri
        base = os.path.basename(page_address)
        if users.is_current_user_admin():
            if base == 'entries':
                q = db.Query(Form_db, projection=('data_id', 'email_address', 'user_name'))
                db_data = q.order('-addTime').fetch(50)
        data = []
        for f in db_data:
            data.append(db.to_dict(f))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))


app = webapp2.WSGIApplication([    # - Pages
    ('/', publicSite),
    ('/posts/?', publicSite),



], debug=True)

