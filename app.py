from flask import Flask
from flask import jsonify
from flask_executor import Executor
import longjob


app = Flask(__name__)
app.config["EXECUTOR_TYPE"] = "process"
executor = Executor()
executor.init_app(app)

longjob.createTable()


@app.route("/")
def hello_world():
    executor.submit_stored("demo", longjob.longjob)
    return "<p>Hello, World!</p>"

@app.route('/status')
def get_status():
    if not executor.futures.done("demo"):
        return jsonify({"status": executor.futures._state("demo")})
    future = executor.futures.pop("demo")
    return jsonify({"status": "done", 'result': future.result()})