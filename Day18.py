class PairNode:
    def __init__(self, parent):
        self.LNode = None
        self.RNode = None
        self.Parent = parent
        self.Val = 0
        self.IsLeaf = True
        self.Level = 0 if parent is None else parent.Level+1

    def incr_level(self):
        self.Level += 1
        if self.IsLeaf is False:
            self.LNode.incr_level()
            self.RNode.incr_level()
            
    def append_val(self, Val):
        if self.Val == -1:
            self.Val = Val
        else:
            self.Val = self.Val*10 + Val

    def parse_input(self, input_str, indent):
        indent_str = ' '*indent
        #print(f"Parsing input_str={input_str}, indent={indent}")
        idx = 0
        while idx < len(input_str):
            c= input_str[idx]
            #print(f"{indent_str}Parsing char {c}")
            if c == '[':
                # Start of left node of next level
                #print(f"{indent_str}Found start of pair, start parsing LNode...")
                self.LNode = PairNode(self)
                self.RNode = PairNode(self)
                self.IsLeaf = False
                parsed_cnt = self.LNode.parse_input(input_str[idx+1:], indent+2)
                #print(f"{indent_str}Finished parsing LNode, consumed {parsed_cnt} chars, start parsing RNode...")
                idx += parsed_cnt + 1
                #print(f"{indent_str}Before parsing RNode, idx={idx}...")
                parsed_cnt = self.RNode.parse_input(input_str[idx+1:], indent+2)
                #print(f"{indent_str}Finished parsing RNode, consumed {parsed_cnt}...")
                idx += parsed_cnt + 1
            elif c == ']':
                # finish of a node
                #print(f"{indent_str}Found finish of pair")
                return idx
            elif c == ',':
                # Done with one side, move to next
                #print(f"{indent_str}Found middle of pair, finish parsing current node, my_idx={idx}...")
                return idx
            else:
                # numbers, set it
                #print(f"{indent_str}Found value {int(c)}, setting it")
                self.append_val(int(c))
            idx += 1

    def print_node(self, level):
        indent_str = ' '*level*2
        if self.LNode != None:
            print(f"{indent_str}{level}-LEFT:")
            self.LNode.print_node(level + 1)
            print(f"{indent_str}{level}-RIGHT:")
            self.RNode.print_node(level + 1)
        else:
            print(f"{indent_str}{self.Val}")

    def get_snail_str(self):
        ret_str = ''
        if self.IsLeaf == False:
            ret_str += '['
            ret_str += self.LNode.get_snail_str()
            ret_str += ','
            ret_str += self.RNode.get_snail_str()
            ret_str += ']'
        else:
            ret_str = str(self.Val)
        return ret_str

    def get_root(self):
        return self if self.Parent is None else self.Parent.get_root()

    def get_up_right(self):
        if self.Parent == None:
            return None
        elif self.Parent.RNode == self:
            return self.Parent.get_up_right()
        elif self.Parent.LNode == self:
            return self.Parent.RNode

    def get_up_left(self):
        if self.Parent == None:
            return None
        elif self.Parent.LNode == self:
            return self.Parent.get_up_left()
        elif self.Parent.RNode == self:
            return self.Parent.LNode

    def get_leftmost_leaf(self):
        if self.IsLeaf == True:
            return self
        else:
            return self.LNode.get_leftmost_leaf()

    def get_rightmost_leaf(self):
        if self.IsLeaf == True:
            return self
        else:
            return self.RNode.get_rightmost_leaf()

    def split(self):
        # print(f"Trying to split {self.get_snail_str()}")
        if self.IsLeaf == False:
            ret_val = self.LNode.split()
            if ret_val == True:
                return True
            ret_val = self.RNode.split()
            if ret_val == True:
                return True
            return False
        else:
            if self.Val >= 10:
                # print(f"splitting node value {self.Val}")
                split_node = PairNode(self.Parent)
                split_node.IsLeaf = False
                split_node.Level = self.Level
                split_node.LNode = PairNode(split_node)
                split_node.LNode.Val = int(self.Val/2)
                split_node.LNode.IsLeaf = True
                split_node.RNode = PairNode(split_node)
                split_node.RNode.Val = int((self.Val + 1) / 2)
                split_node.RNode.IsLeaf = True
                if self.Parent.LNode == self:
                    self.Parent.LNode = split_node
                elif self.Parent.RNode == self:
                    self.Parent.RNode = split_node
                return True
            else:
                # print("self val < 10, return False")
                return False

    def explode(self):
        # print(f"Trying to Explode pair: {self.get_snail_str()}")
        ret_val = False
        if self.LNode.IsLeaf == False:
            ret_val |= self.LNode.explode()
            if ret_val:
                return True
        if self.RNode.IsLeaf == False:
            ret_val |= self.RNode.explode()
            if ret_val:
                return True
        if self.Level >= 4:
            # explode
            if self.Parent.LNode == self:
                # print(f"Pair is on left-half")
                UpperLNode: PairNode = self.get_up_left()
                if UpperLNode == None:
                    # print("Found no upper-left node to add to - must be left-most")
                    NewNode = PairNode(self.Parent.Parent)
                    NewNode.append_val(0)
                    self.Parent.LNode = NewNode
                else:
                    # print("Found upper-left node to add to:")
                    # print(UpperLNode.get_snail_str())
                    UL_rightmost_leaf = UpperLNode.get_rightmost_leaf()
                    UL_rightmost_leaf.Val += self.LNode.Val
                # update upper-R node
                self.Parent.RNode.get_leftmost_leaf().Val += self.RNode.Val
                # clear upper-L node
                self.Parent.LNode = PairNode(self.Parent)
                self.Parent.LNode.Val = 0
            elif self.Parent.RNode == self:
                # print(f"Pair is on right-half")
                UpperRNode : PairNode = self.get_up_right()
                if UpperRNode == None:
                    # print("Found no upper-right node to add to - must be right-most")
                    NewNode = PairNode(self.Parent.Parent)
                    NewNode.append_val(0)
                    self.Parent.RNode = NewNode
                else:
                    # print("Found upper-right node to add to:")
                    # print(UpperRNode.get_snail_str())
                    UR_leftmost_leaf = UpperRNode.get_leftmost_leaf()
                    UR_leftmost_leaf.Val += self.RNode.Val
                # update upper-L node
                self.Parent.LNode.get_rightmost_leaf().Val += self.LNode.Val
                # clear upper-R node
                self.Parent.RNode = PairNode(self.Parent)
                self.Parent.RNode.Val = 0
            # print(f"After explosion, root node looks like: {self.get_root().get_snail_str()}")
            return True
        return ret_val

    def reduce(self):
        # print(f"Start reducing {self.get_snail_str()}")
        Done = False
        while True:
            while self.explode() == True:
                # print(f"Something exploded, After explosion: {self.get_snail_str()}")
                None

            # print("No more explosion, moving to split")
            if self.split() == False:
                # print(f"Nothing to split, WE ARE DONE")
                break
            else:
                # print(f"Something split, after split: {self.get_snail_str()}")
                None

    def get_magnitude(self):
        l_mag = 0
        r_mag = 0
        if self.IsLeaf == True:
            return self.Val
        else:
            l_mag = self.LNode.get_magnitude()
            r_mag = self.RNode.get_magnitude()
            return 3*l_mag + 2*r_mag

