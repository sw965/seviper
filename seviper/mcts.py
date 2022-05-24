import random
import seviper
import parrot

class Eval:
    def __init__(self, func, reverse):
        self.func = func
        self.reverse = reverse

    @staticmethod
    def new_random_playout():
        def func(battle):
            if battle.is_game_end():
                winner = battle.winner()
            else:
                winner = battle.playout(seviper.Trainer.random_instruction, seviper.Trainer.random_instruction)
            if winner == seviper.WINNER_P1:
                return 1.0
            elif winner == seviper.WINNER_P2:
                return 0.0
            else:
                return 0.5

        def reverse(eval_y):
            return 1.0 - eval_y

        return Eval(func, reverse)

class UpperConfidenceBound1:
    def __init__(self):
        self.accum_reward = 0.0
        self.trial = 0

    def average_reward(self):
        return self.accum_reward / float(self.trial)

    def get(self, total_trial, X):
        average_reward = self.average_reward()
        return parrot.upper_confidence_bound1(average_reward, total_trial, self.trial, X)

class ActionCmdUCB1s(dict):
    def total_trial(self):
        return sum([ucb.trial for ucb in self.values()])

    def max_ucb(self, X):
        total_trial = self.total_trial()
        return max([ucb.get(total_trial, X) for ucb in self.values()])

    def max_ucb_action_cmds(self, X):
        total_trial = self.total_trial()
        max_ucb = self.max_ucb(X)
        return [action_cmd for action_cmd, ucb in self.items() if ucb.get(total_trial, X) == max_ucb]

    def max_trial(self):
        return max([ucb.trial for ucb in self.values()])

    def max_trial_action_cmds(self):
        max_trial = self.max_trial()
        return [action_cmd for action_cmd, ucb in self.items() if ucb.trial == max_trial]

class Node:
    def __init__(self, battle):
        self.battle = battle
        self.p1_legal_action_cmds = battle.p1_legal_action_cmds()
        self.p2_legal_action_cmds = battle.p2_legal_action_cmds()
        self.is_p1_all_expansion = len(self.p1_legal_action_cmds) == 0
        self.is_p2_all_expansion = len(self.p2_legal_action_cmds) == 0
        self.p1_action_cmd_ucb1s = ActionCmdUCB1s()
        self.p2_action_cmd_ucb1s = ActionCmdUCB1s()
        self.next_nodes = Nodes()
        self.select_count = 0

    def p1_no_expansion_action_cmds(self):
        return [action_cmd for action_cmd in self.p1_legal_action_cmds if action_cmd not in self.p1_action_cmd_ucb1s]

    def p2_no_expansion_action_cmds(self):
        return [action_cmd for action_cmd in self.p2_legal_action_cmds if action_cmd not in self.p2_action_cmd_ucb1s]

    def select(self, battle, all_nodes, X):
        selects = Selects()
        is_roop_select = False

        while True:
            if not self.is_p1_all_expansion or not self.is_p2_all_expansion:
                break

            if len(self.p1_legal_action_cmds) != 0:
                p1_action_cmd = random.choice(self.p1_action_cmd_ucb1s.max_ucb_action_cmds(X))
            else:
                p1_action_cmd = None

            if len(self.p2_legal_action_cmds) != 0:
                p2_action_cmd = random.choice(self.p2_action_cmd_ucb1s.max_ucb_action_cmds(X))
            else:
                p2_action_cmd = None

            if p1_action_cmd is None:
                action = {"p2":p2_action_cmd}
            elif p2_action_cmd is None:
                action = {"p1":p1_action_cmd}
            else:
                action = {"p1":p1_action_cmd, "p2":p2_action_cmd}

            selects.append(Select(self, p1_action_cmd, p2_action_cmd))
            self.select_count += 1

            battle = battle.push(action)

            if battle.is_game_end():
                break

            #next_nodesの中に、同じ局面のbattleが存在するならば、それを次のnodeとする
            #next_nodesの中に、同じ局面のbattleが存在しないなら、all_nodesの中から同じ局面のbattleが存在しないかを調べる。
		    #all_nodesの中に、同じ局面のbattleが存在するならば、次回から高速に探索出来るように、next_nodesに追加して、次のnodeとする。
		    #next_nodesにもall_nodesにも同じ局面のbattleが存在しないなら、新しくnodeを作り、
		    #next_nodesと、all_nodesに追加し、新しく作ったnodeを次のnodeとする。
		    #またnodeを新しく作った場合は、一番上のbreak条件に必ず引っかかる。

            next_node = self.next_nodes.find(battle)

            if next_node is None:
                next_node = all_nodes.find(battle)
                if next_node is not None:
                    self.next_nodes.append(next_node)
                else:
                    next_node = Node(battle)
                    all_nodes.append(next_node)
                    self.next_nodes.append(next_node)

            if next_node.select_count == 1:
                is_roop_select = True
                break

            self = next_node

        return self, battle, selects, is_roop_select

    def expansion_with_eval_y(self, battle, X, eval, selects):
        assert not self.is_p1_all_expansion or not self.is_p2_all_expansion

        p1_no_expansion_action_cmds = self.p1_no_expansion_action_cmds()
        p2_no_expansion_action_cmds = self.p2_no_expansion_action_cmds()

        if len(self.p1_legal_action_cmds) == 0:
            p1_action_cmd = None
        elif len(p1_no_expansion_action_cmds) == 0:
            p1_action_cmd = random.choice(self.p1_action_cmd_ucb1s.max_ucb_action_cmds(X))
        else:
            p1_action_cmd = random.choice(p1_no_expansion_action_cmds)

        if len(self.p2_legal_action_cmds) == 0:
            p2_action_cmd = None
        elif len(p2_no_expansion_action_cmds) == 0:
            p2_action_cmd = random.choice(self.p2_action_cmd_ucb1s.max_ucb_action_cmds(X))
        else:
            p2_action_cmd = random.choice(p2_no_expansion_action_cmds)

        assert p1_action_cmd is not None or p2_action_cmd is not None

        if p1_action_cmd is None:
            action = {"p2":p2_action_cmd}
        elif p2_action_cmd is None:
            action = {"p1":p1_action_cmd}
        else:
            action = {"p1":p1_action_cmd, "p2":p2_action_cmd}

        battle = battle.push(action)

        if p1_action_cmd not in self.p1_action_cmd_ucb1s and p1_action_cmd is not None:
            self.p1_action_cmd_ucb1s[p1_action_cmd] = UpperConfidenceBound1()

        if p2_action_cmd not in self.p2_action_cmd_ucb1s and p2_action_cmd is not None:
            self.p2_action_cmd_ucb1s[p2_action_cmd] = UpperConfidenceBound1()

        selects.append(Select(self, p1_action_cmd, p2_action_cmd))

        if len(self.p1_action_cmd_ucb1s) == len(self.p1_legal_action_cmds):
            self.is_p1_all_expansion = True

        if len(self.p2_action_cmd_ucb1s) == len(self.p2_legal_action_cmds):
            self.is_p2_all_expansion = True

        eval_y = eval.func(battle)
        return eval_y

