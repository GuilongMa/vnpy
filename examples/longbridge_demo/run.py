from vnpy.event import EventEngine
from vnpy.trader.constant import Currency
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import create_qapp, MainWindow

from vnpy.vnpy_longbridge import LongBridgeGateway


import os

# 环境变量 LONGPORT_REGION=cn 来使用中国大陆的接入点，当前我们仅有 hk 和 cn 两个地区可选
os.environ['LONGPORT_REGION'] = 'cn'

# 获取环境变量
# value = os.environ.get('MY_VAR')
# print(value)  # 输出 'my_value'


def main():
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    gw = main_engine.add_gateway(LongBridgeGateway)
    if isinstance(gw, LongBridgeGateway):
        lb_gw: LongBridgeGateway = gw
        lb_gw.currency = Currency.USD
        lb_gw.main_engine = main_engine

        def subscribe():
            lb_gw.subscribe_symbols(["SPY.US", "QQQ.US", "NVDA.US"])
            lb_gw.load_contract(["NVDA.US", "ARM.US"])

        lb_gw.after_connect = subscribe

    main_window = MainWindow(main_engine, event_engine)
    main_window.showNormal()

    qapp.exec()


if __name__ == "__main__":
    main()
