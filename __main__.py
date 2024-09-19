import sys
from PyQt5.QtWidgets import QApplication
from src.vista.InterfazEPorra import App_EPorra
#from src.logica.Logica_mock import Logica_mock
from src.logica.Logica import Logica
from src.modelo.declarative_base import session, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    # Punto inicial de la aplicación
    engine = create_engine('sqlite:///aplicacion.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    #Base.metadata.create_all(engine)
    #session.close()
    
    logica = Logica()

    app = App_EPorra(sys.argv, logica)
    sys.exit(app.exec_())