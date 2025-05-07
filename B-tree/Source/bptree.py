import sys
import csv
import math
import argparse
##
# Node construction
class Node:
    def __init__(self, order):
        self.order = order   # order of B+ tree
        self.keys = []       # key array
        self.pointers = []   # internal node에서는 children pointer, leaf node에서는 value pointer
        self.nextKey = None  # leaf node에서 오른쪽 노드를 가리킴
        self.parent = None   # parent node
        self.isLeaf = False  # leaf 인지 아닌지

    def insert_at_leaf(self, key, pointer):
        if self.keys:
            for i in range(len(self.keys)):
                if key < self.keys[i]:
                    self.keys = self.keys[:i] + [key] + self.keys[i:]
                    self.pointers = self.pointers[:i] + [pointer] + self.pointers[i:]
                    return
            self.keys.append(key)
            self.pointers.append(pointer)
        else:
            self.keys = [key]
            self.pointers = [pointer]
       
class bptree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.isLeaf = True
        self.order = order

    def search(self, key):
        current_node = self.root
       
        flagged_node = None # internal node flag

        while not current_node.isLeaf:  # insert or delete 할 '리프노드' 찾기
            
            for i in range(len(current_node.keys)):
                if key < current_node.keys[i]:
                    if key in current_node.keys:
                        flagged_node = current_node # 삭제할 때 삭제할 key를 갖고있는 internal node를 저장
                    current_node = current_node.pointers[i]
                    break
            else: # 현재 노드의 모든 키 보다 큰 경우
                if key in current_node.keys:
                    flagged_node = current_node
                current_node = current_node.pointers[-1]

        return current_node, flagged_node # return leaf node, internal node

    def insert(self, key, pointer):
      
        old_node , _ = self.search(key)
        old_node.insert_at_leaf(key, pointer)  

        # overflow가 발생한 경우
        if len(old_node.keys) > old_node.order - 1:
            self.split_node(old_node)

    def split_node(self, old_node):
        new_node = Node(old_node.order)
        new_node.isLeaf = old_node.isLeaf

        mid = len(old_node.keys) // 2
        if old_node.isLeaf:
            # leaf node일 떄
            # 부모로 올릴 키 값을 오른쪽 자식의 첫번째 키에 저장해야함.
            # split 한 후, nextKey 조정
            new_node.keys = old_node.keys[mid:]
            new_node.pointers = old_node.pointers[mid:]
            old_node.keys = old_node.keys[:mid]
            old_node.pointers = old_node.pointers[:mid]

            new_node.nextKey = old_node.nextKey
            old_node.nextKey = new_node

            parent_key = new_node.keys[0]
        else:
            # internal node일 때
            # 부모로 올릴 키 값을 오른쪽 자식에 저장할 필요 없음.
            new_node.keys = old_node.keys[mid + 1:]
            new_node.pointers = old_node.pointers[mid + 1:]
            parent_key = old_node.keys[mid]
            old_node.keys = old_node.keys[:mid]
            old_node.pointers = old_node.pointers[:mid + 1]

            for pointer in new_node.pointers:
                if pointer is not None:
                    pointer.parent = new_node

        # 부모로 insert
        self.insert_into_parent(old_node, new_node, parent_key)

    def insert_into_parent(self, old_node, new_node, key):
        parent = old_node.parent
        if parent is None:
            new_root = Node(old_node.order)
            new_root.keys = [key]
            new_root.pointers = [old_node, new_node]
            old_node.parent = new_root
            new_node.parent = new_root
            self.root = new_root
            return

        for i in range(len(parent.keys)):
            if key < parent.keys[i]:
                parent.keys = parent.keys[:i] + [key] + parent.keys[i:]
                parent.pointers = parent.pointers[:i + 1] + [new_node] + parent.pointers[i + 1:]
                new_node.parent = parent
                break
        else:
            parent.keys.append(key)
            parent.pointers.append(new_node)
            new_node.parent = parent

        # 부모로 insert한 후에도 overflow가 나는지 확인
        if len(parent.keys) > parent.order - 1:
            self.split_node(parent)

    def delete(self, key):
        # leaf node에서 먼저 삭제
        leaf_node, flagged_node= self.search(key)
        

        if key not in leaf_node.keys:
            print(f"Key {key} not found for deletion.")
            return False

        index = leaf_node.keys.index(key)
        leaf_node.keys.pop(index)
        leaf_node.pointers.pop(index)

        #underflow 발생 시 처리
        if len(leaf_node.keys) < math.ceil(self.root.order / 2) - 1:
            #print(f"Underflow after delete {key}")
            self.handle_underflow(leaf_node, key)
        
        #internal node에 key가 있는지 확인하고 삭제
        if flagged_node is not None:

            self.delete_from_internal_nodes(flagged_node,key)
        return True
    
    def delete_from_internal_nodes(self, node, key):
        
        if key in node.keys:
            #print(f"Deleting key {key} from internal node: {node.keys}")
            # 후임자랑 위치를 바꾸고
            # 삭제
            index = node.keys.index(key)

            successor= self.find_min(node.pointers[index+1])

            node.keys[index] = successor

            # underflow 발생 시 처리
            if len(node.keys) < math.ceil(self.root.order/2)-1:
                self.handle_underflow(node,key)

    def find_min(self, node):

        # to find succesor
        # 인자를 받을 때 후임자가 필요한 노드의 오른쪽 자식을 넣어줘야 함.
        current_node= node
        while not current_node.isLeaf:
            if not current_node.pointers:
                raise IndexError("Node pointeres are empty in find_min")
            current_node= current_node.pointers[0] # 계속 왼쪽 노드로
        
        if not current_node.keys:
            raise IndexError("Leaf node keys are empty in find_min")
        return current_node.keys[0] # 현재 키 값들보다 큰 수 중에서 가장 작은 수

    def handle_underflow(self, node, key=None):
        parent = node.parent
        if not parent:
            if len(node.keys) == 0:
                if node.isLeaf:
                    self.root = None
                else:
                    # 왼쪽, 오른족 자식이 모두 살아있는 경우
                    if len(node.pointers) == 2:
                        smallest_key = self.find_min(node.pointers[1])
                        #print(f"smallest key: {smallest_key}")
                        self.root = node.pointers[0]
                        self.root.parent = None
                        self.insert_into_parent(self.root, node.pointers[1], smallest_key)
                        #node.keys.append(smallest_key)
                    elif node.pointers[0]:
                        self.root = node.pointers[0]
                        self.root.parent = None
                    elif node.pointers[1]:
                        self.root = node.pointers[1]
                        self.root.parent = None
                    else:
                        raise IndexError("Invalid node structure, no child pointers")
                    
            return

        try:
            index = parent.pointers.index(node)
        except ValueError:
    
            return  # 포인터 리스트에서 찾지 못한 경우 중단

        # 왼쪽 형제에서 빌려오기 시도
        if index > 0:
            left_sibling = parent.pointers[index - 1]
            if len(left_sibling.keys) > math.ceil(self.root.order / 2) - 1:
                
                if node.isLeaf:
                    
                    #node.keys.insert(0, parent.keys[index-1])
                    node.keys.insert(0, left_sibling.keys[-1])
                    node.pointers.insert(0, left_sibling.pointers[-1])

                    parent.keys[index-1] = node.keys[0]
                    left_sibling.keys.pop(-1)
                    left_sibling.pointers.pop(-1)
                else:
                    node.keys.insert(0, parent.keys[index-1])
                    node.pointers.insert(0, left_sibling.pointers[-1])

                    left_sibling.pointers.pop(-1)
                    parent.keys[index-1] = left_sibling.keys.pop(-1)
                
                if len(parent.keys) < math.ceil(self.root.order / 2) - 1:
            
                    self.handle_underflow(parent)
                return
            
           

        # 오른쪽 형제에서 빌려오기 시도
        if index < len(parent.pointers) - 1:
            right_sibling = parent.pointers[index + 1]
            if len(right_sibling.keys) > math.ceil(self.root.order / 2) - 1:
                
                if node.isLeaf:
                    node.keys.append(parent.keys[index])
                    node.pointers.append(right_sibling.pointers[0])
                    right_sibling.pointers.pop(0)
                    right_sibling.keys.pop(0)

                    parent.keys[index] = right_sibling.keys[0]
                else:
                    node.keys.append(parent.keys[index])
                    node.pointers.append(right_sibling.pointers[0])
                    right_sibling.pointers.pop(0)
                    parent.keys[index] = right_sibling.keys.pop(0)

                if len(parent.keys) < math.ceil(self.root.order / 2) - 1:
            
                    self.handle_underflow(parent)
                return
                
        self.merge(node,index,key)
        # 부모 노드에서도 underflow 발생 시 처리
        if len(parent.keys) < math.ceil(self.root.order / 2) - 1:
            
            self.handle_underflow(parent)

   
    def merge(self, node, index, key=None):
        parent = node.parent
        if index > 0:
            # left_sibling 애 node를 합치는 경우
            left_sibling = parent.pointers[index - 1]

            if parent.keys[index-1] not in left_sibling.keys: 
                # parent의 키가 left_sibling에 없을 때만
                if key is not None and parent.keys[index-1] == key:
                    # parent의 키가 삭제할 key와 같으면 부모로부터 빌려오지 않음
                    #print('skip') # 맡애서 삭제해줌
                    pass
                    
                else:

                    left_sibling.keys.append(parent.keys[index-1]) # 부모로부터 key 빌려옴
            
            # 형제와 합치는 부분
            for key in node.keys:
                if key not in left_sibling.keys:
                    left_sibling.keys.append(key)

            left_sibling.pointers.extend(node.pointers)

            del parent.keys[index - 1]
            del parent.pointers[index]

            if not node.isLeaf:
                for child in node.pointers:
                    if isinstance(child, Node):
                        child.parent = left_sibling
            else:
                left_sibling.nextKey = node.nextKey
        else:
            right_sibling = parent.pointers[index + 1]

            if parent.keys[index] not in node.keys:
                if parent.keys[index] == key:
                    #print('skip') # 밑에서 삭제해줌
                    pass
                else:

                    node.keys.append(parent.keys[index])

            for key in right_sibling.keys:
                if key not in node.keys:
                    node.keys.append(key)

            node.pointers.extend(right_sibling.pointers)

            del parent.keys[index]
            del parent.pointers[index + 1]

            if not node.isLeaf:
                for child in node.pointers:
                    if isinstance(child, Node):
                        # 부모 설정
                        child.parent = node
            else:
                # nextKey 설정
                node.nextKey = right_sibling.nextKey

    def print_tree(self, node, level=0):
        indent = "   " * level
        print(f"{indent}Level {level} Keys: {node.keys}")
   
        if node.isLeaf:
            # Leaf node 출력 형태
            print(f'{indent}Pointers: {node.pointers}')
        else:
            # Internal node 출력 형태 (루트도 여기 포함..)
            for i, child in enumerate(node.pointers):
                print(f"{indent}Children {i}: {id(child)}")
                if child:
                    self.print_tree(child, level+1)

    def range_search(self, start, end):
        current_node, _ = self.search(start)
        
        while current_node is not None:
            
            for i in range(len(current_node.keys)):
                
                if start <= current_node.keys[i] <= end:
                    # key, value 쌍으로 출력
                    print(f"{current_node.keys[i]},{current_node.pointers[i]}")
                elif current_node.keys[i] > end:
                    return
            
            current_node = current_node.nextKey
            
            #print(current_node is None)
            
    def single_key_search(self, key):
        current_node = self.root
        
        while not current_node.isLeaf:
            print(",".join(map(str, current_node.keys))) # 경로 출력
            found =False
            for i in range(len(current_node.keys)):
                if key < current_node.keys[i]:
                    current_node = current_node.pointers[i] # to the left child
                    found =True
                    break
            if not found:
                current_node = current_node.pointers[-1]
        
        print(",".join(map(str, current_node.keys)))
        for i in range(len(current_node.keys)):
            if key == current_node.keys[i]:
                print(current_node.pointers[i]) 
                
                return True
        
        print("NOT FOUND")
        return False