def add_nodes(left, right):
    NewNode = PairNode(None)
    NewNode.IsLeaf = False
    NewNode.LNode = left
    NewNode.RNode = right

    NewNode.LNode.Parent = NewNode
    NewNode.RNode.Parent = NewNode
    NewNode.LNode.incr_level()
    NewNode.RNode.incr_level()

    return NewNode

day18_explode_inputs = [
    '[[[[[9,8],1],2],3],4]',
    '[7,[6,[5,[4,[3,2]]]]]',
    '[[6,[5,[4,[3,2]]]],1]',
    '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
    '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'
]

# for inp in day18_explode_inputs:
#     root_node = PairNode(None)
#     print(f"Testing snail {inp}")
#     root_node.parse_input(inp, 0)
#
#     root_node.reduce()
#     print("After reduce:", root_node.get_snail_str(),"\n\n\n")

# day18_chain = [
#     '[1,1]',
#     '[2,2]',
#     '[3,3]',
#     '[4,4]',
#     '[5,5]',
#     '[6,6]'
#     ]

# day18_chain = [
#      '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
#      '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
#      '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
#      '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
#      '[7,[5,[[3,8],[1,4]]]]',
#      '[[2,[2,2]],[8,[8,1]]]',
#      '[2,9]',
#      '[1,[[[9,3],9],[[9,0],[0,7]]]]',
#      '[[[5,[7,4]],7],1]',
#      '[[[[4,2],2],6],[8,7]]]'
#     ]
day18_chain = [
    '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
    '[[[5,[2,8]],4],[5,[[9,9],0]]]',
    '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
    '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
    '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
    '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
    '[[[[5,4],[7,7]],8],[[8,3],8]]',
    '[[9,3],[[9,9],[6,[4,9]]]]',
    '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
    '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
]

