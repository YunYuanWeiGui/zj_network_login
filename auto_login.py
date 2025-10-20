if __name__ == "__main__":
    import zj_network
    from ping3 import ping
    import time

    user_data = zj_network.user_data()
    if user_data:
        USERNAME, PASSWORD, PROVIDER = user_data

        import logging

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename='zj_network.log',
                            filemode='a',
                            encoding='utf-8')

        logging.info("已开始运行……")
        while True:
            if not ping('8.8.8.8'):
                if zj_network.login(USERNAME, PASSWORD, PROVIDER):
                    logging.info("✅ 登陆成功")
                else:
                    logging.info("❌ 登录失败")
                    if not 6 < time.localtime().tm_hour < 23:
                        logging.info("❌ 不在认证时段内！")
                        if time.localtime().tm_hour >= 23:
                            time.sleep(((24 - time.localtime().tm_hour + 6) * 60 - time.localtime().tm_min) * 60)
                        elif time.localtime().tm_hour < 6:
                            time.sleep(((6 - time.localtime().tm_hour) * 60 - time.localtime().tm_min) * 60)
            try:
                time.sleep(60)
            except KeyboardInterrupt:
                logging.info("已结束运行……")
                break
    else:
        print("配置 config.ini 后重启正常使用")
        while True:
            try:
                time.sleep(24 * 60 * 60)
            except KeyboardInterrupt:
                break
