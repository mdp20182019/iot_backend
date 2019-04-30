import os


from flask import Flask, request,jsonify
from flask_cors import CORS



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/send')
    def hello():
        from . import db
        db.sendData()
        data={"Message": "Success"}
        return jsonify(data)

    @app.route('/login', methods=['POST'])
    def login():
        from . import db
        data = request.get_json()
        print(data)
        result=db.login(data)
        print("?????????????????")
        print(result)
        return jsonify(result)


    @app.route('/getdata')
    def getdata():
        from . import db
        db.get_documents("mesureAck100")
        return "ok"


    @app.route('/receive', methods=['POST'])
    def add():
        data = request.get_json()
        print(data)
        data = jsonify(data)
        print(data)
        return "Success"

    @app.route('/collectionsUrl')
    def collectionsUrl():
        from . import db
        r = db.getCollectionsUrl()
        return jsonify(r)

    @app.route('/createMeasure', methods=['POST'])
    def createMeasure():
        from . import db
        data = request.get_json()
        print(data)
        result = db.getMeasureJson(data['startDate'],data['endDate'],data['MeasureName'],data['creator'],data['TypeOfMeasure'])
        print("Success")
        return jsonify(result)

    @app.route('/save', methods=['POST'])
    def saveData():
        from . import db
        data = request.get_json()
        db.saveToMongo(data)
        print(data)
        return jsonify("Success")

    @app.route('/history')
    def gethistory():
        from . import db
        r = db.getHistory()
        print(type(r))
        return jsonify(r)

    from . import returnData
    app.register_blueprint(returnData.bp)

    return app
