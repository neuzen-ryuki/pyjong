# sys
import os
import pickle
from typing import List

# ours
from tile_type import TileType


class ShantenTable :

    def __init__(self, file_path:str = "", record_mode:bool = False) :
        self.file_path = file_path
        self.record_mode = record_mode

        # normal handの向聴数計算用．複数の関数をまたいで使うのでここで定義．
        self.shanten_num = 8
        self.shanten_temp = 8
        self.opened_sets_num = 0
        self.hand = [0] * 38
        self.pairs_num = 0
        self.tahtsu_num = 0
        self.sets_num = 0

        # 向聴数を記録するハッシュテーブル
        if (os.path.exists(file_path)) :
            self.shanten_table = pickle.load(file_path)
        else :
            self.shanten_table = {}


    # 手牌をハッシュして得られるキーを用いて向聴テーブルに登録された向聴数を返す
    # キーが登録されていなかった場合向聴数を計算してテーブルに登録
    # ※ handは直接の参照を渡すのではなくコピーを渡す
    # ※ ロン和了の場合は和了牌もhandに加えて渡す
    def get_shanten_num(self, hand:List[int], opened_sets_num:int) -> int :
        self.hand = hand
        self.opened_sets_num = opened_sets_num

        shanten_num = self.shanten_table.get(tuple(hand))
        if (shanten_num is None) :
            shanten_num = self._calc_shanten_num()
            self.shanten_table[key] = shanten_num
            if self.record_mode : self.dump()

        return shanten_num


    # 向聴テーブルをダンプ
    def dump_table() -> None :
        pickle.dump(self.shanten_table, self.file_path)


    # handの向聴数を計算
    def _calc_shanten_num(self) -> int :
        if self.opened_sets_num > 0 :
            kokushi = 13
            chiitoi = 6
        else :
            kokushi = self._calc_shanten_num_of_kokushi()
            chiitoi = self._calc_shanten_num_of_chiitoi()
        normal = self._calc_shanten_num_of_normal()

        return min((kokushi, chiitoi, normal))


    # 国士無双の向聴数を返す
    def _calc_shanten_num_of_kokushi(self) -> int :
        pairs_num = 0
        shanten_num = 13

        for i in (TileType.TERMINALS | TileType.HONORS) :
            if self.hand[i] != 0 : shanten_num -= 1
            if self.hand[i] > 1 and pairs_num == 0 : pairs_num = 1
        shanten_num -= pairs_num

        return shanten_num


    # 七対子の向聴数を返す
    def _calc_shanten_num_of_chiitoi(self) -> int :
        shanten_num = 6
        kind = 0 # 6対子あっても孤立牌がないと聴牌にならないのでそれのチェック用

        for i in range(1,38) :
            if self.hand[i] >= 1 :
                kind += 1
            if self.hand[i] >= 2 :
                shanten_num -= 1
        if kind < 7 :
            shanten_num += 7 - kind

        return shanten_num


    # 通常手の向聴数を返す
    def _calc_shanten_num_of_normal(self) -> int :
        self.shanten_num = 8
        self.pairs_num = 0
        self.tahtsu_num = 0
        self.sets_num = 0

        for i in range(1,38) :
            if self.hand[i] >= 2 :
                self.pairs_num += 1
                self.hand[i] -= 2
                self._pick_out_sets(1)
                self.hand[i] += 2
                self.pairs_num -= 1
        self._pick_out_sets(1)

        return self.shanten_num


    # 面子を抜き出す
    def _pick_out_sets(self, i:int) -> None :
        while i < 38 and self.hand[i] == 0 : i += 1
        if i > 37 :
            self._pick_out_tahtsu(1)
            return
        if self.hand[i] > 2 :
            self.sets_num += 1
            self.hand[i] -= 3
            self._pick_out_sets(i)
            self.hand[i] += 3
            self.sets_num -= 1
        if  i < 28 and self.hand[i+1] > 0 and self.hand[i+2] > 0 :
            self.sets_num += 1
            self.hand[i] -= 1
            self.hand[i+1] -= 1
            self.hand[i+2] -= 1
            self._pick_out_sets(i)
            self.hand[i] += 1
            self.hand[i+1] += 1
            self.hand[i+2] += 1
            self.sets_num -= 1
        self._pick_out_sets(i+1)


    # 塔子を抜き出す
    def _pick_out_tahtsu(self, i:int) -> None :
        while i < 38 and self.hand[i] == 0 : i += 1
        if i > 37 :
            self.shanten_temp = 8 - (self.sets_num + self.opened_sets_num) * 2 - self.tahtsu_num - self.pairs_num
            if self.shanten_temp < self.shanten_num :
                self.shanten_num = self.shanten_temp
            return
        if self.sets_num + self.tahtsu_num < 4 :
            if self.hand[i] == 2 :
                self.tahtsu_num += 1
                self.hand[i] -= 2
                self._pick_out_tahtsu(i)
                self.hand[i] += 2
                self.tahtsu_num -= 1
            if i < 29 and self.hand[i+1] != 0 :
                self.tahtsu_num += 1
                self.hand[i] -= 1
                self.hand[i+1] -= 1
                self._pick_out_tahtsu(i)
                self.hand[i] += 1
                self.hand[i+1] += 1
                self.tahtsu_num -= 1
            if i < 29 and i % 10 < 9 and self.hand[i+2] != 0 :
                self.tahtsu_num += 1
                self.hand[i] -= 1
                self.hand[i+2] -= 1
                self._pick_out_tahtsu(i)
                self.hand[i] += 1
                self.hand[i+2] += 1
                self.tahtsu_num -= 1
        self._pick_out_tahtsu(i+1)