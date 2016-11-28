# coding: utf-8

from enum import Enum
import random

from configure.config import INIT
from utils import signalConverter


def decide_next_luminosity_ikeda7(ils):
    """
    池田さんの修論で使われている7近傍の方式です
    :param ils: 知的照明システムのオブジェクト
    :return: None
    """

    # 各照明ごとに次光度を決定する手順を実行
    for l in ils.lights:
        neighbor_type = NeighborType7.default
        distance_rank = []
        for i in range(len(ils.sensors)):
            distance_rank.append(DistanceRank7.default)

        # 各センサに対する照度光度影響度を取得
        influence = l.influence[:]

        for s_i, s in enumerate(ils.sensors):
            # 離席してるセンサの影響度は0にする
            if not s.attendance:
                influence[s_i] = 0.0

            # センサの距離でランク付けする
            if influence[s_i] > 0.20:
                ils.sensors[s_i].tmp_rank = DistanceRank7.rank1
            elif influence[s_i] > 0.15:
                ils.sensors[s_i].tmp_rank = DistanceRank7.rank2
            elif influence[s_i] > 0.10:
                ils.sensors[s_i].tmp_rank = DistanceRank7.rank3
            else:
                ils.sensors[s_i].tmp_rank = DistanceRank7.noRank
            ############################
            # メモ
            #   BACnet...
            #   rank1 -> 0.21
            #   rank2 -> 0.11
            #   rank3 -> 0.05


        # 影響するセンサの数（NoRankじゃないもの）を数える
        influential_sensors = []
        unsatisfied_sensors = []
        for s_i, s in enumerate(ils.sensors):
            if s.tmp_rank != DistanceRank7.noRank:
                influential_sensors.append(ils.sensors[s_i])

        if len(influential_sensors) == 0:
            # 影響するセンサが存在しない場合
            neighbor_design = NeighborDesign.design1
            use_rank = DistanceRank7.noRank
        elif len(influential_sensors) == 1:
            uns_sss = influential_sensors[0]
            # 影響するセンサが1つしかない場合
            if uns_sss.illuminance < uns_sss.target:
                # 目標照度を上回っていない場合
                if 0.98 * uns_sss.target <= uns_sss.illuminance < uns_sss.target:
                    neighbor_design = NeighborDesign.design6
                    use_rank = uns_sss.tmp_rank
                else:
                    if 0.92 * uns_sss.target < uns_sss.illuminance < uns_sss.target * 0.98:
                        neighbor_design = NeighborDesign.design5
                        use_rank = uns_sss.tmp_rank
                    else:
                        neighbor_design = NeighborDesign.design4
                        use_rank = uns_sss.tmp_rank
            else:
                # 目標照度を上回っている場合
                if uns_sss.illuminance > 1.06 * uns_sss.target:
                    neighbor_design = NeighborDesign.design3
                    use_rank = uns_sss.tmp_rank
                else:
                    neighbor_design = NeighborDesign.design2
                    use_rank = uns_sss.tmp_rank
        else:
            # 影響するセンサが複数個ある場合
            for inf_s in influential_sensors:
                # 目標照度を達成していないセンサをリストアップ
                if inf_s.illuminance < inf_s.target:
                    unsatisfied_sensors.append(inf_s)
            if len(unsatisfied_sensors) == 0:
                # 影響するすべてのセンサが目標照度を上回っている場合
                # 影響するすべてのセンサが最小可視変動比以内かチェック
                flag_up_ok = True
                for inf_ss in influential_sensors:
                    if inf_ss.illuminance > 1.06 * inf_ss.target:
                        flag_up_ok = False
                if flag_up_ok:
                    # 最小可視変動比以内にある場合
                    neighbor_design = NeighborDesign.design2
                    use_rank = influential_sensors[0].tmp_rank
                    for inf_sss in influential_sensors:
                        if inf_sss.tmp_rank.value < use_rank.value:
                            use_rank = inf_sss.tmp_rank
                else:
                    # 最小可視変動比以内にないすなわち大きく目標照度を上回っている場合
                    neighbor_design = NeighborDesign.design3
                    use_rank = influential_sensors[0].tmp_rank
                    for inf_sss in influential_sensors:
                        if inf_sss.tmp_rank.value < use_rank.value:
                            use_rank = inf_sss.tmp_rank
            else:
                # 影響するセンサの中に目標照度を満たしていないものがある場合
                # 目標照度を満たしていないすべてのセンサがほぼ目標照度付近にあるかチェック
                flag_near = True
                for uns_s in unsatisfied_sensors:
                    if not 0.98 * uns_s.target <= uns_s.illuminance < uns_s.target:
                        flag_near = False
                if flag_near:
                    # ほぼ目標照度付近にある場合
                    neighbor_design = NeighborDesign.design6
                    use_rank = influential_sensors[0].tmp_rank
                    for uns_ssss in influential_sensors:
                        if uns_ssss.tmp_rank.value < use_rank.value:
                            use_rank = uns_ssss.tmp_rank
                else:
                    # 最小可視変動比内にとどまっているかどうかをチェック
                    flag_under_ok = True
                    for uns_ss in unsatisfied_sensors:
                        if not 0.92 * uns_ss.target < uns_ss.illuminance < 0.98 * uns_ss.target:
                            flag_under_ok = False
                    # 目標照度を満たしていないすべてのセンサが最小可視変動比内にある場合
                    if flag_under_ok:
                        neighbor_design = NeighborDesign.design5
                        use_rank = influential_sensors[0].tmp_rank
                        for uns_ssss in influential_sensors:
                            if uns_ssss.tmp_rank.value < use_rank.value:
                                use_rank = uns_ssss.tmp_rank
                    else:
                        neighbor_design = NeighborDesign.design4
                        use_rank = influential_sensors[0].tmp_rank
                        for uns_ssss in influential_sensors:
                            if uns_ssss.tmp_rank.value < use_rank.value:
                                use_rank = uns_ssss.tmp_rank

        # NeighborDesignとuse_rankからNeighborType7を決定する
        if neighbor_design == NeighborDesign.design1:
            neighbor_type = NeighborType7.typeA
        elif neighbor_design == NeighborDesign.design2:
            if use_rank == DistanceRank7.rank1:
                neighbor_type = NeighborType7.typeD
            elif use_rank == DistanceRank7.rank2:
                neighbor_type = NeighborType7.typeC
            elif use_rank == DistanceRank7.rank3:
                neighbor_type = NeighborType7.typeB
            else:
                print("おかしい．")
        elif neighbor_design == NeighborDesign.design3:
            if use_rank == DistanceRank7.rank1:
                neighbor_type = NeighborType7.typeC
            elif use_rank == DistanceRank7.rank2:
                neighbor_type = NeighborType7.typeB
            elif use_rank == DistanceRank7.rank3:
                neighbor_type = NeighborType7.typeA
            else:
                print("おかしい")
        elif neighbor_design == NeighborDesign.design4:
            if use_rank == DistanceRank7.rank1:
                neighbor_type = NeighborType7.typeG
            elif use_rank == DistanceRank7.rank2:
                neighbor_type = NeighborType7.typeF
            elif use_rank == DistanceRank7.rank3:
                neighbor_type = NeighborType7.typeE
            else:
                print("おかしい")
        elif neighbor_design == NeighborDesign.design5:
            if use_rank == DistanceRank7.rank1:
                neighbor_type = NeighborType7.typeF
            elif use_rank == DistanceRank7.rank2:
                neighbor_type = NeighborType7.typeE
            elif use_rank == DistanceRank7.rank3:
                neighbor_type = NeighborType7.typeD
            else:
                print("おかしい")
        elif neighbor_design == NeighborDesign.design6:
            if use_rank == DistanceRank7.rank1:
                neighbor_type = NeighborType7.typeE
            elif use_rank == DistanceRank7.rank2:
                neighbor_type = NeighborType7.typeD
            elif use_rank == DistanceRank7.rank3:
                neighbor_type = NeighborType7.typeC
            else:
                print("おかしい")
        else:
            print("くそおかしい")

        # neighbor_typeから次光度決定乱数の上限と下限を設定する
        rnd_up = 0.0
        rnd_dn = 0.0

        if neighbor_type == NeighborType7.typeA:
            rnd_up = 1.0
            rnd_dn = -10.0
        elif neighbor_type == NeighborType7.typeB:
            rnd_up = 3.0
            rnd_dn = -7.0
        elif neighbor_type == NeighborType7.typeC:
            rnd_up = 3.0
            rnd_dn = -5.0
        elif neighbor_type == NeighborType7.typeD:
            rnd_up = 2.0
            rnd_dn = -2.0
        elif neighbor_type == NeighborType7.typeE:
            rnd_up = 5.0
            rnd_dn = -3.0
        elif neighbor_type == NeighborType7.typeF:
            rnd_up = 7.0
            rnd_dn = -2.0
        elif neighbor_type == NeighborType7.typeG:
            rnd_up = 12.0
            rnd_dn = -1.0
        else:
            print("おそろしい事が起きました")

        l.neighbor = str(neighbor_type)

        change_rate = random.randint(rnd_dn, rnd_up)

        # 次光度を決定
        l.previous_luminosity = l.luminosity
        l.next_luminosity = l.luminosity * (100.0 + change_rate) / 100.0
        if l.next_luminosity > INIT.LIGHT_LUMINOSITY_MAX[0]:
            l.next_luminosity = INIT.LIGHT_LUMINOSITY_MAX[0]
        elif l.next_luminosity < INIT.LIGHT_LUMINOSITY_MIN[0]:
            l.next_luminosity = INIT.LIGHT_LUMINOSITY_MIN[0]

    for l in ils.lights:
        l.luminosity = l.next_luminosity
        signalConverter.convert_to_signal(ils.lights)


