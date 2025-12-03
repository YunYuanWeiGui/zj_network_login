if __name__ == "__main__":
    import zj_network
    from ping3 import ping
    import time, datetime, chinese_calendar

    user_data = zj_network.user_data()
    if user_data:
        USERNAME, PASSWORD, PROVIDER = user_data

        # 日志
        import logging
        from logging.handlers import TimedRotatingFileHandler

        log_format = logging.Formatter("%(asctime)s\t%(levelname)s:\t%(message)s")
        # 控制台日志
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)
        # 文件日志
        file_handler = TimedRotatingFileHandler("zj_login.log", encoding="utf-8", when="M", interval=1, backupCount=12)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)

        # logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
        logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])

        logging.info("已开始运行……")
        while True:
            if not ping('8.8.8.8'):
                if zj_network.login(USERNAME, PASSWORD, PROVIDER):
                    logging.info("✅ 登陆成功")
                else:
                    logging.info("❌ 登录失败")
                    if not (6 <= time.localtime().tm_hour <= 23 and
                            ((datetime.date.today() + datetime.timedelta(days=1)).weekday() >= 5 or
                            chinese_calendar.is_holiday(datetime.date.today() + datetime.timedelta(days=1)))):
                        logging.info("❌ 不在认证时段内！")
                        if time.localtime()。tm_hour >= 23:
                            time.sleep(((24 - time.localtime().tm_hour + 6) * 60 - time.localtime().tm_min - 1) * 60)
                        elif time.localtime()。tm_hour < 6:
                            time.sleep(((6 - time.localtime().tm_hour) * 60 - time.localtime().tm_min - 1) * 60)
            try:
                time.sleep(60)
            except KeyboardInterrupt:
                logging.info("已结束运行……")
                break
    else:
        print("配置 zj_account.ini 后重启正常使用")
        while True:
            try:
                time.sleep(24 * 60 * 60)
            except KeyboardInterrupt:
                break
