app = Flask(__name__)
app.secret_key = os.urandom(24)
file_path = os.path.abspath(os.getcwd())+"/DataBases/test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False
db = SQLAlchemy(app)
