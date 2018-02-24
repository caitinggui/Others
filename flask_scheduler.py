# coding: utf-8

'''
在flask中用threading的Timer开启定时任务，有两种方式，一种在before_first_request中，一种在main中
- 在before_fisrt_request时，每个进程都会有这个任务，容易造成冲突
- 在main中时，会造成uwsgi要很久才能中止，并且其他worker无法影响master的状态，造成任务一直无法取消
但是两种方式都需要uwsgi开启threads（如果用uwsgi运行flask的话）
uwsgi --http-socket :1337 --wsgi-file flask_scheduler.py --callable app --master --processes 8 --threads 2
所以最终两个都不行
'''


from threading import Timer
import logging

from flask import Flask, jsonify

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/api/<method>")
def api(method):
    data = {
      'foo': 'bar',
      'method': method
    }
    response = jsonify(data)
    response.status_code = 200
    return response


@app.route('/status', methods=["GET"])
def getTaskStatus():
    logging.info("check taks...")
    if hasattr(app, 'scheduler'):
        if app.scheduler.task.isAlive():
            return "The task is still alive"
        else:
            return "The task is killed"
    else:
        return "You should add scheduler to app first"


@app.route("/restart", methods=["GET"])
def restartTask():
    logging.info("restart task...")
    if hasattr(app, 'scheduler'):
        try:
            app.scheduler.stop()
        except Exception as e:
            logging.exception(e)
        app.scheduler.start()
        return "The task restart successfully"
    else:
        return "You should add scheduler to app first"


@app.route("/cancel", methods=["GET"])
def cancelTask():
    logging.info("cancel task...")
    if hasattr(app, 'scheduler'):
        app.scheduler.stop()
        logging.info(app.scheduler.task)
        return "The task cancel successfully"
    else:
        return "You should add scheduler to app first"
# 采用钩子，每个进程都会运行
# @app.before_first_request
# def startTask():
    # app.scheduler = Scheduler(1, query_db)
    # # import ipdb; ipdb.set_trace()
#     app.scheduler.start()


class Scheduler(object):
    def __init__(self, sleep_time, function):
        self.sleep_time = sleep_time
        self.function = function
        self._t = None

    def start(self):
        logging.info("task _t: %s", self._t)
        if self._t is None:
            self._t = Timer(self.sleep_time, self.function)
            self._t.start()
        else:
            logging.error("Other tasks is running")
            raise Exception("this timer is already running")

    def stop(self):
        logging.info(self._t)
        if self._t is not None:
            logging.info("cancel task!")
            self._t.cancel()
            self._t = None

    @property
    def task(self):
        return self._t


def query_db():
    logging.info("IM QUERYING A DB")
    with open('/tmp/test.py', 'a') as f:
        f.write('4')


# 只有一个定时任务开启
app.scheduler = Scheduler(5, query_db)
# import ipdb; ipdb.set_trace()
app.scheduler.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
    app.scheduler.stop()