def create_index_file(index_file, node_size):
    try:
        with open(index_file, 'w') as f:
            f.write(f"B+ Tree Index File - Node Size: {node_size}\n")

            bpt = bptree(node_size) # 루트만 만들어서
            save_tree_node(f, bpt.root) # 파일에 저장
        print(f"Created index_file {index_file} with node size {node_size}.")
    except Exception as e:
        print(f"Failed to create the file: {e}")

def insert_from_csv(bpt, input_file, data_file):
    #csv파일로부터 읽어서 bptree 저장
    with open(data_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) ==2:
                key, value = int(row[0]), int(row[1])
                bpt.insert(key,value)
    save_tree_to_index_file(bpt, input_file) # 

def save_tree_to_index_file(bpt, index_file):
    with open(index_file, 'w') as file:
        file.write(f"B+ Tree Index File - Node Size: {bpt.order}\n")

        save_tree_node(file, bpt.root) 

def save_tree_node(file, node, level=0):
    indent = "   " * level
    if node.isLeaf:
        file.write(f"{indent}Leaf Node Key-Value Pairs: {[(k,p) for k,p in zip(node.keys, node.pointers)]}\n")
       
        
    else:
        file.write(f"{indent}Internal Node Keys: {node.keys}\n")
        for child in node.pointers:
            if child:
                save_tree_node(file, child, level+1)


