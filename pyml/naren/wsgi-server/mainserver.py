#coding:utf8
import textwrap

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

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define('path', default='data', help='store the data', type=str)
define('database', default='fkmodel', help='the database name', type=str)


def decode_body(body):
    try:
        body = eval(body)
        return body
    except:
        bodys = body.split('&')
        body_dct = []


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
        try:
            handleprofile.insert_profile(profile_json, database, company_id)
            self.write({'err_code':0})
        except:
            self.write({'err_code':6665})


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



class PositionResumeHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        body = eval(body)
        rst = handleprofile.check_position_resume(body)
        if len(rst) == 0:
            handleprofile.update_profile(body)
        self.write(rst)


class ModelHandler(tornado.web.RequestHandler):

    def post(self):
        body = self.request.body
        pdb.set_trace()
        body = eval(body)
        action = body['action']
        if action == 'train':
            generate_feature.generate_train(options.path)
            gbdt_model.train_model()
            self.write({'err_code':0})
        else:
            pos_id = body['pos_id']
            resume_id = body['resume_id']
            score = gbdt_model.predict_data(pos_id, resume_id)
            self.write({'err_code':0, 'predict_score':score})


if __name__ == "__main__":
    tornado.options.parse_command_line()
    cf = ConfigParser.ConfigParser()

    cf.read('server.ini')

    data_path = cf.get('servers', 'datapath')
    port = cf.get('servers', 'port')
    options.port = int(port)
    options.path = data_path

    app = tornado.web.Application(
        handlers=[
            (r"/profile", ProfileHandler),
            (r"/pos_resume", PositionResumeHandler),
            (r"/position", PositionHandler),
            (r"/model", ModelHandler)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    # pdb.set_trace()
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
