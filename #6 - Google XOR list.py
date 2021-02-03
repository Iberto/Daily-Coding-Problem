from types import SimpleNamespace

_MEMORY = dict() # simulate a mem in order to access "like" pointers
_ADDRESS = 0

class XorLinkedList:
    '''
    Instead of each node holding 'next' and 'prev' fields, XorLinkedList holds 
    a filed named 'both', which is a XOR of the next node node and the previous node'''

    class Node:
        def __init__(self, value):
            self._value = value

    def __init__(self):
        self._head = None
        self._tail = None
        
    def add(self, element):
        global _ADDRESS

        _node = self.Node(element)

        if self._head is None:
            _both = 0 ^ (_ADDRESS + 1)
            _node_info = SimpleNamespace(Node=_node, Address=_ADDRESS, Both=_both)
            self._head = self._tail = _node_info
            _MEMORY[_ADDRESS] = _node_info
        else:
            _both = (_ADDRESS - 1) ^ (_ADDRESS + 1)
            _node_info = SimpleNamespace(Node=_node, Address=_ADDRESS, Both=_both)
            self._tail = _node_info
            _MEMORY[_ADDRESS] = _node_info

        _ADDRESS += 1

    def get(self, index:int):
        _previous_address = 0

        _current_node = self._head
        _current_both =_current_node.Both

        for _ in range(index):
            _next_address = _previous_address ^ _current_both
            _next_node = _MEMORY[_next_address]

            # update prev addr
            _previous_address = _current_node.Address

            # update curr node
            _current_node = _next_node
            _current_both = _current_node.Both

        return _current_node.Node._value


def main():

    xor_linked_list = XorLinkedList()
   
    xor_linked_list.add("element_1")
    xor_linked_list.add("element_2")
    xor_linked_list.add("element_3")
    xor_linked_list.add("element_4")

    assert xor_linked_list.get(0) == "element_1"
    assert xor_linked_list.get(1) == "element_2"
    assert xor_linked_list.get(2) == "element_3"
    assert xor_linked_list.get(3) == "element_4"

if __name__ == '__main__':
    main()