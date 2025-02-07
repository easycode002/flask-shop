import os, sys
from config.config import Config,DevelopmentConfig,ProductionConfig,TestingConfig
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env = os.getenv('FLASK_ENV','development')

if env == 'production':
    config = ProductionConfig()
elif env == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig();
    
print(f"Using {env} configuration")