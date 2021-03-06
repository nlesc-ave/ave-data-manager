import os
from urllib.parse import urlparse

import connexion
from flask_cors import CORS
from pkg_resources import resource_filename

from .version import __version__

connexion_app = connexion.FlaskApp(__name__, specification_dir='../')
app = connexion_app.app
CORS(app)

app.config.update(dict(
    # File path for database
    DATABASE='ave.db',
    # Maximum number of base pairs at which haplotype clustering is performed
    MAX_RANGE=50000,
    # Directory to store whoosh full text indices
    WHOOSH_BASE_DIR='.',
))
app.config.from_pyfile(os.path.join(os.getcwd(), 'settings.cfg'), silent=True)


def spec_config():
    conf = {'VERSION': __version__}
    return conf


swagger_file = resource_filename(__name__, 'swagger.yml')
connexion_app.add_api(swagger_file, arguments=spec_config())
