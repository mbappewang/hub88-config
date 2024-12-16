import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, setup_database
from services.main_func import getMatchList, getPageTotal, getMatchInfo, getStatscore_id, insert_matches

logger = logging.getLogger(__name__)

app = create_app()

with app.app_context():
    try:
        results = getMatchList(1, 'ENG', 1, 1)
        data = results.get('data', {})
        pageTotal = getPageTotal(data)
    except Exception as e:
        logger.error(f"Error get pageTotal: {e}")
    for current in range(1, pageTotal+1):
        results = getMatchList(current, 'ENG', 1, 1)
        data = results.get('data', {})
        if not data:
            continue
        matchInfo_list = getMatchInfo(data)
    logger.info(f"Get {len(matchInfo_list)} matches")
    matchInfo_list_finial = []
    for matchInfo in matchInfo_list:
        statscore_id = getStatscore_id(matchInfo,'en')
        if statscore_id is None:
            continue
        matchInfo['statscore_id'] = statscore_id
        matchInfo_list_finial.append(matchInfo)
    logger.info(f"Get {len(matchInfo_list_finial)} matches with statscore_id")
    insert_matches(matchInfo_list_finial)
    logger.info("Insert matches successfully")