# coding: utf-8

from configure.config import INIT


def convert_to_luminosity(lights):
    u"""信号値を光度値に変換する"""

    # 1次関数の傾き
    factor = (INIT.LIGHT_LUMINOSITY_MAX[0] - INIT.LIGHT_LUMINOSITY_MIN[0]) / \
             (float(INIT.LIGHT_SIGNAL_MAX[0]) - float(INIT.LIGHT_SIGNAL_MIN[0]))
    # 1次関数の切片
    intercept = INIT.LIGHT_LUMINOSITY_MAX[0] - factor * float(INIT.LIGHT_SIGNAL_MAX[0])

    # for BACnet Mitsubishi LED
    for l in lights:
        # l.luminosity = int(-0.0130119460805247 * float(l.signals[0]) * float(l.signals[0]) + 13.9104144531693 *
        #                    float(l.signals[0]) - 40.0024478040349)
        # l.luminosity = int(13.79 * float(l.signals[0]))

        l.luminosity = l.signals[0] * factor + intercept


def convert_to_signal(lights):
    u"""光度値を信号値に変換する"""

    # for BACnet Mitsubishi LED
    if INIT.MODE_TEMPERATURE:
        # 1次関数の傾き
        factor = (INIT.LIGHT_SIGNAL_MAX[0] - INIT.LIGHT_SIGNAL_MIN[0]) / \
                 (INIT.LIGHT_LUMINOSITY_MAX[0] - INIT.LIGHT_LUMINOSITY_MIN[0])
        # 1次関数の切片
        intercept = INIT.LIGHT_SIGNAL_MAX[0] - factor * float(INIT.LIGHT_LUMINOSITY_MAX[0])

        for l in lights:
            # l.signals[0] = int(0.00000664944924261323 * float(l.luminosity) * float(l.luminosity) +
            #                    0.0711852025585447 * float(l.luminosity) + 3.06397372065703)
            # l.signals[0] = int(100.0 / 1379.0 * float(l.luminosity))
            for lum_s, lum in enumerate(l.luminosities):
                l.signals[lum_s] = int(lum * factor + intercept)
    else:
        # 1次関数の傾き
        factor = (INIT.LIGHT_SIGNAL_MAX[0] - INIT.LIGHT_SIGNAL_MIN[0]) / \
                 (INIT.LIGHT_LUMINOSITY_MAX[0] - INIT.LIGHT_LUMINOSITY_MIN[0])
        # 1次関数の切片
        intercept = INIT.LIGHT_SIGNAL_MAX[0] - factor * float(INIT.LIGHT_LUMINOSITY_MAX[0])

        for l in lights:
            # l.signals[0] = int(0.00000664944924261323 * float(l.luminosity) * float(l.luminosity) +
            #                    0.0711852025585447 * float(l.luminosity) + 3.06397372065703)
            # l.signals[0] = int(100.0 / 1379.0 * float(l.luminosity))

            l.signals[0] = int(l.luminosities[0] * factor + intercept)