day18_input = [
'[5,[7,[8,4]]]',
'[[[4,1],[6,[9,3]]],[[7,4],[5,[7,0]]]]',
'[[6,2],[[[8,6],[5,5]],0]]',
'[[[5,9],[3,[4,2]]],[[[1,2],0],2]]',
'[[[[4,3],2],0],[[[1,7],[1,2]],[[8,2],[6,7]]]]',
'[[[[0,1],9],3],[[4,7],[7,8]]]',
'[[[[8,7],4],[5,[9,2]]],[[8,[9,6]],[1,8]]]',
'[[[2,3],[[9,9],[7,0]]],[6,7]]',
'[8,[[9,9],[8,6]]]',
'[[[[5,7],[7,1]],[3,[7,6]]],[2,[[5,5],[8,3]]]]',
'[[[7,0],2],[[[2,2],7],[6,[2,9]]]]',
'[[6,2],[[0,8],8]]',
'[[[[2,9],4],9],[1,[[6,9],[7,5]]]]',
'[[[9,3],[[5,7],[3,1]]],[5,[6,[7,8]]]]',
'[0,[[8,9],1]]',
'[[4,[[4,3],4]],[7,[[4,0],0]]]',
'[[0,[[1,9],[6,1]]],[[[7,0],[5,2]],[[3,8],[0,4]]]]',
'[[[2,7],[7,[1,6]]],[6,[[8,7],[8,5]]]]',
'[[9,5],[[1,[2,5]],[8,[2,0]]]]',
'[6,[[8,[9,4]],[9,8]]]',
'[[[[2,0],[4,6]],3],[[8,0],4]]',
'[[[8,8],[[5,7],[5,6]]],5]',
'[[5,[[7,9],9]],[1,6]]',
'[[[[5,2],[4,9]],[[1,9],[2,9]]],[[[6,8],[7,5]],[[0,2],4]]]',
'[1,[5,[[5,5],[1,2]]]]',
'[[[1,4],[[0,3],7]],[[[9,1],9],[[2,3],7]]]',
'[[[[6,4],[4,0]],[[3,4],[7,0]]],[[8,7],[5,[0,6]]]]',
'[[3,[8,[2,8]]],[9,[0,[5,2]]]]',
'[[7,[[1,8],1]],[6,[6,6]]]',
'[[[3,[9,4]],[[3,2],[5,2]]],8]',
'[3,[[4,[4,3]],[5,[9,2]]]]',
'[[[1,8],[2,[7,5]]],[[0,[8,1]],[2,0]]]',
'[1,3]',
'[7,[[[9,6],[8,4]],9]]',
'[6,4]',
'[[[8,9],[[3,7],2]],[4,[[5,0],8]]]',
'[[[[1,8],[7,9]],0],[[[4,4],3],[4,[1,7]]]]',
'[[[[2,2],[0,9]],[1,2]],[[[9,1],[0,0]],[[1,6],4]]]',
'[[[[8,1],6],[[3,3],[6,7]]],[[2,3],5]]',
'[[[[9,0],7],6],[[[3,6],[6,7]],3]]',
'[[[[1,0],6],[5,[0,0]]],[[[9,7],7],5]]',
'[[[[5,1],4],[[7,7],[6,2]]],[[0,[6,0]],2]]',
'[[[[8,3],[0,4]],[[9,9],[3,7]]],[[[2,7],[2,9]],[[2,0],[4,7]]]]',
'[6,[[[4,8],0],8]]',
'[[[6,[5,9]],[[0,3],9]],[[[2,5],[9,5]],0]]',
'[[1,4],[6,[0,[6,2]]]]',
'[9,[[[3,7],1],7]]',
'[[[2,3],[[1,2],1]],[[[2,6],[0,1]],[0,[4,1]]]]',
'[[[0,1],[[0,3],[7,3]]],[[8,7],3]]',
'[[0,[[1,5],[5,3]]],4]',
'[[[5,3],[[5,8],6]],[[[6,0],3],[4,1]]]',
'[8,3]',
'[[[[5,5],[3,0]],6],[[7,5],[2,[9,4]]]]',
'[[[3,[3,3]],[[4,7],4]],[[2,0],1]]',
'[[[0,[2,8]],[4,[7,9]]],[[[5,4],2],2]]',
'[[3,[7,[1,8]]],[5,[[8,2],0]]]',
'[[1,9],[[6,[5,9]],8]]',
'[[5,[5,2]],5]',
'[[[1,1],[4,3]],1]',
'[[[[6,9],[4,1]],0],[[[3,0],6],7]]',
'[[9,[[7,3],6]],[[[7,2],0],[9,9]]]',
'[[5,4],[[[6,0],[5,1]],7]]',
'[[[4,0],0],[[[2,6],[4,4]],[[6,8],2]]]',
'[[[9,6],8],[[0,[9,5]],9]]',
'[[6,[2,5]],[[[1,8],[9,0]],[[4,0],[5,7]]]]',
'[5,[[8,[9,9]],[5,[6,8]]]]',
'[[[7,[9,0]],5],6]',
'[[9,[[3,7],[3,0]]],[[[7,2],[5,7]],[[0,5],[7,4]]]]',
'[[7,3],[[6,5],[9,4]]]',
'[[4,[4,3]],[9,[[2,6],0]]]',
'[[[6,[0,1]],9],[[7,[3,2]],[[0,1],[5,2]]]]',
'[[5,[0,[3,1]]],[[[1,1],[8,9]],[[6,3],[0,9]]]]',
'[[[[2,8],0],[[8,7],4]],[[[9,6],3],[[7,8],[2,3]]]]',
'[[[[1,0],1],4],[4,9]]',
'[[[7,8],5],[[[3,7],[5,7]],6]]',
'[[[8,[7,4]],[[1,6],[6,7]]],[2,4]]',
'[[7,8],3]',
'[[0,[4,[3,8]]],[[[1,0],1],6]]',
'[[[[6,3],7],2],[[4,5],6]]',
'[[[5,9],[[1,8],1]],[[[1,8],8],[[6,4],0]]]',
'[[3,[8,[2,8]]],[[[2,8],[4,4]],9]]',
'[7,[5,[[3,3],3]]]',
'[3,[1,[0,[3,0]]]]',
'[[[1,2],4],[9,[[7,1],[5,4]]]]',
'[[[5,8],[7,[0,7]]],[0,[[2,9],8]]]',
'[[[7,[2,0]],[1,[4,3]]],[0,[[1,1],[2,0]]]]',
'[[[2,[2,5]],[4,1]],[0,[6,0]]]',
'[[[8,3],9],[[[4,3],[5,8]],[[7,0],9]]]',
'[2,[1,4]]',
'[[[3,[2,6]],6],[[[3,2],[0,8]],[[3,5],[6,4]]]]',
'[[[1,[3,3]],[[0,8],[1,3]]],[8,[[3,8],[0,8]]]]',
'[[[[1,5],[0,1]],3],[[6,[1,7]],[4,7]]]',
'[[4,[5,7]],[6,[[6,2],7]]]',
'[[[[7,4],[3,1]],[5,6]],[0,[6,5]]]',
'[[[7,[0,0]],6],[5,[[0,0],[3,5]]]]',
'[[[[8,7],[5,8]],[8,[9,3]]],[[7,0],[[7,2],0]]]',
'[[[7,[4,2]],0],[[[4,0],1],3]]',
'[[[6,3],[9,[2,2]]],[[0,8],[1,2]]]',
'[3,[[3,1],[[7,1],1]]]',
'[[3,[[4,0],7]],[[[4,6],[2,3]],[[0,2],[1,8]]]]',
]

