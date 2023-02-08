from flask import Flask
from flask import jsonify
from flask_executor import Executor
import longjob


app = Flask(__name__)
app.config["EXECUTOR_TYPE"] = "process"  # 按理说应该用进程版
executor = Executor()
executor.init_app(app)

longjob.createTable()


@app.route("/")
def hello_world():
    """调用longjob.longjob函数，该函数运行15秒，但是这里不会阻塞而是立刻返回响应

    """    
    executor.submit_stored("demo", longjob.longjob)  # demo可以被看做是这个任务的id，之后可以用来查询任务是否完成
    return "<p>Hello, World!</p>" # 实际使用时可以把任务id返回给前端供查询用，你后台只允许一个计算任务的话可以不需要

@app.route('/status')
def get_status():
    """用于查询计算任务状态，可以在前端定时反复查询，然后成功后从数据库取计算结果

    Returns:
        json字符串: 任务已经完成则返回{"status": "done", 'result': null}，因为longjob.longjob没返回值所以变成了null
                    任务未完成则显示{"status": "RUNNING"}
    """
    if not executor.futures.done("demo"):
        return jsonify({"status": executor.futures._state("demo")})
    future = executor.futures.pop("demo")
    return jsonify({"status": "done", 'result': future.result()})