from typing import List
import datetime

from game import Game
from player import Player
from tile_type import TileType


class Logger :

    def __init__(self, is_logging:bool) :
        now = datetime.datetime.now().isoformat()
        self.save_path = f"../data/log/{now}.log"
        self.is_logging = logging
        self.scores = [0] * 4
        self.actions = [[] for i in range(4)]
        self.starting_hands = [[] for i in range(4)]
        self.tiles_player_got = [[] for i in range(4)]


    def register_ankan(self, i_player:int, tile:int) -> None :
        s_tile = str(tile + 10)
        if tile in TileType.FIVES :
            s_rtile = str(51 + (tile // 10))
            self.actions[i_player].append(f"{s_tile}{s_tile}{s_tile}a{s_rtile}")
        else :
            self.actions[i_player].append(f"{s_tile}{s_tile}{s_tile}a{s_tile}")


    def register_kakan(self, i_player:int, tile:int, pos:int, red:bool) -> None :
        s_tile = str(tile + 10)
        if tile in TileType :
            s_rtile = str(51 + (tile // 10))
            if red :
                if pos == 1 : self.actions[i_player].append(f"{s_tile}{s_tile}{s_rtile}k{s_tile}")
                elif pos == 2 : self.actions[i_player].append(f"{s_tile}k{s_tile}{s_tile}{s_rtile}")
                else : self.actions[i_player].append(f"k{s_tile}{s_tile}{s_tile}{s_rtile}")
            else :
                if pos == 1 : self.actions[i_player].append(f"{s_tile}{s_tile}{s_tile}k{s_rtile}")
                elif pos == 2 : self.actions[i_player].append(f"{s_tile}k{s_rtile}{s_tile}{s_tile}")
                else : self.actions[i_player].append(f"k{s_rtile}{s_tile}{s_tile}{s_tile}")
        elif pos == 1 : self.actions[i_player].append(f"{s_tile}{s_tile}k{s_tile}{s_tile}")
        elif pos == 2 : self.actions[i_player].append(f"{s_tile}k{s_tile}{s_tile}{s_tile}")
        else : self.actions[i_player].append(f"k{s_tile}{s_tile}{s_tile}{s_tile}")


    def register_daiminkan(self, i_player:int, tile:int, pos:int) -> None :
        s_tile = str(tile + 10)
        if tile in TileType.REDS :
            s_tile = str(tile + 15)
            s_rtile = str(51 + (tile // 10))
            if pos == 1 : self.actions[i_player].append(f"{s_tile}{s_tile}{s_tile}m{s_rtile}")
            elif pos == 2 : self.actions[i_player].append(f"{s_tile}m{s_rtile}{s_tile}{s_tile}")
            else : self.actions[i_player].append(f"m{s_rtile}{s_tile}{s_tile}{s_tile}")
        elif tile in TileType.FIVES and self.red[tile//10] :
            s_rtile = str(51 + (tile // 10))
            if pos == 1 : self.actions[i_player].append(f"{s_tile}{s_tile}{s_rtile}k{s_tile}")
            elif pos == 2 : self.actions[i_player].append(f"{s_tile}m{s_tile}{s_tile}{s_rtile}")
            else : self.actions[i_player].append(f"m{s_tile}{s_tile}{s_tile}{s_rtile}")
        elif pos == 1 : self.actions[i_player].append(f"{s_tile}{s_tile}{s_tile}m{s_tile}")
        elif pos == 2 : self.actions[i_player].append(f"{s_tile}m{s_tile}{s_tile}{s_tile}")
        else : self.actions[i_player].append(f"m{s_tile}{s_tile}{s_tile}{s_tile}")


    def register_pon(self, i_player:int, tile:int, pos:int) -> None :
        s_tile = str(tile + 10)
        if tile in TileType.REDS :
            s_tile = str(tile + 15)
            s_rtile = str(51 + (tile // 10))
            if pos == 1 : self.actions[i_player].append(f"{s_tile}{s_tile}p{s_rtile}")
            elif pos == 2 : self.actions[i_player].append(f"{s_tile}p{s_rtile}{s_tile}")
            else : self.actions[i_player].append(f"p{s_rtile}{s_tile}{s_tile}")
        elif tile in TileType.FIVES and self.red[tile//10] :
            s_rtile = str(51 + (tile // 10))
            if pos == 1 : self.actions[i_player].append(f"{s_tile}{s_rtile}p{s_tile}")
            elif pos == 2 : self.actions[i_player].append(f"{s_tile}p{s_tile}{s_rtile}")
            else : self.actions[i_player].append(f"p{s_tile}{s_rtile}{s_tile}")
        elif pos == 1 : self.actions[i_player].append(f"{s_tile}{s_tile}p{s_tile}")
        elif pos == 2 : self.actions[i_player].append(f"{s_tile}p{s_tile}{s_tile}")
        else : self.actions[i_player].append(f"p{s_tile}{s_tile}{s_tile}")


    def register_chii(self, i_player:int, tile:int, tile1:int, tile2:int) -> None :
        s_tile, s_tile1, s_tile2 = str(tile + 10), str(tile1 + 10), str(tile2 + 10)
        if tile in TileType.REDS : s_tile = str(51 + (tile // 10))
        elif tile1 in TileType.REDS : s_tile1 = str(51 + (tile1 // 10))
        elif tile2 in TileType.REDS : s_tile2 = str(51 + (tile2 // 10))
        self.actions[i_player].append(f"c{s_tile}{s_tile1}{s_tile2}")


    def register_got_tile(self, i_player:int, tile:int, is_starting_hand:bool = False) -> None :
        if tile in TileType.REDS : s_tile = str(51 + (tile // 10))
        else : s_tile = str(10 + tile)
        if is_starting_hand : self.starting_hands[i] .append(s_tile)
        else : self.tiles_player_got[i].append(s_tile)


    def register_discarded_tile(self, i_player:int, discarded_tile: int, ready: bool) -> None :
        log_text = ""
        if ready : log_text = "r"
        if discarded_tile in TileType.REDS : s_discarded_tile = str(51 + (discarded_tile // 10))
        else : s_discarded_tile = str(10 + discarded_tile)
        self.actions[i_player].append(log_text + s_discarded)


    def save(game: Game) -> None :
        text = "{\"title\":[\"\",\"\"],\"name\":[\"\",\"\",\"\",\"\"],\"rule\":{\"aka\":1},\"log\":[["
        temp = []
        temp.append(game.rounds_num * 4 + game.rotations_num)
        temp.append(game.counters_num)
        temp.append(game.deposits_num)
        text += str(temp) + ","
        scores = []
        for i in range(4) : scores += [scores[i]]
        text += str(scores) + ","
        dora_indicators = []
        ura_indicators = []
        for i in range(5) :
            if game.dora_indicators[i] in TileType.REDS : dora_indicators += [51 + (game.dora_indicators[i] // 10)]
            else : dora_indicators += [game.dora_indicators[i] + 10]
            if game.ura_indicators[i] in TileType.REDS : ura_indicators += [51 + (game.ura_indicators[i] // 10)]
            else : ura_indicators += [game.ura_indicators[i] + 10]
        text += str(dora_indicators) + ","
        text += str(ura_indicators) + ","

        for i in range (4) :
            text += str(self.starting_hands[i]) + ","
            temp = str(self.tiles_player_got[i])
            temp = temp.replace('\'','\"')
            text += temp + ","
            temp = str(self.actions[i])
            temp = temp.replace('\'','\"')
            text += temp + ","

        text += "[\"不明\"]]]}\n"

        f = open(self.save_path, mode="a")
        f.write(text)
        f.flush()
        f.close()