def load_tree_from_index_file(index_file):
    
    with open(index_file, 'r') as file:
        lines = file.readlines()
    
        
        if "Node Size" in lines[0]:
            order = int(lines[0].split(":")[1].strip())
        else:
            raise ValueError("Index file is missing node size information.")
        
        bpt = bptree(order)

        root = parse_tree_nodes(lines[1:], order)
        #print(root is None)
        #print(root.key)
        bpt.root =root
    
        return bpt


def parse_tree_nodes(lines, order):
    # 텍스트 형태의 트리를 실제 트리로 변환해주는 함수
   
    root = None
    parent_stack = []
    current_level = -1
    prev_leaf = None
    
    for line in lines:
        indent_level = line.count("   ")  # 들여쓰기를 통해 레벨 파악
        line_content = line.strip()
        node =None

        if "Leaf Node Key-Value Pairs:" in line_content:
            pairs = eval(line_content.split("Leaf Node Key-Value Pairs:")[1].strip())  # key-value 쌍을 리스트로 변환
            node = Node(order)
            node.keys = [k for k, _ in pairs]
            node.pointers= [p for _, p in pairs]
            node.isLeaf = True

            if prev_leaf is not None:
                prev_leaf.nextKey = node
            prev_leaf = node


        elif "Internal Node Keys:" in line_content:
            keys = eval(line_content.split("Internal Node Keys:")[1].strip())  # 키 값을 리스트로 변환
            node = Node(order)
            node.keys = keys
            node.isLeaf = False
            #node.pointers = [None] * (len(keys) +1)

        else:
            print(f"Unknown line format, skipping: {line_content}")
            continue

        if node is not None:

            # 부모 자식 관계 설정
            if indent_level == current_level + 1:
                # 새로운 자식 노드
                if parent_stack:
                    node.parent = parent_stack[-1] # 부모 설정 후
                    parent_stack[-1].pointers.append(node) # 부모에 node 추가

            elif indent_level == current_level:
                # 형제 노드
                
                if parent_stack:
                    parent_stack.pop()

                    parent_stack[-1].pointers.append(node)
                    node.parent= parent_stack[-1]

            elif indent_level < current_level: 
                # 부모로 돌아가서 새로운 노드 추가
                while len(parent_stack) > indent_level: 
                    parent_stack.pop()
                if parent_stack:

                    parent_stack[-1].pointers.append(node)
                    node.parent= parent_stack[-1]
            
            parent_stack.append(node)
            current_level = indent_level
            
            if root is None: # 제일 처음에만 이 조건문 실행.
                root = node

    return root