class NeighborType7(Enum):
    default = 0
    typeA = 1
    typeB = 2
    typeC = 3
    typeD = 4
    typeE = 5
    typeF = 6
    typeG = 7

    def __str__(self):
        if self == NeighborType7.typeA:
            return "TYPE A"
        elif self == NeighborType7.typeB:
            return "TYPE B"
        elif self == NeighborType7.typeC:
            return "TYPE C"
        elif self == NeighborType7.typeD:
            return "TYPE D"
        elif self == NeighborType7.typeE:
            return "TYPE E"
        elif self == NeighborType7.typeF:
            return "TYPE F"
        elif self == NeighborType7.typeG:
            return "TYPE G"


class NeighborDesign(Enum):
    default = 0
    design1 = 1
    design2 = 2
    design3 = 3
    design4 = 4
    design5 = 5
    design6 = 6

    def __str__(self):
        if self == NeighborDesign.design1:
            return "DESIGN 1"
        elif self == NeighborDesign.design2:
            return "DESIGN 2"
        elif self == NeighborDesign.design3:
            return "DESIGN 3"
        elif self == NeighborDesign.design4:
            return "DESIGN 4"
        elif self == NeighborDesign.design5:
            return "DESIGN 5"
        elif self == NeighborDesign.design6:
            return "DESIGN 6"


class DistanceRank7(Enum):
    default = 0
    rank1 = 1
    rank2 = 2
    rank3 = 3
    noRank = 10

    def __str__(self):
        if self == DistanceRank7:
            return "!default"
        elif self == DistanceRank7.rank1:
            return "RANK 1st"
        elif self == DistanceRank7.rank2:
            return "RANK 2nd"
        elif self == DistanceRank7.rank3:
            return "RANK 3rd"
        elif self == DistanceRank7.noRank:
            return "NO RANK"
