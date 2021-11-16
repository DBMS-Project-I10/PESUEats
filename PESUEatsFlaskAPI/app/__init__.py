import os
from psycopg2.extras import RealDictCursor

from app.app import create_app
from app.helper import appconfig

app = create_app()

if appconfig.config['APP_CONFIG']['init'] is True:
    sql_dir = os.path.join(os.path.dirname(os.getcwd()), 'PESUEatsSQL')
    user = appconfig.config['POSTGRES']['user']
    os.system(f'psql -U {user} -a -f "{sql_dir}/setup.sql"')
    os.system(f'psql -U {user} -a -f "{sql_dir}/create.sql"')
    os.system(f'psql -U {user} -a -f "{sql_dir}/insert.sql"')
    