root_state = PairNode(None)
for idx, inp in enumerate(day18_chain):
    # print(f"Adding snail {inp} at idx {idx}")
    if idx==0:
        root_state.parse_input(inp, 0)
    else:
        sum_node = None
        right_node = PairNode(None)
        right_node.parse_input(inp, 0)
        sum_node = add_nodes(root_state, right_node)
        # print(f"After addition: sum_node={sum_node.get_snail_str()}")
        sum_node.reduce()
        # print("After reduce:", sum_node.get_snail_str())
        root_state = sum_node

print(f"Final snail = {root_state.get_snail_str()}, mag = {root_state.get_magnitude()}")

max_mag_any2 = 0
max_mag_entries = None
for idx1, inp1 in enumerate(day18_input):
    for idx2, inp2 in enumerate(day18_input):
        if idx1 == idx2:
            continue
        print(f"Trying candidate # {idx1} and {idx1+idx2}")
        cand1 = PairNode(None)
        cand1.parse_input(inp1, 0)
        cand2 = PairNode(None)
        cand2.parse_input(inp2, 0)
        print(f"Cand1: {cand1.get_snail_str()}")
        print(f"Cand2: {cand2.get_snail_str()}")

        cand12 = add_nodes(cand1, cand2)
        print(f"Cand12: {cand12.get_snail_str()}")
        cand12.reduce()
        print(f"After reduce: Cand12 = {cand12.get_snail_str()}, mag={cand12.get_magnitude()}")

        if cand12.get_magnitude() > max_mag_any2:
            max_mag_any2 = cand12.get_magnitude()
            max_mag_entries = (idx1, idx2)
print(f"Max mag = {max_mag_any2}, entries = {max_mag_entries}")