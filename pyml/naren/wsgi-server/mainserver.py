#coding:utf8
import textwrap
import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import ConfigParser
import pdb
reload(sys)
import tornado.web
sys.setdefaultencoding('utf8')
from position import handleposition
from profile import handleprofile
from model import generate_feature
from model import gbdt_model
from nanabase import baseutil as nautil

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define('path', default='data', help='store the data', type=str)
define('database', default='fkmodelt', help='the database name', type=str)


def decode_body(body):
    try:
        body = eval(body)
        return body
    except:
        bodys = body.split('&')
        body_dct = []
        nautil.dlog.exception('ModelTrainHandler')

class update_restart(tornado.web.RequestHandler):
    def get(self):
        try:
            import subprocess
            _cur_dir = os.path.realpath(os.curdir)
            cmdline = "svn up %s" % _cur_dir
            lines = subprocess.check_output(cmdline, shell=True)
            return_lines = ["<html><body>"]
            lines = lines.splitlines()
            return_lines.extend(lines)
            if not lines[-1].startswith("Updated"):
                return_lines.append("NO new code found in SVN, the server will NOT restart")
                return_lines.append("</body></html>")
                self.write('<br>'.join(return_lines))
                return
            return_lines.append("the server will restart in seconds ..... ")
            return_lines.append("</body></html>")
            self.write('<br>'.join(return_lines))
            self.flush()
            subprocess.Popen("./restart.sh", shell=True)
            return
        except Exception, e:
            self.write('exception occurred1 %s' % str(e))
            nautil.dlog.exception('ModelTrainHandler')
            return

class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])


class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


class ProfileHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        body = eval(body)
        profile_json = body['profile']
        company_id = body.get('pos_id', None)
        database = options.database
        # pdb.set_trace()
        try:
            handleprofile.insert_profile(profile_json, database, company_id)
            self.write({'err_code':0})
        except:
            self.write({'err_code':6665})
            nautil.dlog.exception('ModelTrainHandler')


class PositionHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        body = eval(body)
        position_json = body['company']
        database_name = options.database
        try:
            handleposition.insert_company(position_json, database_name)
            self.write({'err_code':0})
        except:
            self.write({'err_code':6665})
            nautil.dlog.exception('ModelTrainHandler')


class PositionResumeHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        body = eval(body)
        rst = handleprofile.check_position_resume(body)
        if len(rst) == 1:
            handleprofile.update_profile(body)
        self.write(rst)


class ModelHandler(tornado.web.RequestHandler):

    def post(self):
        body = self.request.body
        body = eval(body)
        action = body['action']
        pdb.set_trace()
        if action == 'train':
            generate_feature.generate_train(options.path)
            gbdt_model.train_model()
            self.write({'err_code':0})
        else:
            database = options.database
            position_json = body['company']
            handleposition.insert_company(position_json, database, tablename='companytest')
            profile_json = body['profile']
            handleprofile.insert_profile(profile_json, database, test='test')
            pos_id = position_json['position_id']
            resume_id = profile_json['resume_id']
            # pos_id = body['pos_id']
            # resume_id = body['resume_id']
            score = gbdt_model.predict_data(int(pos_id), resume_id)
            self.write({'err_code':0, 'predict_score':score})


if __name__ == "__main__":
    import time
    print 'time is %s' % time.strftime("%Y-%m-%d %H:%M:%S")
    tornado.options.parse_command_line()
    cf = ConfigParser.ConfigParser()

    cf.read('server.ini')
    data_path = cf.get('servers', 'datapath')
    port = cf.get('servers', 'port')
    options.port = int(port)
    options.path = data_path

    settings = {
        "debug": True
    }

    app = tornado.web.Application(
        handlers=[
            (r'/update_restart', update_restart),
            (r"/profile", ProfileHandler),
            (r"/pos_resume", PositionResumeHandler),
            (r"/position", PositionHandler),
            (r"/model", ModelHandler)
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    # pdb.set_trace()
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