class Nodes(list):
    def find(self, battle):
        for node in self:
            if node.battle == battle:
                return node
        return None

class Select:
    def __init__(self, node, p1_action_cmd, p2_action_cmd):
        self.node = node
        self.p1_action_cmd = p1_action_cmd
        self.p2_action_cmd = p2_action_cmd

class Selects(list):
    def backward(self, eval_y, eval):
        for select in self:
            node = select.node
            p1_action_cmd = select.p1_action_cmd
            p2_action_cmd = select.p2_action_cmd

            if p1_action_cmd is not None:
                node.p1_action_cmd_ucb1s[p1_action_cmd].trial += 1
                node.p1_action_cmd_ucb1s[p1_action_cmd].accum_reward += eval_y

            if p2_action_cmd is not None:
                node.p2_action_cmd_ucb1s[p2_action_cmd].trial += 1
                node.p2_action_cmd_ucb1s[p2_action_cmd].accum_reward += eval.reverse(eval_y)

            node.select_count = 0

def run(root_battle, simu_num, X, eval):
    root_node = Node(root_battle)
    all_nodes = Nodes([root_node])

    node = root_node
    battle = root_battle

    for i in range(simu_num):
        node, battle, selects, is_roop_select = node.select(battle, all_nodes, X)

		#select処理を行い、ゲームが終了したならば、その状態で評価関数を呼び出し、評価する。
		#roop_select状態ならば、必ず全てを展開しているnodeになっている(=展開出来ない)ので、そのまま評価を得る。
		#ゲームが終了せず、roop_select状態でなければ、必ず展開していないnodeがある状態なので、展開処理をして、評価を得る。

        if battle.is_game_end() or is_roop_select:
            eval_y = eval.func(battle)
        else:
            eval_y = node.expansion_with_eval_y(battle, X, eval, selects)

        selects.backward(eval_y, eval)
        node = root_node
        battle = root_battle

    return all_nodes

def new_trainer(simu_num, X, eval):
    def result(battle):
        all_nodes = run(battle, simu_num, X, eval)
        return random.choice(all_nodes[0].p1_action_cmd_ucb1s.max_trial_action_cmds())
    return result
