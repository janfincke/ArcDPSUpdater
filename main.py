import logging
import traceback
from updater import ArcDpsUpdater
try:
    updater = ArcDpsUpdater()
    updater.check_for_updates()
except Exception as e:
    logging.error(traceback.format_exc())
    raw_input('Press any key to continue...')
    raise SystemExit