def delete_from_index_file(bpt,input_file, data_file):
    with open(data_file, 'r') as file:
        
        for line in file:
            key = int(line.strip())
            bpt.delete(key)
            
    save_tree_to_index_file(bpt, input_file) # delete 한 후 파일에 저장



def main():
    parser = argparse.ArgumentParser(description= "B+ Tree Command Line Interface")
    
    parser.add_argument('-c',nargs = 2, metavar=('index_file', 'node_size'), help = "Create a new index file.")
    parser.add_argument('-i',nargs = 2, metavar=('index_file', 'data_file'), help = "Insert data from a csv file into index file.")
    parser.add_argument('-d',nargs = 2, metavar=('index_file', 'data_file'), help = "Delete data from index file.")
    parser.add_argument('-s',nargs = 2, metavar=('index_file', 'key'), help= "Single key search.")
    parser.add_argument('-r',nargs = 3, metavar=('index_file','start_key', 'end_key'), help="Range search.")
    args = parser.parse_args()

    if args.c:
        index_file = args.c[0]
        node_size = int(args.c[1])
        create_index_file(index_file, node_size)

    if args.i:
        index_file, data_file = args.i
       
        try:
            bpt = load_tree_from_index_file(index_file)
        
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        insert_from_csv(bpt, index_file, data_file)
        
    
    if args.d:
        index_file = args.d[0]
        data_file = args.d[1]
        try:
            bpt = load_tree_from_index_file(index_file)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        print(f"Deleting data from {index_file}")
        delete_from_index_file(bpt, index_file, data_file)
    if args.s:
        index_file, key = args.s
        try:
            bpt = load_tree_from_index_file(index_file)

        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        print(f"Searching for {key} in {index_file}")
        bpt.single_key_search(int(key))

    if args.r:
        index_file, start_key, end_key = args.r
        
        try:
            bpt = load_tree_from_index_file(index_file)
        except ValueError as e:
            sys.exit(1)
        print(f"Performing range search from {start_key} to {end_key}")
        bpt.range_search(int(start_key),int(end_key))



if __name__ == "__main__":
    main()

    

