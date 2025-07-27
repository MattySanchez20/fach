import logging
from datetime import datetime

from jets import F16, F18
from utils import dogfight
import os


def main():
    """
    Execute a complete dogfight simulation between 2 Jet Fighters.
    """

    # Generate unique log filename with timestamp for this dogfight session
    log_filename = f"dogfight_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Configure logging to write detailed combat information to file
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=f"./logs/{log_filename}",
    )

    # obtain logger instance to pass to functions
    logger = logging.getLogger()

    # Initialize the two competing fighter jets
    logger.info("Initializing jets...")
    fighter1 = F16()
    fighter2 = F18()
    
    dogfight(fighter1=fighter1, fighter2=fighter2, logger=logger)    

if __name__ == "__main__":
    main()
