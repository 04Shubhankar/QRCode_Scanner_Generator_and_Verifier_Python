def logger(logmsg):
    import logging
    # Create a logger instance
    logger = logging.getLogger(__name__)  
    logger.setLevel(logging.INFO)  # Set logger level to INFO

    # Check if the handler is already added
    if not logger.handlers:
        # Create a file handler for logging
        f_handler = logging.FileHandler('log.txt')  
        f_handler.setLevel(logging.INFO)  # Set file handler level to INFO
        # Create a formatter and attach it to the handler
        f_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')  
        f_handler.setFormatter(f_format)
        # Attach the file handler to the logger
        logger.addHandler(f_handler)  
    
    # Log a message
    logger.info(logmsg)  # This will now be logged in 'log.txt'
    logger.info("------------------------")
